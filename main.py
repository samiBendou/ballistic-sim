# -*- coding: utf-8 -*-
"""
Created on Mon Nov  2 15:35:33 2015
Created on Mon Apr 20 12:53:41 2015
@author: Sami

    SIMULATEUR CHUTE LIBRE 3.0 :
    
Programme simulant la chute libre d'un objet cylindrique (voir documentation)
à la surface d'une planète.
On étudie la chute du centre de gravité de l'objet jusqu'à ce que son altitude soit nulle,
ou que l'on ai atteint la durée maximale désiré.
Le programme extrait ensuite les informations pertinent
es de la simulation

    MODES :
    
    -Simulation simple : On étudie la trajectoire d'un seul mobile
    
    -Multisim : On peut choisir un nombre arbitraire de mobile et superposer
                les résultats obtenus.
                
    -Options : Paramètres de la simulations
"""

import matplotlib.pyplot as plt
import numpy as np
import os
import scipy.integrate as itg

import simtir.calc as calc
import simtir.grph as grph
import simtir.ini as ini
import simtir.menu as men
from simtir.classes import PHYS

"""
    EXECUTION DU PROGRAMME :
    
    Variables :
        
        Tmax : float Durée maximale de la simulation
        
        h : float -  Pas de temps de la simulation
        
        rep : string - Correspond au type de repérage utilisé pour choisir la vitesse initiale
        
        method : int - méthode de simulation utilisée
        
        Phys, Sys : classes - Voir le fichier de description des classes.
        
        S ou M: array - Voir calcul
        
        N : int - Nombres d'échantillons de S ou de M à utiliser pour l'extraction des valeurs
        
        U0 : array - Vecteur mouvement initial (0, 0, Z0, VX0, VY0, VZ0)
        
        M0 : array - De la forme (U00, U01,..., U0K) où K est le nombre de
             mobiles
    
"""

(Tmax, h) = (1e3, 1e-3)  # Initialisation des paramètres avec les valeurs par défaut
Phys = PHYS(9.86, 0, 0, 0, 0)

rep = 'c'  # Repérage cartésien par défaut
method = 2
confirm = 0

choix_princ = 0

while (choix_princ != 3):

    choix_princ = men.princ()

    # Menu Simulation simple
    if choix_princ == 1:

        M, NK = [], []
        K = int(input("\nCombien de projectiles : "))
        (SYS, M0) = ini.MULTI(K, rep)  # Initialisation du système et saisie des coordonnées du système
        Nmax = int(Tmax / h)

        for k in range(K):
            # Résolution  numérique de l'équation de la dynamique.
            T = np.linspace(0, Tmax, Nmax)


            def f(U, t):
                return calc.F(U, SYS[k], Phys)


            M.append(itg.odeint(f, M0[k], T))
            NK.append(2 * int((-M0[k, 5] + np.sqrt(M0[k, 5] ** 2 + 2 * M0[k, 2] * Phys.g) / Phys.g / h)))
        N = max(NK)
        # Affichage des résultats
        os.system("clear")
        print("\n     *Simulation effectuée*\n")
        for k in range(K):
            info_num = input("Afficher les informations numériques du projectile N°{0} (1 pour oui)?\n".format(k + 1))
            if info_num == "1":
                men.numerique(M[k], NK[k], SYS[k], Phys, h)

        chx_res = 0
        while (chx_res != 6):
            chx_res = men.resultat()  # Choix du type de courbe à tracer
            if chx_res != 6:
                chx_grph = men.sous_res(chx_res)
                Legend = []  # Chaînes contenant la légende de chaque courbe

                if chx_grph == '3D':
                    fig = plt.figure()  # Création de l'environnemment 3D
                    ax = fig.add_subplot(111, projection='3d')
                    for k in range(K):
                        Legend.append("N°{0}".format(k + 1))
                        G = grph.TRACE_3D(M[k], NK[k])
                        ax.plot(G[0], G[1], G[2])

                    ax.set_xlabel(G[3][0])  # Légendage 3D
                    ax.set_ylabel(G[3][1])
                    ax.set_zlabel(G[3][2])
                    ax.set_title(G[3][3])

                else:
                    for k in range(K):
                        fig = plt.figure()  # Création de l'environnemment 2D
                        ax = fig.add_subplot(111)

                        Legend.append(" Projectile N°{0}".format(k + 1))
                        G = grph.TRACE(chx_res, chx_grph, M[k], NK[k], h, SYS[k], Phys)

                        ax.spines['right'].set_color('none')
                        ax.spines['top'].set_color('none')
                        plt.plot(G[0], G[1])

                        plt.xlabel(G[2][0])  # Légendage 2D
                        plt.ylabel(G[2][1])
                        plt.title(G[2][2])

                plt.legend(Legend)  # Affichage de la légende des courbes
                plt.show()
                chx_grph = 0

                # Menu Options
    if choix_princ == 2:
        chx_opt = men.param_sim()
        if chx_opt == 1:
            (Tmax, dt) = men.param_temp()
        if chx_opt == 2:
            rep = men.param_rep()
        if chx_opt == 3:
            Phys = men.param_phys()
        if chx_opt == 4:
            method = men.param_calcul()
