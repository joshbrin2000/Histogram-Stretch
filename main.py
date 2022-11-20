#Note: make sure you have OpenCV, matplot, and tkinter installed!!!

#HOW TO RUN:
#1. Make sure the picture you want to process is in the same location this file is.
#2. Run this file.
#3. Add the name of the file (with the extension as well) in the textbox. e.g. 'baboon.png'.
#4. Click the 'Enter' button.
#5. Click other buttons at your choosing - pay attention to messages printed out to IDLE

#All steps should work except step 6 due to being unclear on how to actually implement this
#Steps 3 and 4 may be wrong in implementation but I believe the method and thought process is there

#BUGS:

import matplotlib.pyplot as plt
import cv2
import numpy as np
import tkinter as tk
from tkinter import *

im = None
test = 0

def enterImage():
    print(entry.get())
    global im
    im = cv2.imread(entry.get())

def histCalc():
    if im is None:
        print('No Image Loaded')
    else:
        height = im.shape[0]
        width = im.shape[1]

        #test to see if there is a single pixel where r != g or r!= b - if so, its color
        red = im[:,:,0]
        green = im[:,:,1]
        blue = im[:,:,2]

        for i in range(len(red)):
            for j in range(len(red[i])):
                if red[i][j] != green[i][j] or red[i][j] != blue[i][j]:
                    global test
                    test = 1
                    
        if (test == 0):
            gColor = cv2.calcHist([im], [0], None, [256], [0, 256])
            plt.title("Histogram of Greyscale Image")
            plt.plot(gColor, color="grey")
            plt.show()
        else:
            rColor = cv2.calcHist([im], [1], None, [256], [0, 256])
            gColor = cv2.calcHist([im], [2], None, [256], [0, 256])
            bColor = cv2.calcHist([im], [0], None, [256], [0, 256])     

            plt.title("Histogram of RGB Image")
            plt.plot(rColor, color="red")
            plt.plot(gColor, color="green")
            plt.plot(bColor, color="blue")

            plt.show()

def histEqual():
    if im is None:
        print('No Image Loaded')
    else:
        imNew = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)
        chan = cv2.split(imNew)
        cv2.equalizeHist(chan[2], chan[2])
        cv2.merge(chan, imNew)
        imDone = cv2.cvtColor(imNew, cv2.COLOR_HSV2BGR)
        cv2.imshow("Original", im)
        cv2.imshow("After Equalization", imDone)

def histStretch():
    if im is None:
        print('No Image Loaded')
    else:
        #histogram stretch
        #min intensity = 0; 255 - 0 = 255
        chan = cv2.split(im)
        multConst = (255)/(im.max() - im.min())
        for i in range(len(chan[0])):
            np.multiply(chan[0][i], multConst)
        for j in range(len(chan[1])):
            np.multiply(chan[1][j], multConst)
        for k in range(len(chan[2])):
            np.multiply(chan[2][k], multConst)
        imNew = cv2.merge(chan, im)
        cv2.imwrite('StretchedImage.jpg', imNew)
        cv2.imshow('Stretched', imNew)

def histStretchAg():
    if im is None:
        print('No Image Loaded')
    else:
        #add a certain percentage - 3% of 255 ~= 8; max = 255 -8 and min = 0 + 8
        chan = cv2.split(im)
        multConst = (255)/((im.max() - 8) - (im.min() + 8))
        for i in range(len(chan[0])):
            np.multiply(chan[0][i], multConst)
        for j in range(len(chan[1])):
            np.multiply(chan[1][j], multConst)
        for k in range(len(chan[2])):
            np.multiply(chan[2][k], multConst)
        imNewAg = cv2.merge(chan, im)
        cv2.imwrite('StretchedImageAg.jpg', imNewAg)
        cv2.imshow('Stretched Aggressive', imNewAg)

#main panel
main = tk.Tk()
main.geometry('800x150')
main.title('Histogram Program')

#label for textbox
tk.Label(main, text="Image File Name").grid(row=0)

#textbox
entry = tk.Entry(main)
entry.grid(row=0, column=1)

#button menu
tk.Button(main, text='Enter', command=enterImage).grid(row=4, column=0, sticky=tk.W)
tk.Button(main, text='   Default Histogram   ', command=histCalc).grid(row=4, column=1, sticky=tk.W)
tk.Button(main, text='Histogram Stretch - Conservative', command=histStretch).grid(row=4, column=2, sticky=tk.W)
tk.Button(main, text='Histogram Stretch - Aggressive', command=histStretchAg).grid(row=4, column=3, sticky=tk.W)
tk.Button(main, text='Histogram Equalization', command=histEqual).grid(row=4, column=4, sticky=tk.W, pady=1)

tk.mainloop()
