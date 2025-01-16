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
            self.model_path = "llama.cpp/models/Mistral-7B-Instruct-v0.3.Q5_K_M.gguf"
            self.llm = Llama(
                model_path=self.model_path,
                n_ctx=512,
                n_threads=2,
                n_batch=8,
                verbose=False
            )
            self.data_analyzer = DataAnalyzer()
        
    def generate_prompt(self, analysis_results):
        vertical_movement = analysis_results.get('vertical_movement', 0)
        horizontal_movement = analysis_results.get('horizontal_movement', 0)
        rotation = analysis_results.get('rotation', 0)
        
        prompt = f"""<s>[INST] You are a device status analyzer. Based on the following sensor data, analyze the device status:

Sensor Data:
- Vertical movement: {vertical_movement:.2f} cm
- Horizontal movement: {horizontal_movement:.2f} cm
- Rotation angle: {rotation:.2f} degrees

Rules for classification:
1. If vertical movement frequently exceeds 3cm: "heavy vibration"
2. If horizontal movement frequently exceeds 3cm: "unstable posture"
3. If rotation angle frequently exceeds 90 degrees: "slipping"
4. If all measurements show minimal change: "stable"

Provide a brief, clear status assessment in one sentence. [/INST]
"""
        return prompt

    def get_device_status(self):
        while True:
            try:
                with suppress_stderr():
                    # Get analysis results for the past 30 seconds
                    analysis_results = self.data_analyzer.analyze_recent_data(seconds=30)
                    
                    # Generate the prompt
                    prompt = self.generate_prompt(analysis_results)
                    
                    # Call LLM for response
                    response = self.llm.create_chat_completion(
                        messages=[{
                            "role": "user",
                            "content": prompt
                        }],
                        max_tokens=100,
                        temperature=0.1,
                        stop=["</s>", "[INST]", "\n"]
                    )
                    
                    status = response['choices'][0]['message']['content'].strip()
                    print(f"Device Status Assessment: {status}")
                
            except Exception as e:
                print(f"Error in LLM processing: {e}")
            
            # Wait 5 seconds before next assessment
            time.sleep(5)