#!/usr/bin/env python
# coding: utf-8

# In[123]:


import turicreate as tc
from matplotlib import pyplot as plt
import numpy as np
from PIL import Image
import cv2
import pandas as pd

# load the license plate model
plate_model = tc.load_model('models/my_model_real_plates.model')

#load the character recognition model
char_model = tc.load_model('models/my_model_characters1.model')

# code that takes in an image, crops out the plate to return as an image
def find_plate(filename, model): #filename,model

    # load the image, make an sFrame
    image_sarray = tc.image_analysis.load_images('new_test_images', "auto", with_path=False,recursive=True)
    image = cv2.imread('new_test_images/'+ filename)
    #plt.imshow(image)

    # run the prediction
    predictions = model.predict(image_sarray) # make predictions

    # crop based on the bounding box (there might be more than one - deal with that later)
    y = int(round(predictions[0][0]['coordinates']['y']))
    x = int(round(predictions[0][0]['coordinates']['x']))
    w = int(round((predictions[0][0]['coordinates']['width'])/2))
    h = int(round((predictions[0][0]['coordinates']['height'])/2))

    cropped = image[y-h:y+h,x-w:x+w]
    return cropped


# code that takes in the cropped plate and does character recognition, returns just the character string
def read_plate(filename, model):

    # load the image, make an sFrame
    image_sarray = tc.image_analysis.load_images('new_char_test_images', "auto", with_path=False,recursive=True)
    image = cv2.imread('new_char_test_images/'+ filename)

    # run the prediction
    predictions = model.predict(image_sarray) # make predictions

    # crop based on the bounding boxes
    # create ordering based on x coord
    order = {}
    boxes = []

    for box in predictions[0]:
        label = box['label']
        x = box['coordinates']['x']
        y = box['coordinates']['y']
        w = box['coordinates']['width']
        h = box['coordinates']['height']
        confidence = box['confidence']
        info = [label,x,y,w,h,confidence]
        order[round(box['coordinates']['x'],3)] = info # round the key to 3 decimal places for easier look-up
        boxes.append(info)

    #for key in sorted(order.keys()): # uncomment if looking for original recognition results
    #    print("%s: %s" % (key, order[key]))

    # clean the recognition results (get rid of repeats)
    i = 0
    for i in range(0,len(boxes)-1):
        for j in range(i+1,len(boxes)):
            if (abs(boxes[i][1] - boxes[j][1]) < boxes[i][3]/2) and (abs(boxes[i][2] - boxes[j][2]) < boxes[i][4]/2):
                if boxes[i][5] < boxes[j][5]:
                    if round(boxes[i][1],3) in order:
                        del order[round(boxes[i][1],3)]
                else:
                    if round(boxes[j][1],3) in order:
                        del order[round(boxes[j][1],3)]
            j+=1
        i+=1

    print('-------------------------------------------------------------------------------------')
    plate_num = ''
    for key in sorted(order.keys()):
        plate_num = plate_num + order[key][0]

    return plate_num


# code that does the whole process
def full_recognition(image,plate_model,char_model):
    # first save the image to a file (can overwrite existing files because we only need one in there at a time)
    filename = 'new_test_images/platephoto.jpg'
    Image.fromarray(image).save(filename)

    # do plate recognition to crop out the plate
    plate = find_plate('platephoto.jpg',plate_model)

    # save the cropped plate to a file (can overwrite existing files here as well)
    filename = 'new_char_test_images/plate.jpg'
    Image.fromarray(plate).save(filename)

    # do character recognition
    plate_num = read_plate('plate.jpg',char_model)

    return plate_num

# Run an example
def readPlate(img):
    image = cv2.imread(img) # in the final code this image will be whatever is captured on the pi-cam
    platenumber = full_recognition(image,plate_model,char_model)
    return(platenumber)


# In[ ]:





# In[ ]:






# In[ ]:





# In[ ]:





# In[ ]:







# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:
