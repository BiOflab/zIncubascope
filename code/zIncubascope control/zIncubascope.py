

from skimage import data
import matplotlib.pyplot as plt
import skimage.io
from skimage import io
from ctypes import *
import numpy as np
import matplotlib.pyplot as plt
from IPython.display import clear_output
from tkinter import *
from PIL import ImageTk, Image
import cv2
from tifffile import imsave
import os
import time
from pypylon import pylon
import time, os, fnmatch, shutil
import numpy as np
from pypylon import genicam
import pyfirmata 
from tkinter import messagebox
from tkinter import ttk
import tkinter as tk
from tkinter.messagebox import *
import h5py
from threading import Thread



from pyfirmata import Arduino, util, SERVO
from tkinter import filedialog
import subprocess
from  time  import  sleep

#define camera functions   
def Exposure():

    a=float(scale3.get())
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
    II=Snap_BF()
    img2 = Image.fromarray(cv2.resize(II/200, dsize=(600,400), interpolation=cv2.INTER_CUBIC))
    img1 = ImageTk.PhotoImage(image=img2)
    lmain1 = Label(frame1,image=img1,height=400,width=600)
    lmain1.imgtk = img1    
    lmain1.configure(image=img1) 
    lmain1.grid(row=0,column=0,rowspan=4,columnspan=4)
    

    
def Exposure2():
    # Print the model name of the camera.
    #print("Using device ", camera.GetDeviceInfo().GetModelName())
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
    
        
def SetIllumination1_BIS():    
    a=scale1.get()
    percent2=a/100
    sortie1.write(percent2)   
    II=Snap_BF()
    img2 = Image.fromarray(cv2.resize(II/200, dsize=(600,400), interpolation=cv2.INTER_CUBIC))
    img1 = ImageTk.PhotoImage(image=img2)
    lmain1 = Label(frame1,image=img1,height=400,width=600)
    lmain1.imgtk = img1    
    lmain1.configure(image=img1) 
    lmain1.grid(row=0,column=0,rowspan=4,columnspan=4)       


        
def SetIllumination1_BISa(a):   
    percent2=a/100
    sortie1.write(percent2) 
    
def Snap_BF():
    camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly) 
    converter = pylon.ImageFormatConverter()
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

def Preview():
    camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly) 
    converter = pylon.ImageFormatConverter()

    converter.OutputPixelFormat = pylon.PixelType_Mono16
    converter.OutputBitAlignment = pylon.OutputBitAlignment_MsbAligned

    while camera.IsGrabbing():
        grabResult = camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)

        if grabResult.GrabSucceeded():
            image = converter.Convert(grabResult)
            img = image.GetArray()
            #img = cv2.flip(img, 0)
            #img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
            cv2.namedWindow('Preview', cv2.WINDOW_NORMAL)
            cv2.imshow('Preview', img)
            k = cv2.waitKey(1)
            if k == 27 :
                break
        grabResult.Release()
       
    camera.StopGrabbing()
    cv2.destroyAllWindows()


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
            #img = cv2.flip(img, 0)
            #img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
            cv2.namedWindow('Preview', cv2.WINDOW_NORMAL)
            cv2.imshow('Preview', img)
            cv2.waitKey(1)

        grabResult.Release()   
        camera.StopGrabbing()





            
       
       
    #camera.StopGrabbing()
    #cv2.destroyAllWindows()    
    

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
    

def Save_snapshot():
    II=Snap_BF()
    img1 = Image.fromarray(cv2.resize(II/100, dsize=(600,400), interpolation=cv2.INTER_CUBIC))
    img1=np.asanyarray(img1)
    file_name = entry_filename1.get()
    file_path = entry_directory1.get()
    suffix = '.tif'
    total=os.path.join(file_path, file_name +'1' + suffix)
    imsave(total,img1)
    
progress_counter=0
    
def capture():

    global endAngle
    global progress_counter
    
    SetIllumination1_BISa(100)
    Exposure2()
    time.sleep(0.2)
    II1=Snap_BF()
    time.sleep(0.2)
    SetIllumination1_BISa(0) 
    time.sleep(0.2)     
      
    t = time.localtime()
    timestamp = time.strftime('%Y%m%d%H%M_', t)
    img1 = Image.fromarray(cv2.resize(II1, dsize=(5472,3672), interpolation=cv2.INTER_CUBIC))
    img1=np.asanyarray(img1)
    file_name1 = entry_filename1.get()
    file_path1 = entry_directory1.get()
    suffix = '.tif'
    total1=os.path.join(file_path1 + '\\' + file_name1 + '\\BF', timestamp +'_' + str(endAngle)+'_'+ file_name1 + 
                        '-BF ' + suffix)
    imsave(total1,img1)
    print('file')
    # print(t_end)
    # my_progress['value'] += (barpro)*100
    print(timestamp+'-BF ' + str(endAngle)+suffix)

    progress_counter+=1
    my_progress['value']=np.ceil(progress_counter/w*100)

    Text_box_sleep.config(text="Completed: "+str( np.ceil(progress_counter/w*100) )+"%. "+"Waiting for next step ",bg='yellow',fg='black')
    root.update()
    
    
    
def capture_image_stack():
    
    global endAngle
    global step
    step=int ( current_value.get() )
    file_name1 = entry_filename1.get()
    file_path1 = entry_directory1.get()

    endAngle=startZ
    lim=stopZ
       
    while time.time() < t_end:

        endAngle=startZ
        lim=stopZ
        carte . digital [ pin ].write( startZ )   
        sleep (int ( Pause.get() ))

        pb['value']=0
        displaypos()
        root.update()
        
        
        
        while endAngle<lim:

            Text_box_sleep.config(text="Acquiring stack",bg='white',fg='red')
                        
            capture()
            
            endAngle = endAngle+step
            
     
            if endAngle>180 or endAngle==lim:
                endAngle=lim
                carte . digital [ pin ].write( endAngle )
                sleep (int ( Pause.get() ))
                displaypos()
                pb['value']=abs((endAngle)/(stopZ-startZ))*100
                root.update()
                
                capture()
                break
    
            carte . digital [ pin ].write( endAngle )
            
            displaypos()
            pb['value']=abs((endAngle)/(stopZ-startZ))*100
            root.update()
            
            sleep (int ( Pause.get() ))
            
       
        
        
        
        sleep(a1)
        
  
    root.update()  
    

    
    
def Imagetime():
    
    global t_end
    global a1
    global w
    #ob=menu.get()
    #ob=ob[0]
    
    a=int(entry_timeperhour.get())
    a1 = 60 * a
    n = int(entry_time.get())
    t_end = time.time() + 3600 * n ## time duration in hours if it is 3600*n
    
    expbf=float(entry_exposurebf.get())
    
    t2 = time.localtime()
    timestamp2 = time.strftime('%Y%m%d%H%M', t2)
    t1 = time.localtime()
    timestamp1 = time.strftime('%Y%m%d%H%M', t1)
    
    
    file_name1 = entry_filename1.get()
    file_path1 = entry_directory1.get()
      
   
    
    if var1.get()==1:
        
        global stopZ, startZ, step, endAngle, lim
        
        step=int ( current_value.get() )

        w=((n * 3600)/(a * 60))* (abs((stopZ-startZ))/step+1)
        i=(w* 93245) * 10**(-6)

    

        rep = askokcancel ("Incubascope - Alert", "You will take " + str(w) +
                   " pictures for a total of " + str(i) + " GB with a Z-STACK. Would you like to continue")
        
        
        
        if rep == 1:
                
            
           
            
            
            os.mkdir(file_path1 + '\\' + file_name1)
            os.mkdir(file_path1 + '\\' + file_name1 + '\\BF')
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

            my_progress.stop()
            messagebox.showinfo("Incubascope - Alert", "Acquisition completed")
            Text_box_sleep.config(text="Acquistion Complete; End time: "+str(timestamp1))   
            root.update()  




    else:
        w = ((n * 3600)/(a * 60))
        i = (w * 93245) * 10**(-6)
    
        expbf=float(entry_exposurebf.get())
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

                time.sleep(a1)
                
                
            t1 = time.localtime()
            timestamp1 = time.strftime('%Y%m%d%H%M', t1)
            f = open(file_path1 + '\\' + file_name1 + "\\meta_data.txt", "w")
            f.write("File name : " + file_name1 + "\nFile extension : .tif\nStart date : " 
                    + timestamp2 + "\nAcquisition Duration (hrs):" + str(n) + "\nEnd date : " + timestamp1 + "\nImage size : 5472x3672\nPixel deph : 32-bit\nExposure BF : " + str(expbf) +
                     "ms" +  "\nTime step : " + str(a1/60) + " min\nImage Pixel (um)= Camera pixel (2.4um) / (Obj Mag) x (180mm/100mm) " #+str(2.4*1.8/float(menu.get()))
                     +"\nObjc used: " + str(menu.get()))
            f.close()
            my_progress.stop()

            messagebox.showinfo("Incubascope - Alert", "Acquisition completed")
            Text_box_sleep.config(text="Acquistion Complete; End time: ")   
            root.update()  
          
            
    
        
def Start():
    mon_thread.start()
    
def Start1():
    mon_thread1.start()

################## Z_stack window ##############





def  SweepCCW ():
            
    global endAngle
    global startZ
    global stopZ
    global lim
    
    pb['value']=0
    lim=0
    
    
    step=int ( current_value.get() )
    displaypos ()
  
    if var2.get()==1:
       endAngle=startZ
       lim= stopZ
       carte . digital [ pin ].write( endAngle )
       displaypos()
       
       root.update()
    
    while endAngle<180:
        
        if step==0:
            break
        
     #if var1.get()==1:
       #capture()
            
        sleep (int ( Pause.get() ))
        endAngle = endAngle+step
     
        if endAngle>lim:
            endAngle=lim
            carte . digital [ pin ].write( endAngle )
            displaypos()
            root.update()
            break

        carte . digital [ pin ].write( endAngle )
        displaypos()
        pb['value']+=step
        root.update()  
     
    
    

def  SweepCW ():   
        
    global endAngle
    global startZ
    global stopZ
   
    step=int ( current_value.get() )
    displaypos ()
    
    if var2.get()==1:
       endAngle=stopZ
       lim=startZ
       carte . digital [ pin ].write( endAngle )
       displaypos()
       pb['value']=0
       root.update()
    
    while endAngle>0:
    
        
     if step==0: # to prevent infinite loop
        break
    
     
     #if var1.get()==1:
       #capture()
            
     sleep(int ( Pause.get() ))
     endAngle = endAngle-step
   
     if endAngle<lim:
        endAngle=lim
        carte . digital [ pin ].write( endAngle )
        displaypos()
        root.update()
       
        break 
   
     carte . digital [ pin ].write( endAngle )
     displaypos()
     # pb['value']=(endAngle)/(abs(stopZ-startZ))*100
  
     root.update()
     pb['value']+=step
    
            
     
     
def  RotateCCW ():
   
    global endAngle
    global startZ
    global stopZ

    step=int ( current_value.get() )
    
    
    endAngle = endAngle+step
    
    if endAngle>=180:
        endAngle=180
        
    carte.digital[pin].write( endAngle )
    sleep (0.01)
    
    carte.digital[pin].disable_reporting()

    if var_preview.get()==1:
     Preview_Zstack()
    
    
def  RotateCW ():
    
    
    global endAngle
    global startZ
    global stopZ


    step=int ( current_value.get ( ) )
    
    endAngle = endAngle-step
    
    if endAngle<=0:
        endAngle=0
        
    carte.digital[pin].write( endAngle )
    sleep (0.01)
    carte.digital[pin].disable_reporting()

    if var_preview.get()==1:
      Preview_Zstack()
    
    
def  displaypos ():
    
    labelpos.config(text=endAngle)
    labelpos_Zstack.config(text=endAngle)
    
    
def  Zstartpos ():
    global startZ
    startZ=endAngle
    labelZstart.config(text=startZ,bg='green',fg='white')
    
def  Zstoppos ():
    global stopZ
    stopZ=endAngle
    labelZstop.config(text=stopZ,bg='green',fg='white')
    #SweepBtnCCW["state"]=tk.ACTIVE
    #SweepBtnCW["state"]=tk.ACTIVE
    pb["length"]=180
    Text_box_sleep.config(text="Parameters set: Tick the Capture box for stack",bg='orange',fg='white')
    # SweepBtnCCW.state==NORMAL



 
   
#%


