
import matplotlib.pyplot as plt
import skimage.io
import numpy as np
import matplotlib.pyplot as plt
import cv2
import os
import time
import time, os, fnmatch, shutil
import numpy as np
import pyfirmata 
import tkinter as tk
import h5py
import customtkinter
import subprocess

from math import ceil
from skimage import data
from skimage import io
from ctypes import *
from IPython.display import clear_output
from tkinter import *
from PIL import ImageTk, Image
from tifffile import imsave
from pypylon import pylon
from pypylon import genicam
from tkinter import messagebox
from tkinter import ttk
from tkinter.messagebox import *
from threading import Thread
from pyfirmata import Arduino, util, SERVO
from tkinter import filedialog
from  time  import  sleep

### DEFINE CAMERA FUNCTIONS

## Function for setting exposure time on the camera
def Exposure():

    a=float(scale3.get())           # Get exposure time from user
    camera.MaxNumBuffer = 2
    try:
        camera.Gain = camera.Gain.Max
    
    except genicam.LogicalErrorException:
        camera.GainRaw = camera.GainRaw.Max
         
    camera.Width = camera.Width.Max
    camera.Height = camera.Height.Max
    # camera.ExposureTime = camera.ExposureTime.Min
    camera.PixelFormat = "Mono12"
    camera.ExposureTime.SetValue(a) # Set exposure time
    II=Snap_BF() # Capture an image
    
    
    ## Resize and display captured image
    img2 = Image.fromarray(cv2.resize(II/200, dsize=(600,400), interpolation=cv2.INTER_CUBIC))
    img1 = ImageTk.PhotoImage(image=img2)
    lmain1 = Label(frame1,image=img1,height=400,width=600)
    lmain1.imgtk = img1    
    lmain1.configure(image=img1) 
    lmain1.grid(row=0,column=0,rowspan=4,columnspan=4)
    

## Function for setting exposure time on the camera (alternate implementation)    
def Exposure2():
    
    a=float(entry_exposurebf.get())
    camera.MaxNumBuffer = 2
    try:
        camera.Gain = camera.Gain.Max
    
    except genicam.LogicalErrorException:
          camera.GainRaw = camera.GainRaw.Max
    camera.Width = camera.Width.Max
    camera.Height = camera.Height.Max
    # camera.ExposureTime = camera.ExposureTime.Min
    camera.PixelFormat = "Mono12"
    camera.ExposureTime.SetValue(a)
    
## Function for setting illumination and updating the captured image
        
def SetIllumination1_BIS():    
    a=scale1.get()            # Get illumination percentage from the user
    percent2=a/100            # Rescale into percentage
    sortie1.write(percent2)   # Set level through arduino
    II=Snap_BF()              # Use the Snap function to take a picture
    
    ## Resize and display captured image
    img2 = Image.fromarray(cv2.resize(II/200, dsize=(600,400), interpolation=cv2.INTER_CUBIC))
    img1 = ImageTk.PhotoImage(image=img2)
    lmain1 = Label(frame1,image=img1,height=400,width=600)
    lmain1.imgtk = img1    
    lmain1.configure(image=img1) 
    lmain1.grid(row=0,column=0,rowspan=4,columnspan=4)       


        
def SetIllumination1_BISa(a):   
    percent2=a/100
    sortie1.write(percent2) 
    
## Function for capturing a brightfield image    
def Snap_BF():
    camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)    # Initiate grabbing images
    converter = pylon.ImageFormatConverter()                    # Image format converter
    # converting to opencv bgr format
    converter.OutputPixelFormat = pylon.PixelType_Mono16
    converter.OutputBitAlignment = pylon.OutputBitAlignment_MsbAligned
    grabResult = camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)    
    # Access the image data
    image = converter.Convert(grabResult)
    img = image.GetArray()        
    # Releasing the resource    
    camera.StopGrabbing()
    return img    


