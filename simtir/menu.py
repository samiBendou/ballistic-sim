# -*- coding: utf-8 -*-
"""
Created on Mon Nov  2 15:18:39 2015

@author: Sami
"""

###########################
#                         #
# Fonctions de navigations #
#                         #
###########################

import os
from . import ini
from . import calc 
from . import grph

def chx():
    return int(input("\n   Faites un choix : "))


def conf():
    return int(input("\n   Confirmer les valeurs (Oui: 1, Non: 0) ? "))


def saisie(value):
    """Convertit une valeur d'entrée en float"""
    return float(value)


################################

# Affichage des menus du programme

################################

def princ():
    # Affiche le menu principal et donner le choix entre la simulation et les
    # Options.
    os.system("clear")
    print("\n         *Bienvenue dans SimTir 1.0*\n")
    print(" 1- Simulation simple")
    print(" 2- Options")
    print(" 3- Quitter")

    return chx()


def ci(i, rep):
    """
    Fonction affichant les caractères lors de la saisie des conditions initiales
    par l'utilisateur
    
    COORD : Tableau de caractères contenant le nom des coordonées du système choisi
    visuel : Chaîne de caractères à retouner
    """

    if rep == 'c':
        COORD = ["x", "y", "z"]
        visuel = "v" + COORD[i] + "0 (m/s) : "
    if rep == 's':
        COORD = ["Vr0 (m) :", "Vtheta0 (deg) :", "Vphi0 (deg) :"]
        visuel = COORD[i]

    return visuel


def resultat():
    # Affiche le menu d'exploitation des résultats de la simulations
    print("\n1- Positions en fonction du temps")
    print("2- Vitesses en fonction du temps")
    print("3- Trajectoires")
    print("4- Norme des vecteurs")
    print("5- Energies")
    print("6- Quitter")

    return chx()


def sous_res(choix):
    """
    Affiche le sous menu découlant du choix effectué par l'utiisateur dans le
    menu résultat.
    
    gLfonction : Tableau de caractères de taille 5x3 contant les noms des fonctions
                 à afficher selon le choix de l'utilisateur.
                 
    gLvar : Tableau de caractères contenant les variables correspondant
            aux fonctions ci-dessus
            
    Même méthode que pour visuel graphe.
    """
    gLfonction = [["x", "y", "z"], ["dx/dt", "dy/dt", "dz/dt"], ["y", "z", "z"], ["r", "v"], ["Ec", "Ep", "Em"]]
    gLvar = ["(x)", "(x)", "(y)", "(t)"]

    pos1 = choix - 1

    if choix != 3:
        if choix != 4:
            for k in range(3):
                print(k + 1, "- " + gLfonction[pos1][k] + gLvar[3])
        else:
            for k in range(2):
                print(k + 1, "- " + gLfonction[pos1][k] + gLvar[3])
        return chx()
    else:
        traj_choix = sous_traj()
        if traj_choix == 1:
            for k in range(3):
                print(k + 1, "- " + gLfonction[pos1][k] + gLvar[k])
            return chx()
        else:
            return '3D'


def sous_traj():
    print("\n1 - Graphe 2D")
    print("2 - Trajectoire 3D")
    return chx()


################################

# Affichage des premiers résultats.

################################

def numerique(S, N, Sys, Pp, h):
    # Affiche les informations numériques ci dessous pour un mobile
    L = calc.info(S, N, Sys, Pp)

    print("\n -Nombre d'échantillons : ", N)
    print(" -Temps de chute : ", round(N * h, 2), "sec.")
    print(" -Altitude maximale : ", round(L[0], 2), "m")
    print(" -Portée : ", round(L[1], 2), "m")
    print(" -Vitesse finale : ", round(L[2], 2), "m/s")
    print(" -Energie cinétique finale : ", round(L[3], 2), "J")
    print(" -Travail des forces de frottements :", round(L[4], 2), "J\n")

    return ()


def multi_num(M, K, NK, SYS, Pp, h):
    # Affiche les informations numériques pour tous les mobiles

    os.system("clear")
    print("")
    print("\n     *Simulation effectuée*\n")
    info_num = input("Afficher les informations numériques? ")
    print("")
    if info_num == "oui" or info_num == "OUI" or info_num == "Oui" or info_num == "1":
        for k in range(K):
            numerique(M[k], NK[k], SYS[k], Pp, h)

    return ()


################################

# Affichage des menus de paramétrage

################################

def param_sim():
    # Affiche le menu d'initialisation des paramètres temporels de la simulation.
    # Retourne Pt.

    os.system("clear")
    print("\n Menu Options\n")
    print("1- Temps")
    print("2- Repérage")
    print("3- Paramètres physiques")
    print("4- Paramètres de calcul")
    return chx()


def param_temp():
    # Paramètres temporels

    confirm = 0
    while confirm == 0:
        os.system("clear")
        print("\nParamètres de la simulation :\n")
        h = float(input("    Pas de temps (s) : "))
        Tmax = float(input("   Durée maximale de la simulation : "))
        confirm = conf()

    return (Tmax, h)  # Retourne le pas de temps et la durée max


def param_rep():
    # Paramètres de repérages : choix du système de coordonnées
    confirm = 0
    while confirm == 0:
        os.system("clear")
        print("\nChoissisez un système de coordonnées pour la vitesse initiale : \n")
        rep = input("Taper 's' pour sphérique et 'c' pour cartésien : \n")
        confirm = conf()

    return rep


def param_phys():
    # Affiche le menu simulaion et retourne le choix de l'utilisateur
    os.system("clear")
    print("\nChoisissez votre simulation de chute libre: \n")
    print(" 1- Terrestre dans l'air (Conditions standard)")
    print(" 2- Terrestre sans frottements, sans poussée d'archimède")
    print(" 3- Lunaire")
    print(" 4- Marsienne")
    print(" 5- Simulation personnalisée")

    return ini.phys(chx())


def param_calcul():
    os.system("clear")
    print("\nChoix de la méthode de résolution : \n")
    print("1- Euler explicite")
    print("2- Scipy Odeint")

    return chx()
