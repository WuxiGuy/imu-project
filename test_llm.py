import os
import sys
from contextlib import contextmanager
from llama_cpp import Llama

# Suppress all debug output
os.environ['GGML_VERBOSE'] = '0'

@contextmanager
def suppress_stderr():
    """Temporarily suppress stderr output"""
    stderr = sys.stderr
    with open(os.devnull, 'w') as devnull:
        sys.stderr = devnull
        try:
            yield
        finally:
            sys.stderr = stderr

def test_llm():
    try:
        with suppress_stderr():
            llm = Llama(
                model_path="llama.cpp/models/Mistral-7B-Instruct-v0.3.Q5_K_M.gguf",
                n_ctx=512,
                n_threads=4,
                n_batch=8,
                verbose=False
            )
            
            prompt = """<s>[INST] Say "Hello from Raspberry Pi!" [/INST]"""
            
            response = llm.create_chat_completion(
                messages=[{
                    "role": "user",
                    "content": prompt
                }],
                max_tokens=20,
                temperature=0.1,
                stop=["</s>", "[INST]", "\n"]
            )
            
            print("\nResponse:", response['choices'][0]['message']['content'])
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_llm() 