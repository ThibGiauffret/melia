#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  1 11:39:16 2019

Melia (Console version) v.0.1_console
Algorithme de détection de mouvement basé sur une prise en rafale de photos

@author: Th. G
"""

# Importation des librairies
from skimage.measure import compare_ssim
from imutils import paths
from imutils import resize
from cv2 import cvtColor
from cv2 import COLOR_BGR2GRAY
from cv2 import imread
from shutil import copyfile
import glob
from os import path
from os import mkdir
import datetime

print('Initialisation...')

now = datetime.datetime.now()

counter=0
detect=0

if path.exists('config.txt'):   # On vérifie si le fichier de configuration existe.
    f= open("config.txt","r")
    contents = f.readlines()
    var = contents[0]   # La première ligne est l'emplacement des photos. 
    var2 = contents[1]  # La seconde ligne est l'emplacement de sauvegrarde. 
    print('Configuration chargée !')    
else :
    print('Erreur de chargement de la configuration :/')

path = var.strip() + "*.JPG"    # On récupère les adresses de toutes les images au format JPG
imagePaths = glob.glob(path)
imagePaths.sort()   # On les trie par ordre alphabétique

for i in range (0,len(imagePaths),3):   # Dans le cas d'un prise en rafale de 3 images, on parcourt toutes les images par groupe de 3.
    print('Traitement en cours...')
    first = imagePaths[i]   
    second = imagePaths[i+1]    
   
    imageA = imread(first)  # On charge la première image de la rafale.
    imageA = resize(imageA, width=min(400, imageA.shape[1]))    # On réduit la résolution pour améliorer le temps de détection et la précision.
    imageA = imageA[70:270,70:330]  # On definit une ROI qui correspond à la zone où on souhaite détecter.
    imageB = imread(second) # On charge la seconde image de la rafale.
    imageB = resize(imageB, width=min(400, imageB.shape[1]))
    imageB = imageB[70:270,70:330]

    grayA = cvtColor(imageA, COLOR_BGR2GRAY) # On passe en niveaux de gris.
    grayB = cvtColor(imageB, COLOR_BGR2GRAY)

    (score, diff) = compare_ssim(grayA, grayB, full=True)   # On calcule de Structural Similarity Index (SSIM).
    diff = (diff * 255).astype("uint8")
    
    if score <= 0.98 :  # Le seuil fixe est choisi expérimentalement 0.98.
        
        print(imagePaths[i] + ' sauvegardée !')
        path2 = var2.strip()
        try:
            mkdir(path2 + now.strftime("%Y-%m-%d"))     # On crée un dossier à la date du jour.
        except FileExistsError:
            pass
        copyfile(imagePaths[i], path2 + now.strftime("%Y-%m-%d") + '/img_'+ str(counter) + '.jpg')  # On copie les images du mouvement.
        detect+=1
        
    counter+=1

print('Terminé, nombre de mouvements détectés : ' + str(detect))
