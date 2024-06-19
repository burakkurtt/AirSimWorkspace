import airsim
from Module import AirSimModule
import time

vehicleName = "Quad1"
flightMode = "TakeOff"

client = AirSimModule.initialize_airsim()
AirSimModule.enable_api_control(client)

while True:
    if flightMode == "TakeOff":
        












AirSimModule.disable_api_control(client)
AirSimModule.disarm_quadcopter(client)


