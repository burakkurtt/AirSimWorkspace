# AirSim Class
import airsim
import numpy as np
import time
import cv2

class AirSimWrapper:
    def __init__(self):
        # Connect to AirSim
        self.client = airsim.MultirotorClient()
        self.client.confirmConnection()

        # Set default values
        self.takeOff_height = 10.0  # meters
        self.max_speed = 1.0 # meters per seconds
        self.min_distance = 2.0 # meters

    def takeoff(self):
        self.client.takeoffAsync().join()
        self.client.moveToZAsync(-self.takeOff_height, self.max_speed).join()

    def land(self):
        self.client.landAsync().join()

    def arm(self):
        self.client.enableApiControl(True)
        self.client.armDisarm(True)

    def disarm(self):
        self.client.armDisarm(False)
        self.client.enableApiControl(False)

    def move_to_position(self, x, y, z):
        self.client.moveToPositionAsync(x, y, z, self.max_speed).join()

    def get_position(self):
        state = self.client.getMultirotorState()
        position = state.kinematics_estimated.position
        return np.array([position.x_val, position.y_val, position.z_val])

    def get_linear_velocity(self):
        state = self.client.getMultirotorState()
        linear_velocity = state.kinematics_estimated.linear_velocity
        return np.array([linear_velocity.x_val, linear_velocity.y_val, linear_velocity.z_val])
    
    def get_angular_velocity(self):
        state = self.client.getMultirotorState()
        angular_velocity = state.kinematics_estimated.angular_velocity
        return np.array([angular_velocity.x_val, angular_velocity.y_val, angular_velocity.z_val])
    
    def set_linear_velocity(self, vx, vy, vz):
        self.client.moveByVelocityAsync(vx, vy, vz, duration=1).join()

    def hover(self):
        self.client.hoverAsync().join()
        
    def wait(self, duration):
        time.sleep(duration)    

    def reset(self):
        # Reset environment (e.g., return drone to initial position)
        self.client.reset()

    def close(self):
        # Close the connection to AirSim
        self.client.reset()
        self.client.close()

    def display_msg(self):
        print("Client Running")

    def get_image_front_camera(self):    
        # Capture a single image from the front center camera
        responses = self.client.simGetImages([airsim.ImageRequest("0", airsim.ImageType.Scene, False, False)])
        # Process the response
        response = responses[0]
        # Convert the image to a numpy array [Get the image data as a 1D array]
        img1d = np.frombuffer(response.image_data_uint8, dtype=np.uint8)
        # Reshape to 3-channel image array HxWx3
        img_rgb = img1d.reshape(response.height, response.width, 3)
        return img_rgb





