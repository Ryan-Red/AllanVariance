# # First import the library
# import pyrealsense2 as rs
# import math as m


import pyrealsense2 as rs
import numpy as np
import time


class dataFrame:

    def __init__(self):
        self.time = np.array([])
        self.x = np.array([])
        self.y = np.array([])
        self.z = np.array([])

    def add_data(self, timeStamp, data):
        self.time = np.append(self.time, timeStamp*10e-9)#convert to seconds
        self.x = np.append(self.x, data.x)
        self.y = np.append(self.y, data.y)
        self.z = np.append(self.z, data.z)

    def save_file(self, filename,headers=["time (s)", "x-axis", "y-axis", "z-axis"]):

        file = filename + ".txt"
        headerString = ""
        for header in headers:
            headerString = headerString + header + "\t"

        np.savetxt(file,np.column_stack((self.time, self.x,self.y,self.z)),delimiter="\t",header=headerString)



# Configure depth and color streams
pipeline = rs.pipeline()
cfg = rs.config()

# Get device product line for setting a supporting resolution
pipeline_wrapper = rs.pipeline_wrapper(pipeline)

cfg.enable_stream(rs.stream.accel)
cfg.enable_stream(rs.stream.gyro)


# Start streaming
pipeline.start(cfg)

gyro = dataFrame()
accel = dataFrame()

t_start = time.time()

i = 0


try:
    while True:

        # Wait for a coherent pair of frames: depth and color
        frames = pipeline.wait_for_frames()
        depth_frame = frames.get_depth_frame()
        color_frame = frames.get_color_frame()

        gyro.add_data(time.time_ns(), frames[1].as_motion_frame().get_motion_data())
        accel.add_data(time.time_ns(), frames[0].as_motion_frame().get_motion_data())

        if(time.time() - t_start  >= 100):
            i+=1
            gyro.save_file("gyroTest_{}".format(i))
            accel.save_file("accelTest_{}".format(i))
            t_start = time.time()

        time.sleep(0.01)


        # print(gyro.data)
        # print(accel.data)

except KeyboardInterrupt as e:
    gyro.save_file("gyroTest")
    accel.save_file("accelTest")

finally:

    # Stop streaming
    pipeline.stop()