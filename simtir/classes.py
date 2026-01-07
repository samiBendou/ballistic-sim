# -*- coding: utf-8 -*-
"""
Created on Mon Nov  9 17:58:38 2015

@author: Sami
"""


class PHYS:
    """
    Classe des paramètres physiques
    
    Contient les informations relatives à la planète sur laquelle on étudie
    la chute libre.
    """

    def __init__(self, pesanteur, masse_volumique, viscosite, latitude, vitesse_rotation):
        self.g = pesanteur
        self.rho = masse_volumique
        self.etha = viscosite
        self.lat = latitude
        self.omega = vitesse_rotation


class OBJET:
    """
    Classe objet
    
    Contient les dimensions du système étudié
    """

    def __init__(self, volume, masse, surface):
        self.V = volume
        self.m = masse
        self.S = surface

# class SOLID :
#    """
#    Classe solide
#    
#    Contient : 
#        -La masse M du solide
#        -les moments d'inertie du ieme solide dans le repère R2i
#        -La position XG du centre de gravité
#        -Les volumes des parties cylindriques (vol_1) et conique (vol_2)
#        -La surface de front au vent (surf)
#    """
#    def __init__(self, masse, vol_1, vol_2, XG,surf) :
#        self.M = masse
#        self.V1 = vol_1
#        self.V2 = vol_2
#        self.
