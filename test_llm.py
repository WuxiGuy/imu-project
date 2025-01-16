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
            # 针对 Raspberry Pi 优化的配置
            llm = Llama(
                model_path="llama.cpp/models/Mistral-7B-Instruct-v0.3.Q5_K_M.gguf",
                n_ctx=256,           # 减小上下文窗口以节省内存
                n_threads=2,         # 减少线程数以避免过载
                n_batch=1,           # 最小批处理大小
                n_gpu_layers=0,      # 禁用 GPU 层
                verbose=False
            )
            
            # 使用更短的提示
            prompt = """<s>[INST] Say "Hi!" [/INST]"""
            
            print("Model loaded, generating response...")
            
            response = llm.create_chat_completion(
                messages=[{
                    "role": "user",
                    "content": prompt
                }],
                max_tokens=10,       # 减少生成的标记数
                temperature=0.1,
                stop=["</s>", "[INST]", "\n"]
            )
            
            print("\nResponse:", response['choices'][0]['message']['content'])
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    print("Starting LLM test...")
    test_llm() 