# -*- coding: utf-8 -*-
"""
Configuration loader for ballistic simulation

Loads simulation parameters from JSON configuration file
"""

import json
import numpy as np
from .classes import OBJET, PHYS


# Physics presets
PHYSICS_PRESETS = {
    "earth_air": {
        "g": 9.806,
        "rho": 1.184,
        "etha": 0.018e5,
        "omega": 7.272e-05,
        "latitude_deg": 45.0
    },
    "earth_vacuum": {
        "g": 9.806,
        "rho": 0.0,
        "etha": 0.0,
        "omega": 0.0,
        "latitude_deg": 45.0
    },
    "moon": {
        "g": 1.622,
        "rho": 0.0,
        "etha": 0.0,
        "omega": 0.0,
        "latitude_deg": 45.0
    },
    "mars": {
        "g": 3.711,
        "rho": 0.020,
        "etha": 1.48e5,
        "omega": 0.0,
        "latitude_deg": 45.0
    }
}


def load_config(config_path):
    """
    Load configuration from JSON file

    Args:
        config_path: Path to JSON configuration file

    Returns:
        dict: Parsed configuration
    """
    with open(config_path, 'r') as f:
        config = json.load(f)
    return config


def get_physics(config):
    """
    Create PHYS object from configuration

    Args:
        config: Configuration dictionary

    Returns:
        PHYS: Physics environment object
    """
    physics_config = config.get("physics", {})
    preset = physics_config.get("preset", "earth_air")

    # Get parameters from preset or custom
    if preset == "custom":
        params = physics_config.get("custom", {})
    else:
        if preset not in PHYSICS_PRESETS:
            print(f"Warning: Unknown preset '{preset}', using 'earth_air'")
            preset = "earth_air"
        params = PHYSICS_PRESETS[preset].copy()
        # Allow override of preset values with custom values
        if "custom" in physics_config:
            params.update(physics_config["custom"])

    # Create PHYS object
    g = params.get("g", 9.806)
    rho = params.get("rho", 0.0)
    etha = params.get("etha", 0.0)
    omega = params.get("omega", 0.0)
    lat_deg = params.get("latitude_deg", 45.0)
    lat_rad = lat_deg * np.pi / 180.0

    return PHYS(g, rho, etha, lat_rad, omega)


def get_projectile_system(projectile_config):
    """
    Create OBJET from projectile configuration

    Args:
        projectile_config: Dictionary with projectile parameters

    Returns:
        OBJET: Projectile object
    """
    D = projectile_config.get("diameter", 0.1)
    L = projectile_config.get("length", 0.1)
    m = projectile_config.get("mass", 1.0)

    # Calculate volume and surface area
    V = np.pi / 12 * D ** 3 + (L * np.pi / 4) * D ** 2
    S = np.pi / 4 * D ** 2

    obj = OBJET(V, m, S)
    return obj


def get_initial_conditions(projectile_config, coordinate_system):
    """
    Create initial conditions vector U0 from projectile configuration

    Args:
        projectile_config: Dictionary with projectile parameters
        coordinate_system: 'c' for cartesian, 's' for spherical

    Returns:
        numpy.array: Initial state vector [0, 0, z0, vx0, vy0, vz0]
    """
    U0 = np.zeros((6,))

    # Initial altitude
    U0[2] = projectile_config.get("initial_altitude", 0.0)

    # Initial velocity
    vel_config = projectile_config.get("initial_velocity", {})
    vel_type = vel_config.get("type", coordinate_system)

    if vel_type == "cartesian" or vel_type == "c":
        U0[3] = vel_config.get("vx", 0.0)
        U0[4] = vel_config.get("vy", 0.0)
        U0[5] = vel_config.get("vz", 0.0)

    elif vel_type == "spherical" or vel_type == "s":
        # Convert spherical to cartesian
        magnitude = vel_config.get("magnitude", 0.0)
        theta_deg = vel_config.get("theta_deg", 0.0)
        phi_deg = vel_config.get("phi_deg", 0.0)

        theta = theta_deg * np.pi / 180.0
        phi = phi_deg * np.pi / 180.0

        U0[3] = magnitude * np.sin(theta) * np.cos(phi)
        U0[4] = magnitude * np.sin(theta) * np.sin(phi)
        U0[5] = magnitude * np.cos(theta)

    return U0


def load_simulation_config(config_path):
    """
    Load complete simulation configuration from JSON file

    Args:
        config_path: Path to JSON configuration file

    Returns:
        tuple: (Tmax, h, rep, method, Phys, SYS, M0, config)
            - Tmax: Maximum simulation time
            - h: Time step
            - rep: Coordinate system ('c' or 's')
            - method: Numerical method (1 or 2)
            - Phys: PHYS object
            - SYS: List of OBJET objects
            - M0: Array of initial condition vectors
            - config: Original config dict for additional settings
    """
    config = load_config(config_path)

    # Simulation parameters
    sim_config = config.get("simulation", {})
    Tmax = sim_config.get("Tmax", 1000.0)
    h = sim_config.get("h", 0.001)
    rep = sim_config.get("coordinate_system", "c")
    method = sim_config.get("method", 2)

    # Physics environment
    Phys = get_physics(config)

    # Projectiles
    projectiles_config = config.get("projectiles", [])
    SYS = []
    M0 = []

    for proj_config in projectiles_config:
        SYS.append(get_projectile_system(proj_config))
        M0.append(get_initial_conditions(proj_config, rep))

    M0 = np.array(M0)

    return (Tmax, h, rep, method, Phys, SYS, M0, config)


def print_config_summary(config, Phys, SYS, M0):
    """
    Print a summary of the loaded configuration

    Args:
        config: Configuration dictionary
        Phys: PHYS object
        SYS: List of OBJET objects
        M0: Array of initial conditions
    """
    print("\n=== Configuration Loaded ===\n")

    # Simulation parameters
    sim = config.get("simulation", {})
    print(f"Simulation Parameters:")
    print(f"  Tmax: {sim.get('Tmax', 1000.0)} s")
    print(f"  Time step: {sim.get('h', 0.001)} s")
    print(f"  Coordinate system: {'Cartesian' if sim.get('coordinate_system', 'c') == 'c' else 'Spherical'}")
    print(f"  Method: {'Explicit Euler' if sim.get('method', 2) == 1 else 'SciPy odeint'}")

    # Physics
    physics = config.get("physics", {})
    print(f"\nPhysics Environment: {physics.get('preset', 'custom')}")
    print(f"  Gravity: {Phys.g} m/s²")
    print(f"  Fluid density: {Phys.rho} kg/m³")
    print(f"  Viscosity: {Phys.etha} kg/m/s")
    print(f"  Rotation speed: {Phys.omega} rad/s")
    print(f"  Latitude: {Phys.lat * 180 / np.pi:.1f}°")

    # Projectiles
    projectiles = config.get("projectiles", [])
    print(f"\nProjectiles: {len(projectiles)}")
    for i, (proj, sys, u0) in enumerate(zip(projectiles, SYS, M0)):
        name = proj.get("name", f"Projectile {i+1}")
        print(f"\n  {name}:")
        print(f"    Mass: {sys.m} kg")
        print(f"    Diameter: {proj.get('diameter')} m")
        print(f"    Length: {proj.get('length')} m")
        print(f"    Initial altitude: {u0[2]} m")
        print(f"    Initial velocity: ({u0[3]:.2f}, {u0[4]:.2f}, {u0[5]:.2f}) m/s")

    print("\n" + "="*30 + "\n")
