# -*- coding: utf-8 -*-
"""
Created on Mon Nov  2 15:18:40 2015

@author: Sami
"""
import numpy as np

from . import menu
from .classes import OBJET
from .classes import PHYS


def sys():
    """
    INITIALISE SYSTEME
    
    Demande à l'utilisateur de saisir les dimensions du système, retourne un 
    objet de type OBJET
    """
    confirm = 0
    print("\nDimension du projectile : \n")
    while confirm == 0:
        Sys = OBJET(0, 0, 0)
        D = float(input("  Diamètre (m) : "))
        L = float(input("  Longueur (m) : "))
        Sys.m = float(input("  Masse du projectile (kg) : "))
        confirm = menu.conf()

    Sys.V = np.pi / 12 * D ** 3 + (L * np.pi / 4) * D ** 2  # Volume du système
    Sys.S = np.pi / 4 * D ** 2

    return Sys


def cond(rep):
    """
    CONDITIONS INITIALES
    
    Demande à l'utilisateur de saisir les conditions initiales pour un système
    retourne le vecteur mouvement initial U0
    
        -rep : choix du type de repère (cartésien ou cylindrique)
        -U0save : Sauvegarde de la vitesse initiale en coordonnées sphériques
                  afin de pouvoir convertir en coordonnées cartésiennes
    """
    U0 = np.zeros((6,))  # Vecteur U0 initial
    confirm = 0

    while confirm == 0:
        U0[2] = float(input("\nAltitude initiale (m) : "))
        print("\nVitesse initiale : ")
        for i in range(3, 6):
            U0[i] = float(input(menu.ci(i - 3, rep)))
        confirm = menu.conf()

    if rep == 's':  # Conversion des coordonnées pour le calcul
        radeg = np.pi / 180  # Conversion Deg -> Rag
        U0save = U0[1:]
        theta0 = U0save[1] * radeg
        phi0 = U0save[2] * radeg

        U0[1] = U0save[0] * np.sin(theta0) * np.cos(phi0)
        U0[2] = U0save[0] * np.sin(theta0) * np.sin(phi0)
        U0[3] = U0save[0] * np.cos(theta0)

    return U0


def MULTI(K, rep):
    SYS = []
    M0 = []

    for i in range(K):
        # Choix des conditions initiales et des paramètres des objets
        print("\n     Choissisez les paramètres du projectile n°", i + 1, "\n")
        SYS.append(sys())
        M0.append(cond(rep))

    return (SYS, np.array(M0))


def phys(choix):
    """
    INITIALISE PARAMETRES PHYSIQUES
    
    Retourne un objet de type PHYS dépendant du choix de l'utilisateur dans
    param_phys
    """
    Pp = PHYS(0, 0, 0, 0, 0)

    if choix == 1:
        Pp.g = 9.806
        Pp.rho = 1.184
        Pp.etha = 0.018e5
        Pp.lat = np.pi / 4
        Pp.omega = 7.272e-05
    if choix == 2:
        Pp.g = 9.806
        Pp.rho = 0.
        Pp.etha = 0.
        Pp.lat = np.pi / 4
        Pp.omega = 0.
    if choix == 3:
        Pp.g = 1.622
        Pp.rho = 0.
        Pp.etha = 0.
        Pp.lat = np.pi / 4
        Pp.omega = 0.
    if choix == 4:
        Pp.g = 3.711
        Pp.rho = 0.020
        Pp.etha = 1.48e5
        Pp.lat = np.pi / 4
        Pp.omega = 0.
    if choix == 5:
        confirm = 0
        while confirm == 0:
            print("\n Paramètres de l'environnement :\n")
            Pp.g = menu.saisie(input("Intensité de l'accéleration de la pesanteur (m/s^2) : "))
            Pp.rho = menu.saisie(input("Masse volumique du fluide environnant (kg/m^3) : "))
            Pp.etha = menu.saisie(input("Coefficient de viscosité de fluide (kg/m/s) : "))
            Pp.omega = menu.saisie(input("Vitesse de l'astre considéré (rad/s) : "))
            Pp.lat = np.pi / 180 * menu.saisie(input("Latitude d'étude (degrés) :"))
            confirm = menu.conf()

    return Pp
