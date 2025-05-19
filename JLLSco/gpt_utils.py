import openai
import os
import ast

openai.api_key = os.getenv("OPENAI_API_KEY")

def extract_functions_from_code(code: str):
    """파이썬 코드에서 함수 블록만 추출"""
    try:
        tree = ast.parse(code)
        funcs = [ast.get_source_segment(code, node) for node in tree.body if isinstance(node, ast.FunctionDef)]
        return funcs
    except:
        return []

def generate_testcases_for_function(func_code: str):
    """GPT 호출하여 함수에 대한 테스트케이스 생성"""
    prompt = f"""
다음 Python 함수에 대해 테스트 목적과 예상 결과를 포함한 테스트 시나리오를 생성해줘.

```python
{func_code}