## Function for previewing live images from camera
def Preview():
    camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)    # Initiate grabbing images
    converter = pylon.ImageFormatConverter()
    converter.OutputPixelFormat = pylon.PixelType_Mono16
    converter.OutputBitAlignment = pylon.OutputBitAlignment_MsbAligned
    while camera.IsGrabbing():
        grabResult = camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)

        if grabResult.GrabSucceeded():
            image = converter.Convert(grabResult)
            img = image.GetArray()
            cv2.namedWindow('Preview', cv2.WINDOW_NORMAL)
            cv2.imshow('Preview', img)
            k = cv2.waitKey(1)
            # If ESC key is pressed, the preview window closes
            if k == 27 :
                break
        grabResult.Release()
       
    camera.StopGrabbing()
    cv2.destroyAllWindows()

## Function for previewing live images from camera in the Z-stack
def Preview_Zstack():  
    camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly) 
    converter = pylon.ImageFormatConverter()
    converter.OutputPixelFormat = pylon.PixelType_Mono16
    converter.OutputBitAlignment = pylon.OutputBitAlignment_MsbAligned
    while camera.IsGrabbing():
        grabResult = camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)

        if grabResult.GrabSucceeded():
            image = converter.Convert(grabResult)
            img = image.GetArray()
            cv2.namedWindow('Preview', cv2.WINDOW_NORMAL)
            cv2.imshow('Preview', img)
        grabResult.Release()   
        camera.StopGrabbing()
  
## Function for recording video   
def Video():
        k = int(scale4.get())
        camera.StopGrabbing()
        camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly) 
        converter = pylon.ImageFormatConverter()
        converter.OutputPixelFormat = pylon.PixelType_Mono16
        converter.OutputBitAlignment = pylon.OutputBitAlignment_MsbAligned
        vivi=np.zeros([k,915,1371],'uint16')
        file_name1 = entry_filenamevideo.get()
        file_path1 = entry_directoryvideo.get()
        t2 = time.localtime()
        a=float(scale3.get())
        d = camera.ResultingFrameRate.GetValue()
        timestamp2 = time.strftime('%Y%m%d%H%M', t2)
        os.mkdir(file_path1 + '\\' + file_name1)
        f = open(file_path1 + '\\' + file_name1 + "\\meta_data.txt", "w")
        f.write("File name : " + file_name1 + "\nFile extension : .tif\nDate : " + timestamp2 + "\nImage size : 1371x915\nPixel deph : 16-bit\nExposure : " + str(a) + "ms\nFPS : " + str(d) + "\nPixel = 0.5 µm")
        f.close()
        for ii in range(k):
            grabResult = camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)

            if grabResult.GrabSucceeded():
                image = converter.Convert(grabResult)
                img = image.GetArray()
                vivi[ii,:,:]=(cv2.resize(img, dsize=(1371,915), interpolation=cv2.INTER_CUBIC))
            grabResult.Release()       
        camera.StopGrabbing()
        file_name1 = entry_filenamevideo.get()
        file_path1 = entry_directoryvideo.get()
        total=os.path.join(file_path1 + '\\' + file_name1, file_name1 +'.tif')
        imsave(total, vivi)
    
## Function to save a snapshot
def Save_snapshot():
    II=Snap_BF()
    img1 = Image.fromarray(cv2.resize(II/100, dsize=(600,400), interpolation=cv2.INTER_CUBIC))
    img1=np.asanyarray(img1)
    
    # Get the file name and path from the input
    file_name = entry_filename1.get()
    file_path = entry_directory1.get()
    suffix = '.tif'
    total=os.path.join(file_path, file_name +'1' + suffix)
    imsave(total,img1)
    
progress_counter=0  #Initialize counter


## Function to capture images  
def capture():

    # global endAngle
    global progress_counter
    
    SetIllumination1_BISa(100)
    Exposure2()
    time.sleep(0.2)
    II1=Snap_BF()
    time.sleep(0.2)
    SetIllumination1_BISa(0) 
    time.sleep(0.2)   
    
    # Get the current timestamp
    t = time.localtime()
    timestamp = time.strftime('%Y%m%d%H%M_', t)
    img1 = Image.fromarray(cv2.resize(II1, dsize=(5472,3672), interpolation=cv2.INTER_CUBIC))
    img1=np.asanyarray(img1)
    # Get the file name and path 
    file_name1 = entry_filename1.get()
    file_path1 = entry_directory1.get()
    suffix = '.tif'
    total1=os.path.join(file_path1 + '\\' + file_name1 + '\\BF', timestamp +'_' + str(endAngle)+'_'+ file_name1 + 
                        '-BF ' + suffix)
    # Save the image
    imsave(total1,img1)
    print('file')
    print(timestamp+'-BF ' + str(endAngle)+suffix)

    # Update the progress counter and progress bar
    progress_counter+=1
    my_progress['value']=np.ceil(progress_counter/w*100)
    Text_box_sleep.config(text="Completed: "+str( np.ceil(progress_counter/w*100) )+"%. "+"Waiting for next step ",bg='yellow',fg='black')
    root.update()
    
    
