import sqlite3
import numpy as np
from datetime import datetime, timedelta

class DataAnalyzer:
	def __init__(self):
		self.db_path = "sensor_data.db"
	
	def get_recent_data(self, seconds=30):
		"""Retrieve sensor data from the recent time period"""
		conn = sqlite3.connect(self.db_path)
		cursor = conn.cursor()
		
		time_threshold = datetime.now() - timedelta(seconds=seconds)
		
		query = """
		SELECT timestamp, x, y, z, rotation_x, rotation_y, rotation_z 
		FROM sensor_data 
		WHERE timestamp > ?
		ORDER BY timestamp
		"""
		
		cursor.execute(query, (time_threshold.timestamp(),))
		data = cursor.fetchall()
		
		conn.close()
		return data
	
	def analyze_recent_data(self, seconds=30):
		"""Analyze recent sensor data for movement patterns"""
		data = self.get_recent_data(seconds)
		if not data:
			return {
				'vertical_movement': 0,
				'horizontal_movement': 0,
				'rotation': 0
			}
		
		# Convert data to numpy array for calculations
		data_array = np.array(data)
		
		# Calculate position changes
		positions = data_array[:, 1:4]  # x, y, z coordinates
		vertical_movement = np.std(positions[:, 2])  # z-axis standard deviation
		horizontal_movement = np.sqrt(np.std(positions[:, 0])**2 + np.std(positions[:, 1])**2)
		
		# Calculate rotation changes
		rotations = data_array[:, 4:7]  # rotation_x, rotation_y, rotation_z
		max_rotation = np.max(np.abs(rotations[:, 2]))  # using z-axis rotation
		
		return {
			'vertical_movement': vertical_movement * 100,  # convert to centimeters
			'horizontal_movement': horizontal_movement * 100,  # convert to centimeters
			'rotation': max_rotation  # degrees
		}
