#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  1 11:39:16 2019

Melia GUI v.0.1_gui
Algorithme de détection de mouvement basé sur une prise en rafale de photos

@author: Th. G
"""

# import the necessary packages
from skimage.measure import compare_ssim
import imutils
import cv2
from shutil import copyfile
import glob
import os
import datetime
from tkinter import * 
from PIL import Image
from PIL import ImageTk
import platform

now = datetime.datetime.now()

fenetre = Tk()

fenetre.title("Melia")

cadre1 = Frame(fenetre, width=600, height=50, borderwidth=1)
cadre1.pack(side=TOP, fill=X, expand=True, anchor=N)

titleLabel = Label(cadre1, font=('arial', 12, 'bold'),
                   text="Detection de mouvement par comparaison d'images",
                   bd=5, anchor=N)
titleLabel.pack()

cadre = Frame(fenetre, width=300, height=300, borderwidth=1)
cadre.pack(side=LEFT, fill=X, expand=True, anchor=W)

configArea = LabelFrame(cadre, text="Configuration ", width=250, height=80)
configArea.pack(fill=X, padx=20, pady=10)


if os.path.exists('config.txt'):
    f= open("config.txt","r")
    contents = f.readlines()
    var_texte = contents[0]
    var_texte2 = contents[1]
else :
    f2= open("config.txt","r+")
    contents = []
    contents.append(ligne_texte.get() + "\n")
    contents.append(ligne_texte2.get() + "\n")
    with open("config.txt", "w") as f2:
        f2.writelines(contents)
    f2.close()
    

f.close()

label_rafale = Label(configArea, text="Nombre de photos en rafale")
label_rafale.pack(anchor=W)

rafale = StringVar()
rafale.set('3')
ligne_rafale = Entry(configArea, textvariable=rafale, background='white')
ligne_rafale.pack()

label_seuil = Label(configArea, text="Seuil de similarité (de 0 à 1)")
label_seuil.pack(anchor=W)

seuil = StringVar()
seuil.set('0.98')
ligne_seuil = Entry(configArea, textvariable=seuil, background='white')
ligne_seuil.pack()

label2 = Label(configArea, text="Emplacement des photos")
label2.pack(anchor=W)

v = StringVar()
v.set(var_texte.strip())
ligne_texte = Entry(configArea, textvariable=v, background='white')
ligne_texte.pack(fill=X)

def view_source():
    path3 = str(ligne_texte.get())
    system = platform.system()
    print(system)
    if system == "Linux" :
        os.system('xdg-open "%s"' % path3)
    else :
        os.startfile(path3)

bouton_source = Button(configArea, text="Voir toutes les photos", command=view_source)
bouton_source.pack(anchor=E)

label3 = Label(configArea, text="Emplacement de sauvegarde")
label3.pack(anchor=W)

v2 = StringVar()
v2.set(var_texte2.strip())
ligne_texte2 = Entry(configArea, textvariable=v2, background='white')
ligne_texte2.pack(fill=X)

def view():
    path3 = str(ligne_texte2.get())
    system = platform.system()
    print(system)
    if system == "Linux" :
        os.system('xdg-open "%s"' % path3)
    else :
        os.startfile(path3)

bouton_voir = Button(configArea, text="Voir les photos extraites", command=view)
bouton_voir.pack(anchor=E)

def update_config():
    f2= open("config.txt","r+")
    contents = f2.readlines()
    contents[0] = ligne_texte.get() + "\n"
    contents[1] = ligne_texte2.get() + "\n"
    
    with open("config.txt", "w") as f2:
        f2.writelines(contents)
    f2.close()
    print('Configuration sauvegardée !')

bouton_update2 = Button(configArea, text="Sauvergarder la configuration", command=update_config)
bouton_update2.pack(padx=20, pady=10)


def run():
    window = Toplevel(fenetre)
    window.title("Detection de mouvement en cours")
    picture = Label(window, text="Visionneuse")
    picture.pack() 
    
    bouton_lancer.config(text='Tri en cours...', state=DISABLED)

    counter=0
    detect=0
    
    path = str(ligne_texte.get()) + "*.JPG"
    imagePaths = glob.glob(path)
    imagePaths.sort()
    
    for i in range (0,len(imagePaths),int(ligne_rafale.get())):

        first = imagePaths[i]
        second = imagePaths[i+1]
       
        imageA = cv2.imread(first)
        imageA = imutils.resize(imageA, width=min(400, imageA.shape[1]))
        imageA = imageA[70:270,70:330]
        imageB = cv2.imread(second)
        imageB = imutils.resize(imageB, width=min(400, imageB.shape[1]))
        imageB = imageB[70:270,70:330]
    
        grayA = cv2.cvtColor(imageA, cv2.COLOR_BGR2GRAY)
        grayB = cv2.cvtColor(imageB, cv2.COLOR_BGR2GRAY)
    
        (score, diff) = compare_ssim(grayA, grayB, full=True)
        diff = (diff * 255).astype("uint8")
        # print("SSIM: {}".format(score))
        
        
        n_seuil = float(ligne_seuil.get())
        
        if score <= n_seuil :
            
            thresh = cv2.threshold(diff, 0, 255,
            	cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
            cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
            	cv2.CHAIN_APPROX_SIMPLE)
            cnts = imutils.grab_contours(cnts)
        
            for c in cnts:
                	(x, y, w, h) = cv2.boundingRect(c)
                	cv2.rectangle(imageA, (x, y), (x + w, y + h), (0, 0, 255), 2)
            
            im = Image.fromarray(imageA)
            imgtk = ImageTk.PhotoImage(image=im)
            picture.config(image=imgtk)
            fenetre.update()
            print(imagePaths[i] + ' sauvegardée !')
            path2 = str(ligne_texte2.get()) 
            try:
                os.mkdir(path2 + now.strftime("%Y-%m-%d"))
            except FileExistsError:
                pass
            copyfile(imagePaths[i], path2 + now.strftime("%Y-%m-%d") + '/img_'+ str(counter) + '.jpg')
            detect+=1
            
        counter+=1
        
    label4 = Label(cadre, text="Nombre de mouvements détectés : {}".format(detect))
    label4.pack()
    bouton_lancer.config(text='Lancer la détection !', state="normal")
    window.destroy()


bouton_lancer = Button(cadre, text="Lancer la détection !", command=run)
bouton_lancer.pack(padx=20, pady=20)

fenetre.mainloop() 

#    # threshold the difference image, followed by finding contours to
#    # obtain the regions of the two input images that differ
#    thresh = cv2.threshold(diff, 0, 255,
#    	cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
#    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
#    	cv2.CHAIN_APPROX_SIMPLE)
#    cnts = imutils.grab_contours(cnts)
#
#    # loop over the contours
#    for c in cnts:
#    	# compute the bounding box of the contour and then draw the
#    	# bounding box on both input images to represent where the two
#    	# images differ
#    	(x, y, w, h) = cv2.boundingRect(c)
#    	cv2.rectangle(imageA, (x, y), (x + w, y + h), (0, 0, 255), 2)
#    	cv2.rectangle(imageB, (x, y), (x + w, y + h), (0, 0, 255), 2)
#
## show the output images
#cv2.imshow("Original", imageA)
#cv2.imshow("Modified", imageB)
#cv2.imshow("Diff", diff)
#cv2.imshow("Thresh", thresh)
#cv2.waitKey(0)
