# AirSim Module
import airsim

# Initialize and connect to Airsim
def initialize_airsim():
    client = airsim.MultirotorClient()
    client.confirmConnection()
    return client

# Enable API control
def enable_api_control(client):
    client.enableApiControl(True)
    client.armDisarm(True)

# Arm the drone
def arm_quadcopter(client):
    client.armDisarm(client)

# Disable API control and arm the drone
def disable_api_control(client):
    client.enableApiControl(False)

# Disarm the quadcopter
def disarm_quadcopter(client):
    client.armDisarm(False)


