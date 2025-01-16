import threading
from sensor_collector import SensorCollector
from local_llm import LocalLLM

def main():
	# Create sensor collector instance
	sensor_collector = SensorCollector()
	
	# Create LLM instance
	llm = LocalLLM()
	
	# Create and start sensor data collection thread
	sensor_thread = threading.Thread(
		target=sensor_collector.collect_data,
		daemon=True
	)
	sensor_thread.start()
	
	# Create and start LLM analysis thread
	llm_thread = threading.Thread(
		target=llm.get_device_status,
		daemon=True
	)
	llm_thread.start()
	
	try:
		# Keep main thread running
		while True:
			sensor_thread.join(1)
			llm_thread.join(1)
	except KeyboardInterrupt:
		print("\nProgram terminated")

if __name__ == "__main__":
	main()
