import time
import sqlite3
import smbus2

# MPU9250 register addresses
ACCEL_XOUT_H = 0x3B
GYRO_XOUT_H = 0x43
PWR_MGMT_1 = 0x6B
MPU_ADDRESS = 0x68  # Default address if AD0 pin is low

DB_PATH = "sensor_data.db"

def read_word_2c(bus, addr, reg):
	"""
	Read two bytes from 'reg' and combine them into one signed 16-bit value.
	"""
	high = bus.read_byte_data(addr, reg)
	low = bus.read_byte_data(addr, reg + 1)
	val = (high << 8) + low
	if val >= 0x8000:
		val = -((65535 - val) + 1)
	return val

def setup_mpu(bus, addr):
	"""
	Write to PWR_MGMT_1 to wake up the MPU device.
	"""
	bus.write_byte_data(addr, PWR_MGMT_1, 0x00)
	time.sleep(0.1)

def read_accel_gyro(bus, addr):
	"""
	Read raw accelerometer and gyroscope data from the MPU.
	Returns (ax, ay, az, gx, gy, gz).
	Note: Real displacement or rotation requires further calculation or filtering.
	"""
	ax_raw = read_word_2c(bus, addr, ACCEL_XOUT_H)
	ay_raw = read_word_2c(bus, addr, ACCEL_XOUT_H + 2)
	az_raw = read_word_2c(bus, addr, ACCEL_XOUT_H + 4)

	gx_raw = read_word_2c(bus, addr, GYRO_XOUT_H)
	gy_raw = read_word_2c(bus, addr, GYRO_XOUT_H + 2)
	gz_raw = read_word_2c(bus, addr, GYRO_XOUT_H + 4)

	return ax_raw, ay_raw, az_raw, gx_raw, gy_raw, gz_raw

def insert_imu_reading(timestamp, ax, ay, az, gx, gy, gz):
	"""
	Insert one IMU reading into the SQLite database.
	"""
	conn = sqlite3.connect(DB_PATH)
	cursor = conn.cursor()
	cursor.execute("""
		INSERT INTO sensor_data (timestamp, ax, ay, az, gx, gy, gz)
		VALUES (?, ?, ?, ?, ?, ?, ?)
	""", (timestamp, ax, ay, az, gx, gy, gz))
	conn.commit()
	conn.close()

def main():
	"""
	Continuously read sensor data and store it in the database.
	"""
	bus = smbus2.SMBus(1)
	setup_mpu(bus, MPU_ADDRESS)

	sampling_rate = 50  # Hz
	interval = 1.0 / sampling_rate

	while True:
		ax, ay, az, gx, gy, gz = read_accel_gyro(bus, MPU_ADDRESS)
		ts = time.time()
		insert_imu_reading(ts, ax, ay, az, gx, gy, gz)
		time.sleep(interval)

if __name__ == "__main__":
	main()

