# -*- coding: utf-8 -*-
"""
Created on Mon Nov  2 15:18:40 2015

@author: Sami
"""
import numpy as np
import numpy.linalg as lng

from . import calc as cl


def LEGENDE(choix1, choix2):
    """
    FONCTION VISUEL GRAPHIQUE
    
    Permet d'afficher les légendes de la courbe voulue par l'utilisateur, renvoie une
    liste de chaînes de caractères.
    
    Sujet : [string] Liste des sujets à afficher dans le titre du graphique
    Normes : [string] complément si le graphe choisi est une norme
    Energies : de même pour l'énergie
    fHoraire : [string][string] Tableau bidimensionnel affichant la fonction horaire voulue
    
    La démarche est la même pour les autres variables. On décompose les phrases
    afin d'écrire les légendes voulues de manière plus compacte
    """

    pos1 = choix1 - 1
    pos2 = choix2 - 1

    Sujet = [r'Position sur l\'axe $(O$', r'Vitesse sur l\'axe $(O$', r'Trajectoire dans le plan $(O$',
             'Norme du vecteur ', 'Energie ']
    Normes = ['Position', 'Vitesse']
    Energies = ['Cinétique', 'Potentielle', 'Mécanique']
    fct_temps = ' en fonction du temps.'

    fHoraire = [[r'$x(t)$', r'$y(t)$', r'$z(t)$'], [r'$v_x(t)$', r'$v_y(t)$', r'$v_z(t)$']]

    fTrajectoire = [r'$y(x)$', r'$z(x)$', r'$z(y)$']
    varTrajectoire = [r'$x$', r'$x$', r'$z$']

    fNorme = [r'$r(t)$', r'$v(t)$']
    fEnergie = [r'$E_c(t)$', r'$E_p(t)$', r'$E_m(t)$']

    Unites = [' (m)', ' (m/s)']
    m = ' (m)'
    J = ' (J)'
    t = r'$t$ (s)'

    gtitle = Sujet[pos1]

    if choix1 < 3:
        ylab = fHoraire[pos1][pos2] + Unites[pos1]
        xlab = t

        if choix2 == 1:
            gtitle += r'$x)$'
        elif choix2 == 2:
            gtitle += r'$y)$'
        elif choix2 == 3:
            gtitle += r'$z)$'

        gtitle += fct_temps

    elif choix1 == 3:
        ylab = fTrajectoire[pos2] + m
        xlab = varTrajectoire[pos2] + m

        if choix2 == 1:
            gtitle += r'$xy)$'
        elif choix2 == 2:
            gtitle += r'$xz)$'
        elif choix2 == 3:
            gtitle += r'$yz)$'

    elif choix1 == 4:
        ylab = fNorme[pos2] + Unites[pos2]
        xlab = t
        gtitle += Normes[pos2] + fct_temps
    elif choix1 == 5:
        ylab = fEnergie[pos2] + J
        xlab = t
        gtitle += Energies[pos2] + fct_temps
    else:
        ylab = 0
        xlab = 0

    return xlab, ylab, gtitle


def extrait(choix1, choix2, S, N, Sys, Pp):
    """
    FONCTION GRAPHE
    
    permet d'extraire le graphe voulu par l'utilisateur. Retourne le tuple (X, Y)
    qui représente le graphe de la grandeur à tracer
    """
    pos1 = choix1 - 1
    pos2 = choix2 - 1
    X = []
    Y = []
    for k in range(N):
        if choix1 <= 2:  # Tracé des positions ou des vitesses en fonction du temps
            Y.append(S[k][pos2 + 3 * pos1])
        elif choix1 == 3:  # Tracé des trajectoires en 2D
            if choix2 < 3:  # Ce choix détermine le plan dans lequel on trace la trajectoire
                X.append(S[k][0])
                Y.append(S[k][choix2])
            if choix2 == 3:
                X.append(S[k][1])
                Y.append(S[k][2])
        elif choix1 == 4:  # Norme des vecteurs accéleration et vitesses
            if choix2 == 1:
                Y.append(lng.norm(S[k][:3]))
            elif choix2 == 2:
                Y.append(lng.norm(S[k][3:]))
        elif choix1 == 5:  # Energies
            Y.append(cl.Eng(S[k][3:], S[k][2], Sys, Pp)[pos2])

    if choix1 == 3:
        return X, Y
    else:
        return Y


def TRACE(choix1, choix2, S, N, h, Sys, Pp):
    """
    Extrait, affiche et légende le graphique voulu par l'utilisateur
    
        -texteG : Contient le texte à afficher pour légender le graphe G [xlab, ylab, title]
    """

    if choix1 == 3:
        (X, Y) = extrait(choix1, choix2, S, N, Sys, Pp)
    else:
        Y = extrait(choix1, choix2, S, N, Sys, Pp)
        X = np.linspace(0, N * h, N)

    texteG = LEGENDE(choix1, choix2)

    return (X, Y, texteG)


def TRACE_3D(S, N):
    """
    De même pour l'affichage de la trajectoire en 3D
    """
    X, Y, Z = [], [], []
    for k in range(N):
        X.append(S[k][0])
        Y.append(S[k][1])
        Z.append(S[k][2])
    #
    #    ax.set_xlim3d(0, max(X)+0.5)
    #    ax.set_ylim3d(min(Y)-0.5, max(Y)+0.5)
    #
    texteG = ('x (m)', 'y (m)', 'z (m)', 'Trajectoire(s) dans l\'espace')

    return (X, Y, Z, texteG)
