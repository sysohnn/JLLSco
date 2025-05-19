import streamlit as st
import zipfile
import os
import shutil
import tempfile
import pandas as pd
from gpt_utils import extract_functions_from_code, generate_testcases_for_function

st.set_page_config(page_title="📦 TC-Bot Folder Processor", layout="wide")
st.title("🧠 TC-Bot - 소스코드 ZIP 업로드로 테스트케이스 자동 생성")

uploaded_file = st.file_uploader("소스코드가 포함된 ZIP 파일을 업로드하세요", type="zip")

if uploaded_file:
    with tempfile.TemporaryDirectory() as tmpdir:
        zip_path = os.path.join(tmpdir, "code.zip")
        with open(zip_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        # 압축 해제
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(tmpdir)

        py_files = []
        for root, _, files in os.walk(tmpdir):
            for file in files:
                if file.endswith(".py"):
                    py_files.append(os.path.join(root, file))

        results = []
        for filepath in py_files:
            with open(filepath, "r", encoding="utf-8") as f:
                code = f.read()
            functions = extract_functions_from_code(code)
            for func in functions:
                testcase = generate_testcases_for_function(func)
                results.append({"file": os.path.basename(filepath), "function": func[:100], "testcase": testcase})

        df = pd.DataFrame(results)

        st.success("✅ 테스트케이스 생성 완료!")
        st.dataframe(df)

        # 엑셀로 다운로드
        excel_file = os.path.join(tmpdir, "testcases.xlsx")
        df.to_excel(excel_file, index=False)
        with open(excel_file, "rb") as f:
            st.download_button("📥 테스트케이스 엑셀 다운로드", f, file_name="testcases.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
