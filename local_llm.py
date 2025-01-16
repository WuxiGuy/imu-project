import time
from llama_cpp import Llama
from data_analysis import DataAnalyzer

class LocalLLM:
    def __init__(self):
        self.model_path = "llama.cpp/models/Mistral-7B-Instruct-v0.3.Q5_K_M.gguf"
        self.llm = Llama(model_path=self.model_path)
        self.data_analyzer = DataAnalyzer()
        
    def generate_prompt(self, analysis_results):
        vertical_movement = analysis_results.get('vertical_movement', 0)
        horizontal_movement = analysis_results.get('horizontal_movement', 0)
        rotation = analysis_results.get('rotation', 0)
        
        context = f"""
        Analyze device status based on sensor data:
        - Vertical movement: {vertical_movement:.2f} cm
        - Horizontal movement: {horizontal_movement:.2f} cm
        - Rotation angle: {rotation:.2f} degrees

        Please assess the device status according to these rules:
        1. If vertical movement frequently exceeds 3cm, classify as heavy vibration
        2. If horizontal movement frequently exceeds 3cm, classify as unstable posture
        3. If rotation angle frequently exceeds 90 degrees, classify as slipping
        4. If all measurements show minimal change, classify as stable

        Please briefly describe the current device status.
        """
        return context

    def get_device_status(self):
        while True:
            # Get analysis results for the past 30 seconds
            analysis_results = self.data_analyzer.analyze_recent_data(seconds=30)
            
            # Generate the prompt
            prompt = self.generate_prompt(analysis_results)
            
            # Call LLM for response
            response = self.llm.create_completion(
                prompt,
                max_tokens=100,
                temperature=0.1,
                stop=["。", "\n"]
            )
            
            print(f"Device Status Assessment: {response.choices[0].text}")
            
            # Wait 5 seconds before next assessment
            time.sleep(5)