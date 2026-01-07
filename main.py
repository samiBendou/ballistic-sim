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
Le programme extrait ensuite les informations pertinentes de la simulation

    JSON CONFIGURATION MODE:

    The simulation now uses JSON configuration files for all parameters.
    See CONFIG_README.md for documentation on the configuration format.

    Usage:
        python main.py [config_file.json]

    If no config file is specified, defaults to 'config.json'
"""

import matplotlib.pyplot as plt
import numpy as np
import os
import sys
import scipy.integrate as itg

import simtir.calc as calc
import simtir.grph as grph
import simtir.menu as men
import simtir.config_loader as config_loader
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

# Load configuration from JSON file
config_file = sys.argv[1] if len(sys.argv) > 1 else "config.json"

try:
    (Tmax, h, rep, method, Phys, SYS, M0, config) = config_loader.load_simulation_config(config_file)
    config_loader.print_config_summary(config, Phys, SYS, M0)
except FileNotFoundError:
    print(f"Error: Configuration file '{config_file}' not found.")
    print("Usage: python main.py [config_file.json]")
    print("\nSee CONFIG_README.md for documentation on creating configuration files.")
    sys.exit(1)
except Exception as e:
    print(f"Error loading configuration: {e}")
    sys.exit(1)

# Get number of projectiles
K = len(SYS)

# Run simulation for each projectile
print("Running simulation...")
M, NK = [], []
Nmax = int(Tmax / h)

for k in range(K):
    # Résolution numérique de l'équation de la dynamique
    T = np.linspace(0, Tmax, Nmax)

    def f(U, t):
        return calc.F(U, SYS[k], Phys)

    M.append(itg.odeint(f, M0[k], T))
    NK.append(2 * int((-M0[k, 5] + np.sqrt(M0[k, 5] ** 2 + 2 * M0[k, 2] * Phys.g) / Phys.g / h)))

N = max(NK)

# Display results
os.system("clear")
print("\n     *Simulation effectuée*\n")

# Show numerical info if requested
output_config = config.get("output", {})
show_numerical = output_config.get("show_numerical_info", False)
auto_plot = output_config.get("auto_plot", False)

if show_numerical:
    for k in range(K):
        projectile_name = config["projectiles"][k].get("name", f"Projectile N°{k + 1}")
        print(f"\n=== {projectile_name} ===")
        men.numerique(M[k], NK[k], SYS[k], Phys, h)
        print()

# Generate all plots automatically in a comprehensive view
print("Generating comprehensive plots...")

# Create main figure with all 2D plots (14 subplots in 4x4 grid)
fig = plt.figure(figsize=(20, 16))
fig.suptitle('Complete Simulation Results', fontsize=16, fontweight='bold')

# Define all plot configurations
# Format: (choix1, choix2, subplot_position)
plot_configs = [
    # Row 1: Positions
    (1, 1, 1),   # x(t)
    (1, 2, 2),   # y(t)
    (1, 3, 3),   # z(t)
    # Row 2: Velocities
    (2, 1, 5),   # vx(t)
    (2, 2, 6),   # vy(t)
    (2, 3, 7),   # vz(t)
    # Row 3: Trajectories
    (3, 1, 9),   # y(x)
    (3, 2, 10),  # z(x)
    (3, 3, 11),  # z(y)
    # Row 4: Norms and Energies
    (4, 1, 13),  # r(t)
    (4, 2, 14),  # v(t)
    (5, 1, 15),  # Ec(t)
    (5, 2, 16),  # Ep(t)
]

# Generate all 2D plots
for choix1, choix2, subplot_pos in plot_configs:
    ax = fig.add_subplot(4, 4, subplot_pos)

    for k in range(K):
        projectile_name = config["projectiles"][k].get("name", f"Projectile {k + 1}")
        G = grph.TRACE(choix1, choix2, M[k], NK[k], h, SYS[k], Phys)

        ax.plot(G[0], G[1], label=projectile_name, linewidth=1.5)

    ax.set_xlabel(G[2][0], fontsize=9)
    ax.set_ylabel(G[2][1], fontsize=9)
    ax.set_title(G[2][2], fontsize=10, fontweight='bold')
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3)
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')

plt.tight_layout(rect=[0, 0.03, 1, 0.97])
plt.show()

# Create separate 3D trajectory plot
fig_3d = plt.figure(figsize=(12, 10))
ax_3d = fig_3d.add_subplot(111, projection='3d')

for k in range(K):
    projectile_name = config["projectiles"][k].get("name", f"Projectile {k + 1}")
    G = grph.TRACE_3D(M[k], NK[k])
    ax_3d.plot(G[0], G[1], G[2], label=projectile_name, linewidth=2)

ax_3d.set_xlabel(G[3][0], fontsize=12)
ax_3d.set_ylabel(G[3][1], fontsize=12)
ax_3d.set_zlabel(G[3][2], fontsize=12)
ax_3d.set_title(G[3][3], fontsize=14, fontweight='bold')
ax_3d.legend(fontsize=10)
ax_3d.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

print("\nSimulation terminée.")