## Function to capture a stack of images  
def capture_image_stack():
    global endAngle
    global step
    
    step=int ( current_value.get() )  # Get step size from user input
    file_name1 = entry_filename1.get()
    file_path1 = entry_directory1.get()

    endAngle=startZ
    lim=stopZ
       
    while time.time() < t_end:
        endAngle=startZ
        lim=stopZ
        carte . digital [ pin ].write( startZ )  # Move to startZ position 
        sleep (int ( Pause.get() ))

        pb['value']=0  # Reset progress bar
        displaypos()
        root.update()
        
        while endAngle<lim:
            Text_box_sleep.config(text="Acquiring stack",bg='white',fg='red')
            capture()
            endAngle += step
            
            if endAngle>180 or endAngle==lim:
                endAngle=lim
                carte . digital [ pin ].write( endAngle )  # Move to endAngle position
                sleep (int ( Pause.get() ))                # Wait for the pause duration
                displaypos()
                pb['value']=abs((endAngle)/(stopZ-startZ))*100  # Update progress bar
                root.update()
                
                capture()                                  # Capture the final image in the stack
                break
    
            carte.digital [ pin ].write( endAngle )
            displaypos()
            pb['value']=abs((endAngle)/(stopZ-startZ))*100
            root.update()
            
            sleep (int ( Pause.get()))    
                    
        sleep(a1)  # Wait for the interval between stacks
        
    root.update()  # update the visual interface
    

    
