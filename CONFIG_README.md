# Configuration File Documentation

This document describes the JSON configuration format for the ballistic simulation.

## Configuration Structure

### Simulation Parameters

```json
"simulation": {
  "Tmax": 1000.0,        // Maximum simulation time in seconds
  "h": 0.001,            // Time step for numerical integration in seconds
  "coordinate_system": "c",  // 'c' for cartesian, 's' for spherical
  "method": 2            // 1 = Explicit Euler, 2 = SciPy odeint (recommended)
}
```

### Physics Environment

The `physics` section supports both presets and custom parameters:

#### Using Presets

Available presets:
- `"earth_air"` - Earth with air resistance (default)
- `"earth_vacuum"` - Earth without atmosphere
- `"moon"` - Moon environment
- `"mars"` - Mars with thin atmosphere
- `"custom"` - Use custom parameters defined in the `custom` section

```json
"physics": {
  "preset": "earth_air"
}
```

#### Preset Values

| Preset | g (m/s²) | rho (kg/m³) | etha (kg/m/s) | omega (rad/s) |
|--------|----------|-------------|---------------|---------------|
| earth_air | 9.806 | 1.184 | 1.8e-05 | 7.272e-05 |
| earth_vacuum | 9.806 | 0.0 | 0.0 | 0.0 |
| moon | 1.622 | 0.0 | 0.0 | 0.0 |
| mars | 3.711 | 0.020 | 1.48e-05 | 0.0 |

#### Custom Parameters

```json
"physics": {
  "preset": "custom",
  "custom": {
    "g": 9.806,           // Gravity acceleration (m/s²)
    "rho": 1.184,         // Fluid density (kg/m³)
    "etha": 1.8e-05,      // Viscosity coefficient (kg/m/s)
    "omega": 7.272e-05,   // Planetary rotation speed (rad/s)
    "latitude_deg": 45.0  // Latitude of observation point (degrees)
  }
}
```

### Projectiles

Define one or more projectiles to simulate:

```json
"projectiles": [
  {
    "name": "Projectile 1",        // Optional descriptive name
    "diameter": 0.1,               // Diameter in meters
    "length": 0.5,                 // Length in meters
    "mass": 2.5,                   // Mass in kilograms
    "initial_altitude": 100.0,     // Starting altitude in meters
    "initial_velocity": {
      "type": "cartesian",         // 'cartesian' or 'spherical'
      "vx": 10.0,                  // X velocity component (m/s)
      "vy": 0.0,                   // Y velocity component (m/s)
      "vz": 20.0                   // Z velocity component (m/s)
    }
  }
]
```

#### Velocity Specifications

**Cartesian coordinates:**
```json
"initial_velocity": {
  "type": "cartesian",
  "vx": 10.0,   // X component (m/s)
  "vy": 0.0,    // Y component (m/s)
  "vz": 20.0    // Z component (m/s)
}
```

**Spherical coordinates:**
```json
"initial_velocity": {
  "type": "spherical",
  "magnitude": 25.0,      // Velocity magnitude (m/s)
  "theta_deg": 60.0,      // Polar angle (degrees from vertical)
  "phi_deg": 0.0          // Azimuthal angle (degrees)
}
```

### Output Options

```json
"output": {
  "show_numerical_info": true,   // Display numerical results for each projectile
  "auto_plot": false             // Automatically show plots (false = interactive menu)
}
```

## Example Configurations

### Simple Drop Test

```json
{
  "simulation": {
    "Tmax": 10.0,
    "h": 0.001,
    "coordinate_system": "c",
    "method": 2
  },
  "physics": {
    "preset": "earth_air"
  },
  "projectiles": [
    {
      "name": "Ball",
      "diameter": 0.1,
      "length": 0.1,
      "mass": 0.5,
      "initial_altitude": 50.0,
      "initial_velocity": {
        "type": "cartesian",
        "vx": 0.0,
        "vy": 0.0,
        "vz": 0.0
      }
    }
  ]
}
```

### Multiple Projectile Comparison

Compare different launch angles on the Moon:

```json
{
  "simulation": {
    "Tmax": 100.0,
    "h": 0.01,
    "coordinate_system": "s",
    "method": 2
  },
  "physics": {
    "preset": "moon"
  },
  "projectiles": [
    {
      "name": "30 degrees",
      "diameter": 0.05,
      "length": 0.2,
      "mass": 1.0,
      "initial_altitude": 1.0,
      "initial_velocity": {
        "type": "spherical",
        "magnitude": 20.0,
        "theta_deg": 30.0,
        "phi_deg": 0.0
      }
    },
    {
      "name": "45 degrees",
      "diameter": 0.05,
      "length": 0.2,
      "mass": 1.0,
      "initial_altitude": 1.0,
      "initial_velocity": {
        "type": "spherical",
        "magnitude": 20.0,
        "theta_deg": 45.0,
        "phi_deg": 0.0
      }
    },
    {
      "name": "60 degrees",
      "diameter": 0.05,
      "length": 0.2,
      "mass": 1.0,
      "initial_altitude": 1.0,
      "initial_velocity": {
        "type": "spherical",
        "magnitude": 20.0,
        "theta_deg": 60.0,
        "phi_deg": 0.0
      }
    }
  ]
}
```

## Usage

Run the simulation with a configuration file:

```bash
python main.py config.json
```

If no configuration file is specified, the program will look for `config.json` in the current directory.
