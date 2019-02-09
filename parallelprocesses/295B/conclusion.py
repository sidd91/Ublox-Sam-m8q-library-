# Python modules
import mmap
import os
import sys
import hashlib
from PIL import Image
# 3rd party modules
import posix_ipc

# Utils for this demo
import utils


PY_MAJOR_VERSION = sys.version_info[0]

utils.say("Oooo 'ello, I'm Mrs. Conclusion!")

params = utils.read_params()

# Mrs. Premise has already created the semaphore and shared memory.
# I just need to get handles to them.

try:
    memory = posix_ipc.SharedMemory(params["SHARED_MEMORY_NAME"])
except posix_ipc.ExistentialError:
    print("error")
   #continue
try:
    semaphore = posix_ipc.Semaphore(params["SEMAPHORE_NAME"])
except posix_ipc.ExistentialError:
    print("error")
   #continue
# MMap the shared memory
mapfile = mmap.mmap(memory.fd, memory.size)
# Once I've mmapped the file descriptor, I can close it without
# interfering with the mmap. This also demonstrates that os.close() is a
# perfectly legitimate alternative to the SharedMemory's close_fd() method.
os.close(memory.fd)

print(semaphore.value)


while(1):
    semaphore.acquire()
    s = utils.read_from_memory(mapfile)
    semaphore.release()
    break

semaphore.close()
mapfile.close()
print("Image read")
#print(s)
#s = s.encode()
#frame = Image.open(s)
frame = Image.frombytes('RGB',(640,480),s,'raw')
print(type(frame))
frame.show()