## Function to acquire images during a time-based acquisition    
def Imagetime():
    global t_end
    global a1
    global w
   
    a=int(entry_timeperhour.get())   # Get the time step from user
    a1 = 60 * a                      # Convert time step to minutes
    n = int(entry_time.get())        # Get the total duration from input
    t_end = time.time() + 3600 * n   # Calculate the end time (3600*n: 'n' is in hours)
    
    expbf=float(entry_exposurebf.get())  # Exposure from user information
    
    # Get the current timestamps 
    t2 = time.localtime()
    timestamp2 = time.strftime('%Y%m%d%H%M', t2)
    t1 = time.localtime()
    timestamp1 = time.strftime('%Y%m%d%H%M', t1)
    
    # Get the file name and path 
    file_name1 = entry_filename1.get()
    file_path1 = entry_directory1.get()
          
    if var1.get()==1: # Validation variable for Z-stack and time stack
        global stopZ, startZ, step, endAngle, lim
        
        step=int ( current_value.get() )                       # Get the step size from user input
        w=((n * 3600)/(a * 60))* (abs((stopZ-startZ))/step+1)  # Calculate the total number of images
        i=(w* 93245) * 10**(-6)                                # Calculate the total data size

        # Ask user confirmation before proceeding
        rep = askokcancel ("Incubascope - Alert", "You will take " + str(w) +
                   " pictures for a total of " + str(i) + " GB with a Z-STACK. Would you like to continue")
                      
        if rep == 1:  
            os.mkdir(file_path1 + '\\' + file_name1)
            os.mkdir(file_path1 + '\\' + file_name1 + '\\BF')
            
            # Save metadata to a text file
            f = open(file_path1 + '\\' + file_name1 + "\\meta_data.txt", "w")
            f.write("File name : " + file_name1 + "\nFile extension : .tif\nStart date : " + timestamp2 + 
                    "\nAcquisition Duration (hrs):" + str(n)
                     + "\nImage size : 5472x3672\nPixel deph : 16-bit \nExposure BF : " + str(expbf) + 
                    "ms" + "\nTime step : " + str(a1/60) + " min\nImage Pixel (um)= Camera pixel (2.4um) / (Obj Mag) x (180mm/100mm) " #+str(2.4*1.8/float(menu.get()))
                    +"\nObjc used: "+(menu.get())
                    +"\nZ-stack_start (um): "+ str(startZ*2)+"\nZ-stack_stop (um): "+str(stopZ*2)+"\nstep_size (um): "+str(step*2))

    
            f.close()
            
            capture_image_stack()

            t1 = time.localtime()
            timestamp1 = time.strftime('%Y%m%d%H%M', t1)
            f = open(file_path1 + '\\' + file_name1 + "\\meta_data.txt", "w")
            f.write("File name : " + file_name1 + "\nFile extension : .tif\nStart date : " + timestamp2 + "\nAcquisition Duration (hrs):" + str(n)+
                    "\nEnd date : " + timestamp1 + "\nImage size : 5472x3672\nPixel deph : 32-bit\nExposure BF : " +
                    str(expbf) + "ms" + "\nTime step : "+  str(a1/60) + " min\nImage Pixel (um)= Camera pixel (2.4um) / (Obj Mag) x (180mm/100mm) " #+str(2.4*1.8/float(menu.get()))
                    +"\nObjc used: "+(menu.get())
                    +"\nZ-stack_start (um): "+ str(startZ*2)+"\nZ-stack_stop (um): "+str(stopZ*2)+"\nstep_size (um): "+str(step*2))
            f.close()

            my_progress.stop()   # Stop the progress bar
            messagebox.showinfo("Incubascope - Alert", "Acquisition completed")
            Text_box_sleep.config(text="Acquistion Complete; End time: "+str(timestamp1))   
            root.update()  




    else:   # Perform only a time-stack
        w = ((n * 3600)/(a * 60))
        i = (w * 93245) * 10**(-6)
    
        expbf=float(entry_exposurebf.get())
        
        # Ask user confirmation before proceeding
        rep = askokcancel ("Incubascope - Alert", "You will take " + str(w) + " pictures for a total of " + 
                         str(i) + " GB. Would you like to  continue")
        
        
        if rep == 1:
        
            os.mkdir(file_path1 + '\\' + file_name1)
            os.mkdir(file_path1 + '\\' + file_name1 + '\\BF')
            f = open(file_path1 + '\\' + file_name1 + "\\meta_data.txt", "w")
            f.write("File name : " + file_name1 + "\nFile extension : .tif\nStart date : " + 
                    timestamp2 + "\nAcquisition Duration (hrs):" + str(n) +"\nImage size : 5472x3672\nPixel deph : 16-bit \nExposure BF : " + str(expbf) + 
                    "ms" + "\nTime step : " + str(a1/60) + " min\nImage Pixel (um)= Camera pixel (2.4um) / (Obj Mag) x (180mm/100mm) " #+str(2.4*1.8/float(menu.get()))
                    +"\nObjc used: " + str(menu.get()))
            f.close()
        
            while time.time() < t_end:

                capture()

                time.sleep(a1)  # Wait for the time-stack interval 
                
                
            t1 = time.localtime()
            timestamp1 = time.strftime('%Y%m%d%H%M', t1)
            f = open(file_path1 + '\\' + file_name1 + "\\meta_data.txt", "w")
            f.write("File name : " + file_name1 + "\nFile extension : .tif\nStart date : " 
                    + timestamp2 + "\nAcquisition Duration (hrs):" + str(n) + "\nEnd date : " + timestamp1 + "\nImage size : 5472x3672\nPixel deph : 32-bit\nExposure BF : " + str(expbf) +
                     "ms" +  "\nTime step : " + str(a1/60) + " min\nImage Pixel (um)= Camera pixel (2.4um) / (Obj Mag) x (180mm/100mm) " #+str(2.4*1.8/float(menu.get()))
                     +"\nObjc used: " + str(menu.get()))
            f.close()
            
            my_progress.stop() # Stop the progress bar
            messagebox.showinfo("Incubascope - Alert", "Acquisition completed")
            Text_box_sleep.config(text="Acquistion Complete; End time: "+str(timestamp1))   
            root.update()  
          

def Start():
    mon_thread.start()
    
def Start1():
    mon_thread1.start()

#### Z_stack window and control of the motor


