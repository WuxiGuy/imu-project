import time
from data_analysis import get_motion_status
from llama_cpp import Llama

# Modify MODEL_PATH to match your actual local model file path
MODEL_PATH = "llama.cpp/models/Mistral-7B-Instruct-v0.3.Q5_K_M.gguf"

def run_llm_monitoring():
    """
    Periodically retrieve motion status from data_analysis and prompt the local LLM.
    """
    llm = Llama(
        model_path=MODEL_PATH,
        n_ctx=2048,
        n_threads=4
    )

    while True:
        # Get motion status for the last 5 seconds
        status = get_motion_status(duration=5)
        # Construct a simple prompt
        prompt = f"Current device motion status is: {status}. Please provide a brief explanation."
        
        output = llm.create_chat_completion(
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.5,
            max_tokens=64
        )

        # Call the local LLM
        response = output["choices"][0]["message"]["content"]

        print("========================================")
        print(f"Prompt: {prompt}")
        print(f"LLM Response: {response}")
        print("========================================")

        time.sleep(5)