def main():
    global camera
    global mon_thread1
    global mon_thread
    global scale1
    global scale3
    global scale4
    global sortie1
    global sortie2
    global frame0
    global frame1
    #global entry_filename
    global entry_directoryvideo
    global entry_filename1
    global entry_filenamevideo
    #global entry_directory
    global entry_directory1
    global entry_timeperhour
    global entry_time
    global entry_exposurebf
    global my_progress
    global cmb
    global carte
    global pin
    
    global current_value
    global labelpos
    global labelZstart, labelZstop, ZstopBtn, labelpos_Zstack, ZstopBtn, var1, var2, SweepBtnCCW, SweepBtnCW
    global Pause, pb
    
    global var1
    global endAngle
    global root
    global Text_box_sleep

    global var_preview
    global progess_counter
    global menu
    #camera initialization
    camera = pylon.InstantCamera(
    pylon.TlFactory.GetInstance().CreateFirstDevice())

    camera.Open()

        # Print the model name of the camera.
    camera.MaxNumBuffer = 2

    camera.Width = camera.Width.Max
    camera.Height = camera.Height.Max
        # camera.ExposureTime = camera.ExposureTime.Min
    camera.PixelFormat = "Mono12"
    camera.ExposureTime.SetValue(20)
    
    #Arduino initialization
            
    carte = Arduino('COM17')
    sortie1 = carte.get_pin('d:3:p')
    #servo = carte.get_pin('d:10:s')
    pin=10
    carte.digital[pin].mode=SERVO
   

    root = Tk()
    root.resizable(True, True)
    root.title('Incubascope 2.0 - Software')
    root.geometry("1800x750")
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
    

    mon_thread=Thread(target=Imagetime)
    mon_thread1=Thread(target=Preview)
    
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


    frame1 = Frame(frame11, width=1000, height=670, background="gray32")
    img2 = Image.fromarray(cv2.resize(II/200, dsize=(600,400), interpolation=cv2.INTER_CUBIC))
    img1 = ImageTk.PhotoImage(image=img2)
    lmain1 = Label(frame1,image=img1,height=400,width=600)
    lmain1.imgtk = img1    
    lmain1.configure(image=img1) 
    lmain1.grid(row=0,column=0,rowspan=4,columnspan=4)

    button_start1 = Button(frame1, text='Start preview', bg='Seagreen1', height=3, width=20, command = Preview)
    button_start1.grid(row=0, column=6, columnspan=3)

    scale1 = Scale( frame1, variable = v, from_ = 0, to = 100, orient = VERTICAL, resolution=20, tickinterval=20, length=150,
        label='BF')
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
   
       
    
    frame_zstack=Frame(root,width=500, height=500)
    frame_zstack.grid(row=0, column=8, columnspan=8, rowspan=8)
    
    CCWBtn = tk . Button ( frame_zstack , width=5, bd = 5 , bg = '#89CFF0' , text = "UP" , 
                          command= lambda:[RotateCCW(),displaypos()]  )
    CCWBtn . grid ( column = 4 , row = 1, pady=10 )

    CWBtn = tk . Button ( frame_zstack , width=5, bd = 5 , bg = '#89CFF0' , text = "DOWN" ,
                         command= lambda:[RotateCW(),displaypos()]  )    
    CWBtn . grid ( column = 4 , row = 2, pady=10)

    var_preview = tk.IntVar()
    ch_pr = tk.Checkbutton(frame_zstack, text='Preview (! Turn on light!)',variable=var_preview, onvalue=1, offvalue=0)
    ch_pr.grid(column=5,row=1,columnspan=3)

    #SweepBtnCCW=tk . Button ( frame_zstack , bd = 5 , bg = '#89CFF0' , text = "sweep UP" ,state="disabled", command= lambda:[SweepCCW()]  )
    #SweepBtnCCW . grid ( column = 4 , row = 8)

    #SweepBtnCW=tk . Button ( frame_zstack , bd = 5 , bg = '#89CFF0' , text = "sweep DOWN" , state="disabled", command= lambda:[SweepCW()]  )
    #SweepBtnCW . grid ( column = 4 , row = 9)

    Pause = tk . Scale ( frame_zstack , bd = 5 , from_ = 2 , to = 10 , resolution=1 , orient = tk.HORIZONTAL )
    Pause . grid ( column = 1 , row = 6, columnspan=3)
    tk . Label ( frame_zstack , text = "Pause (2s to 10s)" ). grid ( column = 2 , row = 7 )
    
    current_value = tk.StringVar(value=1)

    sb = tk.Spinbox(frame_zstack ,textvariable=current_value, width=15,from_=1,to=100)
    sb.grid(row=1,column=1,padx=2,pady=2, columnspan=3)
    sb_label = tk.Label(frame_zstack, text ='Step Size', fg="navyblue") 
    sb_label. grid ( row=2,column=2,padx=2,pady=0)

