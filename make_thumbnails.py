#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

import os
import glob

import skimage.io as io

#Read data
data = pd.read_excel('dataAll-NoNa_allround_binaryLabels_PCAclusters_tested.xlsx')

#Get data
#Get roundID
round = data.iloc[:,0]
#Get plateID
plate = pd.Series([int(x[0]) for x in data.ID_plate.str.split('-')])
colony = pd.Series([int(x[1]) for x in data.ID_plate.str.split('-')])
#Get coordatates
centroid1 = data.centroid_1
centroid2 = data.centroid_2
r = [100]

#Get clusters
cluster = data.cluster6

#Read pictures and crop
folder = '.\images' #read main folder, needs folder with images to be name as 'images'
folders = os.listdir(folder)#each folder will have the data from each round

#Loop inside each folder, get plate and crop. Save using the id and the cluster they belong
for i in np.arange(len(folders)):
    #Loop in folder
    files = glob.glob(folder+'\\'+folders[i]+'\*.tif')
    for j, file in enumerate(files):
        #Read the image
        image = io.imread(file)
        #Get ids    
        nametif = file.split('\\')[3]
        name =  nametif.split('_')[2]+'-c'
        temp_colony = np.array(colony[(round == i+1) & (plate == j+1)])
        #Find coordenates
        temp_centroid1 = np.array(centroid1[(round == i+1) & (plate == j+1)])
        temp_centroid2 = np.array(centroid2[(round == i+1) & (plate == j+1)])
        #temp_diameter = np.array(diameter[(round == i+1) & (plate == j+1)])
        
        #Find cluster
        temp_cluster = np.array(cluster[(round == i+1) & (plate == j+1)])
        #print(temp_centroid1)
        for k in np.arange(len(temp_centroid1)):
            #Generate the name to save the thumbnail
            temp_name = 'r'+str(i)+'id'+str(temp_colony[k])+'_'+name+str(temp_cluster[k])+'.tif'
            temp_image = image[(temp_centroid2[k]-50):(temp_centroid2[k]+50), 
            (temp_centroid1[k]-50):(temp_centroid1[k]+50),:]
            io.imsave(('thumbnails\\'+temp_name), temp_image, plugin='tifffile')   


