import os
from PIL import Image
import subprocess
import sys
import cv2

#data entry function from the command line
def data_comand():
    input_video = sys.argv[1]
    input_img = sys.argv[2]
    x_coord = sys.argv[3]
    x_coord = int(x_coord)
    y_coord = sys.argv[4]
    y_coord = int(y_coord)
    p = subprocess.call("./music_from_video")
    image_alignment(input_video,input_img,x_coord,y_coord)

#function image alignment
def image_alignment(input_video,input_img,x_coord,y_coord):
    img = Image.open(input_img)
    width = 160
    height = 160
    resized_img = img.resize((width, height), Image.ANTIALIAS)
    resized_img.save(input_img)
    images_from_video(input_video,input_img,x_coord,y_coord,width,height)

#function which extracts footage from the video
def images_from_video(input_video,input_img,x_coord,y_coord,width,height):
    vidcap = cv2.VideoCapture(input_video)
    success,image = vidcap.read()
    count = 1
    success = True
    failure = False
    while success:
        success,image = vidcap.read()
        print("Read a new frame: ", success)
        cv2.imwrite("Images/image{}.jpg".format(count), image)  # save frame as JPEG file
        count += 1
    count -= 1
    path = os.path.join(os.path.abspath(os.path.dirname(__file__)),"Images/image{}.jpg".format(count))
    os.remove(path)

    path, dirs, files = os.walk('Images').next()
    file_count = len(files)
    print(file_count)
    check_coordinate(input_img,x_coord,y_coord,width,height,count,file_count)

#function checking the location of the image
def check_coordinate(input_img,x_coord,y_coord,width,height,count,file_count):
    width_video, height_video = Image.open(open("Images/image{}.jpg".format(count - 1))).size
    if x_coord < 0:
        x_coord = 0
    if y_coord < 0:
        y_coord = 0
    if x_coord > width_video - width:
        x_coord = width_video - width
    if y_coord > height_video - height:
        y_coord = height_video - height
    images_with_wm(input_img,x_coord,y_coord,file_count)

#function image overlay on frames
def images_with_wm(input_img,x_coord,y_coord,file_count):
    count = 1
    while count < file_count + 1:
        ph = Image.open("Images/image{}.jpg".format(count)).convert("RGBA")
        wm = Image.open(input_img).convert("RGBA")
        ph.paste(wm, (x_coord ,y_coord), wm)
        ph.save("Images_with_wm/photo_watermark{}.png".format(count))
        count += 1
    print('The picture is placed on frames')
    assembly_and_removal(file_count)

#function assembling frames in video
def assembly_and_removal(file_count):
    p = subprocess.call("./ffmpeg_in_video")
    count = 1
    while count < file_count + 1:
      os.remove("Images/image{}.jpg".format(count))
      os.remove("Images_with_wm/photo_watermark{}.png".format(count))
      count += 1

data_comand()