# sb.Label(win , text = "Pause (0 to 180)" )
    

    labelpos=tk.Label(frame_zstack,text='0',bg='gold',fg='blue')
    labelpos. grid ( column = 2, row = 4 )
    pos_label = tk.Label(frame_zstack, text ='Position (degrees)', fg="blue") 
    pos_label. grid ( row=5 ,column=2,padx=20,pady=2)

    ZstartBtn = tk . Button ( frame_zstack , bd = 5 , bg = '#89CFF0' , text = "Z-start" , command= lambda:[Zstartpos()]   )
    ZstartBtn . grid ( column = 6 , row = 7)
 
    labelZstart=tk.Label(frame_zstack,text='0',width=5,bg='gold',fg='blue')
    labelZstart. grid ( column = 7, row =7  )

    ZstopBtn = tk . Button ( frame_zstack , bd = 5 , bg = '#89CFF0' , text = "Z-stop" , command= lambda:[Zstoppos()]  )
    ZstopBtn . grid ( column = 6 , row = 2)

    labelZstop=tk.Label(frame_zstack,text='0',width=5, bg='gold',fg='blue')
    labelZstop. grid ( column = 7, row =2  )
 
    #ZstopBtn = tk . Button ( frame_zstack , bd = 5 , bg = 'green' , text = "Capture at pos." ,  command= lambda:[capture(var1)]  )
    #ZstopBtn . grid ( column = 6, row = 9)

    labelpos_Zstack=tk.Label(frame_zstack,text='0',width=3,bg='gold',fg='blue')
    labelpos_Zstack. grid ( column = 7, row =4  )

    sb = tk.Spinbox(frame_zstack ,textvariable=current_value, width=5,from_=0,to=180)
    sb.grid(row=5,column=7,padx=5,pady=10)
    sb_label = tk.Label(frame_zstack, text ='Step Size', fg="navyblue") 
    sb_label. grid ( row=6,column=7,padx=2,pady=0)

# labelstep_Z=tk.Label(win,text='0',width=5, bg='gold',fg='blue')
# labelstep_Z. grid ( column = 7, row =6  )
# labelstep_Z_label = tk.Label(win, text ='Step (degrees)', fg="blue") 
# labelstep_Z.config(text=int ( current_value.get() ),bg='green',fg='white')


    var1 = tk.IntVar()
    c1 = tk.Checkbutton(frame_zstack, text='Tick to capture Z_stack',font=('Helvetica Bold',12),variable=var1, onvalue=1, offvalue=0)
    c1.grid(column=2,row=8, columnspan=8, padx=5, pady=5)

    #var2 = tk.IntVar()
    #c2 = tk.Checkbutton(frame_zstack, text='Tick to visualize Z_stack',variable=var2, onvalue=1, offvalue=0)
    #c2.grid(column=3,row=6,columnspan=4)


     



    pb = ttk.Progressbar(frame_zstack, orient='vertical',    mode='determinate',    length=180)
# place the progressbar
    pb.grid(column=8, row=2, rowspan=6, columnspan=1, padx=10, pady=20)

    pb_label=tk.Label(frame_zstack,text='Stack Progress',width=10,fg='blue', bg='white')
    pb_label.grid(column=8, row=8)

    Text_box_sleep = tk.Label(frame_zstack, text='Select Z-stack parameters', width = 52, font=('Helvetica Bold',16))
    Text_box_sleep.grid(row=10, column=1, columnspan=20, pady=20)

    my_progress = ttk.Progressbar(frame_zstack, orient=HORIZONTAL, length=150, mode = "determinate")
    my_progress.grid(row=12, column=1, columnspan=20, pady=20)

    root.mainloop()

if __name__ == "__main__":
    main()

#%%
