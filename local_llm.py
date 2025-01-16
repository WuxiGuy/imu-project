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
		
		prompt = f"""### Human: Analyze device status with these readings:
				Vertical: {vertical_movement:.2f} cm
				Horizontal: {horizontal_movement:.2f} cm
				Rotation: {rotation:.2f} degrees

				Rules:
				- vertical > 3cm = "vibrating"
				- horizontal > 3cm = "unstable"
				- rotation > 90° = "slipping"
				- otherwise = "stable"

				Respond with one word only: "stable", "slipping", "unstable", or "vibrating"
				### Assistant:"""
		return prompt

	def get_device_status(self):
		while True:
			try:
				with suppress_stderr():
					analysis_results = self.data_analyzer.analyze_recent_data(seconds=30)
					prompt = self.generate_prompt(analysis_results)
					
					response = self.llm.create_completion(
						prompt=prompt,
						max_tokens=10,
						temperature=0.1,
						stop=["###", "\n"]
					)
					
					status = response['choices'][0]['text'].strip()
					valid_states = {"stable", "slipping", "unstable", "vibrating"}
					if status.lower() in valid_states:
						print(status.lower())
					else:
						print("stable")
				
			except Exception as e:
				print(f"Error: {e}")
			
			time.sleep(5)