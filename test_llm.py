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
            # 使用 TinyLlama
            llm = Llama(
                model_path="llama.cpp/models/TinyLlama-1.1B-Chat-v1.0.Q2_K.gguf",
                n_ctx=256,
                n_threads=2,
                n_batch=1,
                n_gpu_layers=0,
                verbose=False
            )
            
            prompt = """<|system|>You are a helpful assistant.</s>
<|user|>Say hi!</s>
<|assistant|>"""
            
            print("Model loaded, generating response...")
            
            response = llm.create_completion(
                prompt=prompt,
                max_tokens=10,
                temperature=0.1,
                stop=["</s>", "<|user|>", "<|system|>", "\n"]
            )
            
            print("\nResponse:", response['choices'][0]['text'])
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    print("Starting LLM test...")
    test_llm() 