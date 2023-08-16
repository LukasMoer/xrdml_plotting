# -*- coding: utf-8 -*-
"""
2D-DIFFRACTION DATA VIEWER 2DDDV
"""
import matplotlib.pyplot as plt
from tkinter import *
from tkinter.filedialog import askopenfilename
import statistics
import math
import numpy as np

def ask_filename():
    """Opens Explorer to pick file. 
    Returns string of filename"""
    root=Tk()
    fn=askopenfilename()
    root.destroy()
    return fn

def read_XRDML(filename):
    """Extracts the values from the xrdml
    parameters: filename [str], 
    returns: numpy 2D array"""
    
    #Read data points
    data = []
    with open(filename, 'r') as fobj:
        for line in fobj:
            if "<counts" in line:
                #<counts> 0 1 0 2 ..</counts>
                #contains a row of the image
                line = line.split(">", 1)[1]
                line = line.split("</")[0]
                values = line.split(" ")
                values = [int(value) for value in values]
                data.append(values)
    return np.array(data)

def read_labels(filename):
    """Open file again to read axis labels, 
    parameters: filename [str]. 
    returns tuple (xmin [float],xmax[float],xlabel[str]) """
    with open(filename, 'r') as fobj:
        xinfo=[]
        reading_info=False
        for line in fobj:
            if reading_info:
                xinfo.append(line)
                if len(xinfo)==3: 
                  break    
            if "<dataPoints>" in line:
                reading_info=True 
            
            
    xangle=xinfo[0].split("\"")[1] #e.g. 2Theta
    xunit=xinfo[0].split("\"")[3] #e.g. deg
    xmin=float(xinfo[1].split("startPosition>")[1].split("</")[0]   )   
    xmax=float(xinfo[2].split("endPosition>")[1].split("</")[0]   ) 
    
    return (xmin,xmax,str(xangle)+" ("+str(xangle)+")")

def plot_xprofile(data, start, end, xscale=1):
    dx=(xmax-xmin)/len(data[0])
    j0=int((start-xmin)/dx)
    j1=int((end-xmin)/dx)
    xprofile=[]
    for j in range(j0,j1):
        column=0
        for i in range(len(data)):
            column+=data[i][j]
        xprofile.append(column)
    xprofile=128*np.array(xprofile)/max(xprofile)
    
    winkel=np.linspace(start,end,len(xprofile))
    xm=0
    for i in range(len(xprofile)):
        xm+=winkel[i]*xprofile[i]/sum(xprofile)
        
    plt.plot([xm,xm],[-128,128],"w--")
    plt.plot([xm,xm],[128,256*xscale],"k-")
    plt.plot(winkel,xprofile*xscale+128,"k-")
    
    return 0

def plot_yprofile(data, start, end, yscale=0.8):
    dx=(xmax-xmin)/len(data[0])
    j0=int((start-xmin)/dx)
    j1=int((end-xmin)/dx)
    yprofil=[]
    for i in range(len(data)):
        yprofil.append(sum(data[i][j0:j1]))
    ym=0
    for i in range(len(yprofil)):
        ym+=(i-128)*yprofil[i]/sum(yprofil)
    ym=-ym
    
    yprofil=np.array(yprofil)
    
    plt.plot([start,end],[ym,ym],"w--")
    plt.plot(yscale*(end-start)*(yprofil)/np.max(yprofil)+end,np.linspace(-128,128,len(yprofil)),"w-")
    return 0


if __name__ == "__main__":
    """"Example of usage"""
    #step 1: pick xrdml file
    filename= ask_filename()
    #step 2: extract data
    data=read_XRDML(filename)
    #step 3: extract x labels
    (xmin,xmax,label_x)=read_labels(filename)
    #step 4: plot the data
    plt.imshow(data,aspect="auto",extent=[xmin,xmax,-len(data)/2,+len(data)/2],cmap="jet")
    plt.plot([xmin,xmax],[0,0],"w-")
    plt.xlabel(label_x)
    #step 5 (optional): examine peak profile between theta=44-46 degrees
    start=44
    end=46
    xscale=1
    yscale=0.8
    
    plot_xprofile(data, start, end, xscale)
    plot_yprofile(data, start, end, yscale)
    

    
    #Optional: Play around a little
    """
    #calculate peaks for simple cubic
    wavelenght=1.54
    d=12.28
    calculated=[]
    for n in range(1,10):
        calculated.append((2*math.asin(n*wavelenght/(2*d)))*180/math.pi)
    
    plt.plot(calculated,[0]*len(calculated),marker="+", markersize=20, markeredgecolor="white")
    """
    
    #Step 6: show plot
    plt.show()