# Function to rotate counter-clockwise           
def  RotateCCW ():
   
    global endAngle
    global startZ
    global stopZ

    # Step size from user 
    step=int ( current_value.get() )
    endAngle = endAngle+step
    
    if endAngle>=180:
        endAngle=180
        
    carte.digital[pin].write( endAngle )
    sleep (0.01)


    if var_preview.get()==1:
       Preview_Zstack()        # Preview Z-stack if enabled (box is ticked)
    
    
def  RotateCW ():
    
    global endAngle
    global startZ
    global stopZ

    # Step size from user 
    step=int ( current_value.get ( ) )
    endAngle = endAngle-step
    
    if endAngle<=0:
        endAngle=0
        
    carte.digital[pin].write( endAngle )
    sleep (0.01)
    
    if var_preview.get()==1:
       Preview_Zstack()   # Preview Z-stack if enabled (box is ticked)
    
# Function to display the current position  
def  displaypos ():
    labelpos.config(text=endAngle)
    labelpos_Zstack.config(text=endAngle)
    
# Function to set the start position for Z-stack  
def  Zstartpos ():
    global startZ
    startZ=endAngle
    labelZstart.config(text=startZ,bg='green',fg='white')
  
# Function to set the stop position for Z-stack    
def  Zstoppos ():
    global stopZ
    stopZ=endAngle
    labelZstop.config(text=stopZ,bg='green',fg='white')
    pb["length"]=180       # Set Z-stack progress bar length
    Text_box_sleep.config(text="Parameters set: Tick the Capture box for stack",bg='orange',fg='white')
    num_slices_Zstack.config(text=str(ceil(abs(int(stopZ)-int(startZ))/int ( current_value.get ( ) ))))

# Function to define the number of slices in the Z-stack
def  tick ():
     num_slices_Zstack.config(text=str(1+ceil(abs(int(stopZ)-int(startZ))/int ( current_value.get ( ) ))))
     button_stepok.config(bg='seagreen',fg='white')
   

