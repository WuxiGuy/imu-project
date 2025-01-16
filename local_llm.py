import time
import os
import sys
from contextlib import contextmanager
from llama_cpp import Llama
from data_analysis import DataAnalyzer

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

class LocalLLM:
    def __init__(self):
        with suppress_stderr():
            self.model_path = "llama.cpp/models/TinyLlama-1.1B-Chat-v1.0.Q2_K.gguf"
            self.llm = Llama(
                model_path=self.model_path,
                n_ctx=256,
                n_threads=2,
                n_batch=1,
                n_gpu_layers=0,
                verbose=False
            )
            self.data_analyzer = DataAnalyzer()
        
    def generate_prompt(self, analysis_results):
        vertical_movement = analysis_results.get('vertical_movement', 0)
        horizontal_movement = analysis_results.get('horizontal_movement', 0)
        rotation = analysis_results.get('rotation', 0)
        
        prompt = f"""<|system|>You are a device status analyzer. Respond with only one of these states: "heavy vibration", "unstable posture", "slipping", or "stable".</s>
<|user|>Data:
    - Vertical: {vertical_movement:.2f} cm
    - Horizontal: {horizontal_movement:.2f} cm
    - Rotation: {rotation:.2f} degrees

Rules:
    1. vertical > 3cm = "heavy vibration"
    2. horizontal > 3cm = "unstable posture"
    3. rotation > 90° = "slipping"
    4. minimal changes = "stable"</s>
<|assistant|>"""
        return prompt

    def get_device_status(self):
        while True:
            try:
                with suppress_stderr():
                    analysis_results = self.data_analyzer.analyze_recent_data(seconds=30)
                    prompt = self.generate_prompt(analysis_results)
                    
                    response = self.llm.create_completion(
                        prompt=prompt,
                        max_tokens=30,
                        temperature=0.1,
                        stop=["</s>", "<|user|>", "<|system|>", "\n"]
                    )
                    
                    status = response['choices'][0]['text'].strip()
                    print(status)
                
            except Exception as e:
                print(f"Error: {e}")
            
            time.sleep(5)