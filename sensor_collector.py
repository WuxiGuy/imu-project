import time
import sqlite3
from datetime import datetime
import smbus2

class SensorCollector:
	def __init__(self):
		# MPU6050 constants
		self.MPU_ADDR = 0x68  # Default I2C address of MPU6050
		self.PWR_MGMT_1 = 0x6B
		self.ACCEL_XOUT_H = 0x3B
		self.GYRO_XOUT_H = 0x43
		
		# Initialize I2C bus
		self.bus = smbus2.SMBus(1)  # Use bus 1 for Raspberry Pi
		self.db_path = "sensor_data.db"
		
		# Wake up MPU6050
		self.bus.write_byte_data(self.MPU_ADDR, self.PWR_MGMT_1, 0)
	
	def read_word_2c(self, register):
		"""Read two bytes and convert to 2's complement"""
		high = self.bus.read_byte_data(self.MPU_ADDR, register)
		low = self.bus.read_byte_data(self.MPU_ADDR, register + 1)
		
		value = (high << 8) + low
		
		if value >= 0x8000:
			value = -((65535 - value) + 1)
		return value
	
	def read_sensor(self):
		"""Read current sensor data"""
		try:
			# Read accelerometer data (16384 is the default sensitivity for ±2g)
			accel_x = self.read_word_2c(self.ACCEL_XOUT_H) / 16384.0
			accel_y = self.read_word_2c(self.ACCEL_XOUT_H + 2) / 16384.0
			accel_z = self.read_word_2c(self.ACCEL_XOUT_H + 4) / 16384.0
			
			# Read gyroscope data (131 is the default sensitivity for ±250deg/s)
			gyro_x = self.read_word_2c(self.GYRO_XOUT_H) / 131.0
			gyro_y = self.read_word_2c(self.GYRO_XOUT_H + 2) / 131.0
			gyro_z = self.read_word_2c(self.GYRO_XOUT_H + 4) / 131.0
			
			return {
				'x': accel_x,
				'y': accel_y,
				'z': accel_z,
				'rotation_x': gyro_x,
				'rotation_y': gyro_y,
				'rotation_z': gyro_z
			}
		except Exception as e:
			print(f"Error reading sensor: {e}")
			return None
	
	def save_to_db(self, sensor_data):
		"""Save sensor data to database"""
		if sensor_data is None:
			return
			
		conn = sqlite3.connect(self.db_path)
		cursor = conn.cursor()
		
		cursor.execute("""
			INSERT INTO sensor_data 
			(timestamp, x, y, z, rotation_x, rotation_y, rotation_z)
			VALUES (?, ?, ?, ?, ?, ?, ?)
		""", (
			datetime.now().timestamp(),
			sensor_data['x'],
			sensor_data['y'],
			sensor_data['z'],
			sensor_data['rotation_x'],
			sensor_data['rotation_y'],
			sensor_data['rotation_z']
		))
		
		conn.commit()
		conn.close()
	
	def collect_data(self):
		"""Main loop for continuous data collection"""
		while True:
			try:
				sensor_data = self.read_sensor()
				self.save_to_db(sensor_data)
				time.sleep(0.1)  # Collect data every 0.1 seconds
			except Exception as e:
				print(f"Error collecting sensor data: {e}")
				time.sleep(1)  # Wait 1 second on error before retrying