# the main function
def main():
    # Global variables declaration for use in the functions defined above
    global camera
    global mon_thread1, mon_thread
    global scale1, scale3, scale4 
    global sortie1, sortie2
    global frame0, frame1
    #global entry_filename
    global entry_directoryvideo, entry_filename1, entry_filenamevideo, entry_directory1
    #global entry_directory
    global entry_timeperhour, entry_time, entry_exposurebf
    global my_progress
    global cmb
    global carte, pin, sb, current_value
    global labelpos, button_stepok
    global labelZstart, labelZstop, ZstopBtn, labelpos_Zstack
    global ZstopBtn, var1, var2, SweepBtnCCW, SweepBtnCW, num_slices_Zstack
    global Pause, pb
    global endAngle, root, Text_box_sleep
    global var_preview
    global progess_counter, menu
   
    # Camera initialization
    camera = pylon.InstantCamera(
    pylon.TlFactory.GetInstance().CreateFirstDevice())
    camera.Open()
    camera.MaxNumBuffer = 2
    camera.Width = camera.Width.Max
    camera.Height = camera.Height.Max
    # camera.ExposureTime = camera.ExposureTime.Min
    camera.PixelFormat = "Mono12"
    camera.ExposureTime.SetValue(20)
    
    #Arduino initialization
    carte = Arduino('COM17')
    sortie1 = carte.get_pin('d:3:p')
    pin=10
    carte.digital[pin].mode=SERVO
   
    # Tkinter root window initialization
    root = Tk()
    root.resizable(True, True)
    root.title('zIncubascope - Software')
    root.geometry("1700x750")
    root.configure(background='gray32')

    notebook = ttk.Notebook(root)
    notebook.grid(row=1, column=0)
    frame11 = Frame(root, width=1450, height=750, background="gray32")
    frame22 = Frame(root, width=1450, height=750, background="gray32")
    
    v = DoubleVar()  
    y = DoubleVar()
    f = DoubleVar()
    p = DoubleVar()
    II = Snap_BF()
    endAngle=0
    
    # Threading for image acquisition and preview
    mon_thread=Thread(target=Imagetime)
    mon_thread1=Thread(target=Preview)
    
    # Frame for the main title and logo
    frame0 = Frame(root, width=1450, height=80, background="gray32")
    Title=Label(frame0, text='INCUBASCOPE 2.0 - Acquisition software', background="gray32")
    Title.config(font=('Arial', 18))
    Title.grid(column=0, row=0, rowspan=1, columnspan=1)
    test0 = Image.open('C:\\Users\\BiOf\\logo1.jpg')
    test0=test0.resize((150, 70), Image.ANTIALIAS)
    photo0 = ImageTk.PhotoImage(test0)
    label0 = Label(frame0,image=photo0,height=70,width=150)
    label0.image = photo0
    label0.grid(column=1,row=0,columnspan=3)
    frame0.grid(row=0, column=0, rowspan=1, columnspan=6)

    # Frame for image preview and controls
    frame1 = Frame(frame11, width=1000, height=670, background="gray32")
    img2 = Image.fromarray(cv2.resize(II/200, dsize=(600,400), interpolation=cv2.INTER_CUBIC))
    img1 = ImageTk.PhotoImage(image=img2)
    lmain1 = Label(frame1,image=img1,height=400,width=600)
    lmain1.imgtk = img1    
    lmain1.configure(image=img1) 
    lmain1.grid(row=0,column=0,rowspan=4,columnspan=4)

    button_start1 = Button(frame1, text='Start preview', bg='Seagreen1', height=3, width=20, command = Preview)
    button_start1.grid(row=0, column=6, columnspan=3)

    scale1 = Scale( frame1, variable = v, from_ = 0, to = 100, orient = VERTICAL, resolution=20, tickinterval=20, length=150,label='BF')
    scale1.grid(row=2, column=6, columnspan=2)
    scale3 = Spinbox(frame1, from_=20, to=100000)
    scale3.grid(row=5, column=1, columnspan=2)

    text_exposure = Label(frame1, text='Exposure (ms)', height=2, width=10,background="gray32", foreground='white')
    text_exposure.grid(row=5, column=0, columnspan=2)
    text_imagevideo = Label(frame1, text=' Number of Images', height=2, width=20,background="gray32", foreground='white')
    text_imagevideo.grid(row=6, column=0, columnspan=2)
    text_imagevideopath = Label(frame1, text='Directory path', height=2, width=10,background="gray32", foreground='white')
    text_imagevideopath.grid(row=7, column=0, columnspan=2)
    text_imagevideoname = Label(frame1, text='File name', height=2, width=10,background="gray32", foreground='white')
    text_imagevideoname.grid(row=8, column=0, columnspan=2)

    scale4 = Spinbox(frame1, from_=1, to=100000)
    scale4.grid(row=6, column=1, columnspan=2)
    button_video = Button(frame1, text='Start video',bg='Seagreen2', height=2, width=10, command = Video)
    button_video.grid(row=7, column=2, columnspan=5)
    entry_directoryvideo = Entry(frame1)
    entry_directoryvideo.insert(10,"C:/Users/Admin")
    entry_directoryvideo.grid(row=7, column=1, columnspan=2)
    entry_filenamevideo = Entry(frame1)
    entry_filenamevideo.insert(10,"default")
    entry_filenamevideo.grid(row=8, column=1, columnspan=2)
    
    button_illumination2 = Button(frame1, text='Confirm BF',bg='tomato2', height=2, width=8, command = SetIllumination1_BIS)
    button_illumination2.grid(row=3, column=6)
    button_exposure = Button(frame1, text='Confirm XP',bg='light blue', height=2, width=8, command = Exposure)
    button_exposure.grid(row=5, column=2, columnspan=5)


    frame1.grid(row=2, column=0, rowspan= 1, columnspan=1)
    
    frame2 = Frame(frame11, width=450, height=670, background="gray32")
    text_directory0 = Label(frame2, text='', height=2, width=15,background="gray32", foreground='white')
    text_directory0.grid(row=1, column=1)
    text_directory = Label(frame2, text='Directory path', height=2, width=15,background="gray32", foreground='white')
    text_directory.grid(row=1, column=2)
    text_filename = Label(frame2, text='File name', height=2, width=15,background="gray32", foreground='white')
    text_filename.grid(row=2, column=2)
    text_time1 = Label(frame2, text='Time step (min)', height=2, width=15,background="gray32", foreground='white')
    text_time1.grid(row=3, column=2)
    text_time2 = Label(frame2, text='Time span (hour)', height=2, width=15,background="gray32", foreground='white')
    text_time2.grid(row=4, column=2)
    text_time2 = Label(frame2, text='Exposure BF (ms)', height=2, width=15,background="gray32", foreground='white')
    text_time2.grid(row=6, column=2)

    button_snap = Button(frame2, text='Save snapshot',bg='Seagreen2', height=2, width=10, command = Save_snapshot)
    button_snap.grid(row=0, column=2,columnspan=1)


    entry_directory1 = Entry(frame2)
    entry_directory1.insert(10,"C:/Users/Admin/Documents")
    entry_directory1.grid(row=1, column=3)
    entry_filename1 = Entry(frame2)
    entry_filename1.insert(10,"default")
    entry_filename1.grid(row=2, column=3)


    entry_timeperhour = Spinbox(frame2, from_=1, to=100000)
    entry_timeperhour.grid(row=3, column=3)
    entry_time = Spinbox(frame2, from_=1, to=100000)
    entry_time.grid(row=4, column=3)
    entry_exposurebf = Spinbox(frame2, from_=20, to=100000)
    entry_exposurebf.grid(row=6, column=3)

    menu=StringVar()
    menu.set("Objective Mag")
    text_OBJ = Label(frame2, text='Select Objective (X)', height=2, width=15,background="gray32", foreground='white')
    text_OBJ.grid(row=8, column=2)
    Obj_drop=OptionMenu(frame2,menu,"2X","4X","10X","20X")
    Obj_drop.grid(row=8, column=3,columnspan=1)

    button_snap1 = Button(frame2, text='Launch Acquisition',font=('Helvetica Bold',14),bg='seagreen2', fg='black',height=2, width=20, command = Start)
    button_snap1.grid(row=15, column=1,columnspan=3,rowspan=1, pady=10)


    frame2.grid(row=2, column=1, rowspan= 8, columnspan=4)
    frame11.grid(row=0, column=0, columnspan=8)


    selection = ('Full', '2', '3', '4', '10')
    selected = tk.StringVar()
    cmb = ttk.Combobox(frame22, textvariable=selected)
    cmb['values'] = selection
    cmb.current(0)
    cmb.grid(row=2, column=1)
    
    frame22.grid(row=0, column=0)
    notebook.add(frame11, text='Software')
             
   # Frame for z-stack controls
    frame_zstack=Frame(root,width=400, height=450)
    frame_zstack.grid(row=0, column=8, columnspan=7, rowspan=12)
    
    # Buttons for moving in Z
    CCWBtn = tk . Button ( frame_zstack , width=5, bd = 5 , bg = '#89CFF0' , text = "UP" , command= lambda:[RotateCCW(),displaypos()]  )
    CCWBtn . grid ( column = 4 , row = 1, pady=10 )
    CWBtn = tk . Button ( frame_zstack , width=5, bd = 5 , bg = '#89CFF0' , text = "DOWN" ,command= lambda:[RotateCW(),displaypos()]  )    
    CWBtn . grid ( column = 4 , row = 2, pady=10)

    current_value = tk.StringVar(value=1)

    # Label for current position and step during moving
    sb = tk.Spinbox(frame_zstack ,textvariable=current_value, width=5,from_=1,to=100)
    sb.grid(row=1,column=2,padx=0, columnspan=1)
    sb_label = tk.Label(frame_zstack, text ='Step Size', fg="navyblue",font=('Helvetica Bold',11)) 
    sb_label. grid ( row=1,column=1,padx=0)

    labelpos=tk.Label(frame_zstack,text='0',bg='white',fg='black',font=('Helvetica Bold',11), width=5)
    labelpos. grid ( column = 2, row = 2 )
    pos_label = tk.Label(frame_zstack, text ='Position', fg="blue",width=10,font=('Helvetica Bold',11)) 
    pos_label. grid ( row=2 ,column=1,padx=0,pady=2)
    
    # Checkbox for preview option
    var_preview = tk.IntVar()
    ch_pr = tk.Checkbutton(frame_zstack, text='Preview',variable=var_preview, onvalue=1, offvalue=0,font=('Helvetica Bold',11))
    ch_pr.grid(column=2,row=3,columnspan=2, pady=5)

    # Scale for pause duration
    Pause = tk . Scale ( frame_zstack , bd = 5 , from_ = 2 , to = 10 , resolution=1 , orient = tk.HORIZONTAL )
    Pause . grid ( column = 1 , row = 5, columnspan=3)
    
    tk . Label ( frame_zstack , text = "Pause (2s to 10s)" ). grid ( column = 1 , row = 6, columnspan=2 )
    
    # Buttons for setting Z-start and Z-stop positions
    ZstartBtn = tk . Button ( frame_zstack , bd = 5 ,width=8, bg = '#89CFF0' , text = "Z-start" ,font=('Helvetica Bold',13), command= lambda:[Zstartpos()]   )
    ZstartBtn . grid ( column =8 , row = 5)
 
    labelZstart=tk.Label(frame_zstack,text='0',width=5,bg='gold',fg='blue',font=('Helvetica Bold',13))
    labelZstart. grid ( column = 9, row =5 )

    ZstopBtn = tk . Button ( frame_zstack , bd = 5 , width=8, bg = '#89CFF0' , text = "Z-stop" ,font=('Helvetica Bold',13), command= lambda:[Zstoppos()]  )
    ZstopBtn . grid ( column =8 , row = 1)

    labelZstop=tk.Label(frame_zstack,text='0',width=5, bg='gold',fg='blue',font=('Helvetica Bold',13))
    labelZstop. grid ( column = 9, row =1  )
    
    # Label for the current Z-stack position
    labelpos_Zstack=tk.Label(frame_zstack,text='0',width=5,bg='white',fg="black",font=('Helvetica Bold',10))
    labelpos_Zstack. grid ( column = 9, row =2 , pady=10 )
    labelpos_Zstack_label = tk.Label(frame_zstack, text ='Current position', fg="black",font=('Helvetica Bold',10)) 
    labelpos_Zstack_label. grid ( row=2,column=8,pady=10, padx=10)

    sb = tk.Spinbox(frame_zstack ,textvariable=current_value, width=4,from_=0,to=180,font=('Helvetica Bold',13))
    sb.grid(row=3,column=9,padx=2,pady=10)
    
    # Button for setting the step size
    button_stepok = Button(frame_zstack, bd = 5 , width=8, bg = '#89CFF0', text = 'Step Size', fg="black",font=('Helvetica Bold',13), command = tick)
    button_stepok. grid ( row=3,column=8,padx=2,pady=10)

    #Label to display the number of slices in Z-stack
    num_slices_Zstack=tk.Label(frame_zstack,text='0',width=5,bg='white',fg="black",font=('Helvetica Bold',10))
    num_slices_Zstack. grid ( column = 9, row =4 , pady=10 )
    num_slices_Zstack_label = tk.Label(frame_zstack, text ='Stack Size', fg="black",font=('Helvetica Bold',10)) 
    num_slices_Zstack_label. grid ( row=4,column=8,pady=10, padx=10)

    # Checkbox to capture Z-stack
    var1 = tk.IntVar()
    c1 = tk.Checkbutton(frame_zstack, text='Tick to capture Z-stack',font=('Helvetica Bold',15),variable=var1, onvalue=1, offvalue=0)
    c1.grid(column=2,row=8, columnspan=8, padx=5, pady=8)
  
    # Progress bar for Z-stack progress
    pb = ttk.Progressbar(frame_zstack, orient='vertical',    mode='determinate',    length=200)
    pb.grid(column=11, row=1, rowspan=6, columnspan=1, padx=10, pady=0)

    pb_label=tk.Label(frame_zstack,text='Stack Progress',width=10,fg='blue', bg='white')
    pb_label.grid(column=11, row=6, columnspan=4)

    Text_box_sleep = tk.Label(frame_zstack, text='Select Z-stack parameters', width = 52, font=('Helvetica Bold',16),bg='orange')
    Text_box_sleep.grid(row=10, column=1, columnspan=20, pady=20)

    my_progress = ttk.Progressbar(frame_zstack, orient=HORIZONTAL, length=350, mode = "determinate")
    my_progress.grid(row=12, column=1, columnspan=20, pady=20)

    root.mainloop()

if __name__ == "__main__":
    main()
