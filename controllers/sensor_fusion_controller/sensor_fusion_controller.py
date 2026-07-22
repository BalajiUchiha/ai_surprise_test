from controller import Robot

# Initialize Webots Robot instance
robot = Robot()
time_step = int(robot.getBasicTimeStep())

# Enable Sensors
camera = robot.getDevice('camera')
camera.enable(time_step)

lidar = robot.getDevice('lidar')
lidar.enable(time_step)
lidar.enablePointCloud()

imu = robot.getDevice('inertial unit')
imu.enable(time_step)

# Initialize Actuators (Motors)
left_motor = robot.getDevice('left wheel motor')
right_motor = robot.getDevice('right wheel motor')
left_motor.setPosition(float('inf'))
right_motor.setPosition(float('inf'))

print("[SYSTEM INITIALIZED] Sensor Fusion Engine Running...")

while robot.step(time_step) != -1:
    # 1. Read Sensor Data
    roll, pitch, yaw = imu.getRollPitchYaw()
    lidar_data = lidar.getRangeImage()
    min_dist = min(lidar_data) if lidar_data else 10.0

    # 2. Sensor Fusion & Decision Logic
    if min_dist < 0.6:
        left_motor.setVelocity(0.0)
        right_motor.setVelocity(0.0)
        print(f"[FUSION ALERT] Obstacle at {min_dist:.2f}m! Stopping.")
    else:
        left_motor.setVelocity(2.0)
        right_motor.setVelocity(2.0)
