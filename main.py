from Library import AirSimWrapper
from Utils import utils
import Slam
import threading
import time


quadClient = AirSimWrapper.AirSimWrapper()
slamClient = AirSimWrapper.AirSimWrapper()


# Slam Thread
def slam():
    print("SLAM thread has been started.")
    while True:
        imgRGB = slamClient.get_image_front_camera()
        Slam.image_process(imgRGB)
        time.sleep(0.1)

def main():
    print("MAIN thread has been started.")
    flightMode = "TAKEOFF"
    quadClient.reset()

    while True:
        # IDLE
        if flightMode == "IDLE":
            print("Flight Mode : IDLE")
            quadClient.wait(5)
            print("Air Vehicle Simulation Terminated.")
            break
        # TAKEOFF
        elif flightMode == "TAKEOFF":
            print("Flight Mode : TAKEOFF")
            quadClient.arm()
            quadClient.takeoff()

            flightMode = "MOVE"
        # LAND
        elif flightMode == "LAND":
            print("Flight Mode : LAND")
            quadClient.land()
            quadClient.disarm()
            
            flightMode = "IDLE"
        # HOVER
        elif flightMode == "HOVER":
            print("Flight Mode : HOVER")
            quadClient.hover()
            quadClient.wait(10)

            flightMode = "LAND"
        # MOVE
        elif flightMode == "MOVE":
            print("Flight Mode : MOVE")
            quadClient.move_to_position(10, 0, -quadClient.takeOff_height)

            flightMode = "LAND"
        # UNDEFINED
        else:
            quadClient.hover()
            print("Flight Mode : UNDEFINED(HOVER)")
            print("Undefined Flight Mode. Air Vehicle is Hovering.")
            quadClient.wait(5)
            print("Air Vehicle Simulation Terminated.")
            break

threads = []
threads.append(threading.Thread(target=slam, ))
threads.append(threading.Thread(target=main, ))

# Start all threads
for thread in threads:
    thread.start()

# Wait for all threads finish
for thread in threads:
    thread.join()

print("All threads are terminated.")