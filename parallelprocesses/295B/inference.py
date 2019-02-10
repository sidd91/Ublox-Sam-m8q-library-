# Python modules
import mmap
import numpy as np
import cv2
import os
import sys
import hashlib
from PIL import Image
# 3rd party modules
import posix_ipc

# Utils for this demo
import utils

sys.path.append(os.path.join('/home/nvidia/darknet/','python'))
import darknet as dn
PY_MAJOR_VERSION = sys.version_info[0]

params = utils.read_params()

global cam, classifier_list, images, classifier, path, dstdir, images_list_file, camera_list, labels_list, cur_location, client, home, net, meta

#Check if the shared memory and semaphore exists
while 1:
    try:
        memory = posix_ipc.SharedMemory(params["SHARED_MEMORY_NAME"])
        semaphore = posix_ipc.Semaphore(params["SEMAPHORE_NAME"])
    except posix_ipc.ExistentialError:
        continue
    
    break

# MMap the shared memory
mapfile = mmap.mmap(memory.fd, memory.size)
# Once I've mmapped the file descriptor, I can close it without
# interfering with the mmap. This also demonstrates that os.close() is a
# perfectly legitimate alternative to the SharedMemory's close_fd() method.
os.close(memory.fd)

def convert_PIL_to_cv2object(frame):
#    nparr = np.fromstring(s)
    open_cv_image = np.array(frame)
    image = open_cv_image[:, :, ::-1].copy()
#img_np = cv2.imdecode(nparr, cv2.IMREAD_COLOR) 
    return image

def load_all_config():
    global cam, classifier_list, images, classifier, path, dstdir, images_list_file, camera_list, labels_list, cur_location, client, home, net, meta
  

def testing_illegal(frame, mydir_illegal):
    global cam, classifier_list, images, classifier, path, dstdir, images_list_file, camera_list, labels_list, cur_location, client, home, net, meta
    #Raw folder path
    dn.set_gpu(0)
    net = dn.load_net(bytes("/home/nvidia" + "/darknet/yolo-obj.cfg"), bytes("/home/nvidia" + "/darknet/yolo-obj_40000.weights"), 0)
    meta = dn.load_meta(bytes("/home/nvidia" + "/darknet/obj.data"))
  
    #Classified folder path
    folder_classified = mydir_illegal
    count = 0
    font = cv2.FONT_HERSHEY_SIMPLEX
    labels_list = ['cart', 'electronics','furniture', 'mattress', 'sofa', 'trash_bags', 'trash'] 
    chart_colors = [(204,102,51),(18,557,220),(0,153,255),(24,150,16),(175,175,246),(172,62,59),(198,153,0)]
    #Perform detection for every image in the files list
    images = []
    classifier = []
    classifier_list = []

    image_cv2 = frame
    cv2.imwrite("test_file.jpg", frame)    
    r = dn.detect(net, meta, "test_file.jpg")	
    print (r)
    cnt = 0
    if r != []:
	while cnt < len(r):
	    name = r[cnt][0]
	    if name in labels_list:
	    	i = labels_list.index(name)
	    predict = r[cnt][1]
	    #print (name+":"+str(predict))
	    classifier.append(name)

	    x = r[cnt][2][0]
	    y = r[cnt][2][1]
	    w = r[cnt][2][2]
	    z = r[cnt][2][3]

	    x_max = int(round((2*x+w)/2))
	    x_min = int(round((2*x-w)/2))

	    y_min = int(round((2*y-z)/2))
	    y_max = int(round((2*y+z)/2))
	    print (x_min, y_min, x_max, y_max)
	    pixel_list = [ x_min, y_min, x_max, y_max]
	    neg_index = [pixel_list.index(val) for val in pixel_list if val < 0]
	    cv2.rectangle(image_cv2,(x_min,y_min),(x_max,y_max),(chart_colors[i]), 2)
	    if neg_index == []:
		cv2.rectangle(image_cv2,(x_min,y_min-24), (x_min+10*len(name),y_min),chart_colors[i],-1)
		cv2.putText(image_cv2,name,(x_min,y_min-12), font, 0.5,(0,0,0),1,cv2.LINE_AA)
	    else:
		if (y_min < 0 and x_min > 0):
		    cv2.rectangle(image_cv2,(x_min,0), (x_min+10*len(name),24),chart_colors[i],-1)
		    cv2.putText(image_cv2,name,(x_min,12), font, 0.5,(0,0,0),1,cv2.LINE_AA)
		elif (x_min < 0 and y_min > 0):
		    cv2.rectangle(image_cv2,(0,y_min-24), (10*len(name),y_min),chart_colors[i],-1)
		    cv2.putText(image_cv2,name,(0,y_min-12), font, 0.5,(0,0,0),1,cv2.LINE_AA)
		elif (x_min < 0 and y_min < 0):
		    cv2.rectangle(image_cv2,(0,24), (10*len(name),48),chart_colors[i],-1)
		    cv2.putText(image_cv2,name,(0,12), font, 0.5,(0,0,0),1,cv2.LINE_AA)
            #cv2.imshow('image',image_cv2)
	    #cropped = image.crop((x_min, y_min+20, x_max, y_max))
	    cnt+=1
	classifier_list.append(" ".join(set(classifier)))
	count += 1
	saving_path = folder_classified+ name +"_"+ str(count) + ".jpg"
	print (saving_path)
	images.append(saving_path)
	#file1.write(name+",")
	cv2.imwrite(saving_path,image_cv2)
	cv2.destroyAllWindows()
#file1.write("\n")


while(1):
    semaphore.acquire()
    print("Process 2") 
    s = utils.read_from_memory(mapfile)
    #im = convert_bytes_to_cv2object(s)
    frame = Image.frombytes('RGB',(640,480),s,'raw')
    #frame.show()
    im = convert_PIL_to_cv2object(frame)
    #cv2.imshow('jaimatadi',im)
    #cv2.waitKey()
    semaphore.release()
    testing_illegal(im, "./")


