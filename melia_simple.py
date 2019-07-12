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
from imutils import grab_contours
import cv2
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
    
    path = var.strip() + "*.JPG"    # On récupère les adresses de toutes les images au format JPG
    imagePaths = glob.glob(path)
    imagePaths.sort()   # On les tris par ordre alphabétique
    
    for i in range (0,len(imagePaths),3):   # Dans le cas d'un prise en rafale de 3 images, on parcours toutes les images par groupe de 3.
        print('Traitement en cours...')
        first = imagePaths[i]   
        second = imagePaths[i+1]    
       
        imageA = cv2.imread(first)  # On charge la première image de la rafale.
        imageA = resize(imageA, width=min(400, imageA.shape[1]))    # On réduit la résolution pour améliorer le temps de détection et la précision.
        #imageA = imageA[70:270,70:330]  # On peut définir une ROI qui correspond à la zone où on souhaite détecter.
        imageB = cv2.imread(second) # On charge la seconde image de la rafale.
        imageB = resize(imageB, width=min(400, imageB.shape[1]))
        #imageB = imageB[70:270,70:330]
    
        grayA = cv2.cvtColor(imageA, cv2.COLOR_BGR2GRAY) # On passe en niveaux de gris.
        grayB = cv2.cvtColor(imageB, cv2.COLOR_BGR2GRAY)
    
        (score, diff) = compare_ssim(grayA, grayB, full=True)   # On calcule de Structural Similarity Index (SSIM).
        diff = (diff * 255).astype("uint8")
        
        thresh = cv2.threshold(diff, 0, 255,
    	        cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
        cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
        	    cv2.CHAIN_APPROX_SIMPLE)
        cnts = grab_contours(cnts)
            #print(len(cnts))
            
    #        cv2.imshow("Thresh", thresh)
    #        k = cv2.waitKey(0)
    #        if k == 27:         # wait for ESC key to exit
    #            cv2.destroyAllWindows()
            
        if score <= 0.98 and len(cnts) < 20 :  # Le seuil fixe est choisit expérimentalement 0.98. 
            # On élimine aussi les clichés avec trop de bruit !
            detect+=1
            
            path2 = var2.strip()
            try:
                mkdir(path2)
                try:
                    mkdir(path2 + now.strftime("%Y-%m-%d"))     # On crée un dossier à la date du jour.
                except FileExistsError:
                    pass
            except FileExistsError:
                try:
                    mkdir(path2 + now.strftime("%Y-%m-%d"))     # On crée un dossier à la date du jour.
                except FileExistsError:
                    pass
            try:
                copyfile(imagePaths[i], path2 + now.strftime("%Y-%m-%d") + '/img'+ str(counter) + '.jpg')  # On copie les images du mouvement.
                print(imagePaths[i] + ' sauvegardée !')
            except FileNotFoundError:
                print('Une erreur s\'est produite !')
            
            counter+=1

    print('Terminé, nombre de mouvements détectés : ' + str(detect))

else :
    print('Erreur de chargement de la configuration :/')

