# -*- coding: utf-8 -*-
"""
Created on Mon Nov  2 15:32:16 2015

@author: Sami
"""
import numpy as np
import numpy.linalg as lng

# Définition des vecteurs de la base canonique

ex = np.array([1, 0, 0])
ey = np.array([0, 1, 0])
ez = np.array([0, 0, 1])

"""
**********FONCTIONS DE CALCUL**********
"""


def coeff_archimede(Sys, Phys):
    return Phys.rho * Sys.V * Phys.g


def coeff_frottement(S, rho):
    Cx = 0.45
    return -1 / 2 * Cx * S * rho


def F(U, Sys, Phys):
    """
    FONCTION dU/dt
    
    Calcule la résultante des forces appliquées aux système et retourne la
    dérivée temporelle du vecteur U qui est une fonction de U et des paramètres
    physiques. Les grandeurs ci-dessous sont instantanées.
    On utilise un repérage cartésien lié au référentiel terrestre.
    
        U : array Vecteur mouvement (X, Y, Z, Vx, Vy, Vz)
        DU : dérivée temporelle de U
        A : Accelération
        V : Vitesse
    """
    A = np.zeros((3,))
    DU = np.zeros((6,))

    V = U[3:]
    DU[:3] = V

    A += -Phys.g * ez

    if Phys.rho != 0:
        kfrot = coeff_frottement(Sys.S, Phys.rho)
        karchimede = coeff_archimede(Sys, Phys)
        A += kfrot / Sys.m * V * lng.norm(V) + karchimede / Sys.m * ez
    if Phys.omega != 0:
        OMEGA = Phys.omega * np.array([-np.sin(Phys.lat), np.cos(Phys.lat), 0])
        A += - 2 * np.cross(OMEGA, V)

    DU[3:] = A

    return DU


def EULER(U0, Sys, Pp, h, Tmax):
    """
    CALCUL DU VECTEUR MOUVEMENT
    
   On résouds l'équation du mouvement par la méthode d'Euler explicite.
   On utilise un repère cartésien lié au référentiel terrestre.
   
       -U : array Vecteur mouvement (X, Y, Z, Vx, Vy, Vz)
       -S : [array,...] Tableau stockant le vecteur U à chaque instant
            S[k][0] représente la position sur (Ox) à l'instant tk = k * h
    """
    j = 0
    S = [U0]

    # Résolution de l'équation du mouvement
    while S[j][2] >= 0 and j * h < Tmax:
        # La simulation s'arrête lorsque l'objet possède une altitude nulle
        # ou que la durée limite est atteinte.
        DU = F(S[j], Sys, Pp)
        S += [S[j] + DU * h]
        j += 1

    return S


def info(S, N, Sys, Pp):
    """
    CALCUL INFORMATIONS NUMERIQUES
    
    Affiche les informations relatives à un lancé dont les paramètres sont stockés
    dans S
    """

    zmax = max(S[:N][2])
    vfinal = lng.norm(S[N][3:])

    Einit = Eng(S[0][3:], S[0][2], Sys, Pp)
    Efinal = Eng(S[N][3:], S[N][2], Sys, Pp)
    Ecfinal = Efinal[0]  # Energie cinétique finale
    W = np.abs(Efinal[2] - Einit[2])  # Travail des forces non conservatives

    dist = lng.norm(S[N][:3])  # Distance finale à l'origine

    return (zmax, dist, vfinal, Ecfinal, W)


def Eng(v, z, Sys, Pp):
    # Calcule les énergies potentielle, cinétique (de translation)
    # et mécanique du système.

    Ec = 0.5 * Sys.m * lng.norm(v) ** 2
    Ep = (Sys.m * Pp.g - Pp.rho * Sys.V) * z
    return (Ec, Ep, Ec + Ep)
