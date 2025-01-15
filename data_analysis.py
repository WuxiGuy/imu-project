import time
import sqlite3

DB_PATH = "sensor_data.db"

def fetch_recent_data(duration=5):
	"""
	Fetch rows from the last 'duration' seconds.
	Returns a list of tuples: (timestamp, ax, ay, az, gx, gy, gz).
	"""
	current_time = time.time()
	start_time = current_time - duration
	conn = sqlite3.connect(DB_PATH)
	cursor = conn.cursor()
	cursor.execute("""
		SELECT timestamp, ax, ay, az, gx, gy, gz
		FROM sensor_data
		WHERE timestamp >= ?
		ORDER BY timestamp ASC
	""", (start_time,))
	rows = cursor.fetchall()
	conn.close()
	return rows

def analyze_motion(rows):
	"""
	Perform basic threshold checks on raw data.
	Returns a string: 'heavy vibration', 'unstable posture', 'slipping', or 'stable'.
	This is a simplified demonstration. Real computation would require calibration and integration.
	"""
	if not rows:
		return "stable"

	# Example thresholds for raw differences (placeholders):
	up_down_threshold = 3000
	left_right_threshold = 3000
	rotation_threshold = 2000

	ax_values = [r[1] for r in rows]  # raw ax
	ay_values = [r[2] for r in rows]  # raw ay
	gz_values = [r[6] for r in rows]  # raw gz

	ax_diff = max(ax_values) - min(ax_values)
	ay_diff = max(ay_values) - min(ay_values)
	gz_diff = max(gz_values) - min(gz_values)

	if ax_diff > up_down_threshold:
		return "heavy vibration"
	elif ay_diff > left_right_threshold:
		return "unstable posture"
	elif gz_diff > rotation_threshold:
		return "slipping"
	else:
		return "stable"

def get_motion_status(duration=5):
	"""
	Fetch recent sensor data, analyze, and return a string status.
	"""
	rows = fetch_recent_data(duration)
	status = analyze_motion(rows)
	return status
