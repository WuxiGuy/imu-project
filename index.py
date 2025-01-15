import time
import subprocess
# If you want to directly import functions from sensor_collector.py, you can do so.
# For example: from sensor_collector import main as sensor_main
# In this example, we run sensor_collector.py as a separate process.
from local_llm import run_llm_monitoring

def main():
	"""
	Main entry point that controls sensor data collection and local LLM monitoring.
	"""
	# Start the sensor collector as a separate subprocess.
	collector_process = subprocess.Popen(["python", "sensor_collector.py"])
	print("Sensor collector started.")

	try:
		# Run local LLM monitoring in the current process.
		run_llm_monitoring()
	except KeyboardInterrupt:
		print("Received KeyboardInterrupt. Stopping processes...")
	finally:
		# Terminate the sensor collector
		print("Terminating sensor_collector.py...")
		collector_process.terminate()
		collector_process.wait()
		print("Sensor collector stopped.")

if __name__ == "__main__":
	main()
