# Python modules
import time
import mmap
from PIL import Image

# 3rd party modules
import posix_ipc

# Utils for this demo
import utils
import geo_tagging as gt
import io
import sys

#CMPE 295 libraries
from camera import Camera
import cv2
import os

device = "\dev\ttyTHS2"
frame = gt.geotag(device)
print(type(frame))
py_major_version = sys.version_info[0]

print("Geotagging starts")
params = utils.read_params()

## Create the shared memory and the semaphore.
memory = posix_ipc.SharedMemory(params["SHARED_MEMORY_NAME"], posix_ipc.O_CREX,
                                size=params["SHM_SIZE"])
semaphore = posix_ipc.Semaphore(params["SEMAPHORE_NAME"], posix_ipc.O_CREX,0600, 1)

## MMap the shared memory
mapfile = mmap.mmap(memory.fd, memory.size)

## Once I've mmapped the file descriptor, I can close it without
## interfering with the mmap.
memory.close_fd()

print(semaphore.value)
semaphore.acquire()
print(frame.size, frame.mode)
image_to_be_written = frame.tobytes()
frame.show()
print(len(image_to_be_written))
utils.write_to_memory(mapfile, image_to_be_written)
semaphore.release()


