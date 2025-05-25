# Numerical Programming

A collection of computational mathematics projects implementing numerical methods and simulations for solving applied mathematical problems in Python.

## Repository Overview

This repository showcases various numerical programming techniques and their applications across different domains of computational mathematics. Each project demonstrates practical implementations of numerical algorithms with real-world applications.

## Repository Structure

```bash
numerical-programming/
├── ball-interceptor/                          # Projectile simulation
│   ├── ball_interceptor.py                    # Main interception engine
│   ├── detect_ball.py                         # Computer vision detection
│   ├── create_falling_ball_video.py           # Video generation utility
│   ├── falling_ball.mp4                       # Sample test video
│   ├── interception.gif                       # Output animation
│   ├── Intercept a moving ball.pptx           # Presentation
│   ├── test_cases/
│   │   ├── 1_high_velocity/
│   │   │   ├── falling_ball_50_50_50_150.mp4
│   │   │   ├── interception_falling_ball_50_50_50_150.gif
│   │   │   └── log.txt
│   │   ├── 2_low_velocity/
│   │   │   ├── falling_ball_50_50_50_300.mp4
│   │   │   ├── interception_falling_ball_50_50_50_300.gif
│   │   │   └── log.txt
│   │   ├── 3_long_distance/
│   │   │   ├── falling_ball_50_50_150_10.mp4
│   │   │   ├── interception_falling_ball_50_50_150_10.gif
│   │   │   └── log.txt
│   │   └── 4_slow_target/
│   │   │   ├── falling_ball_320_50_100_50.mp4
│   │   │   ├── interception_falling_ball_320_50_100_50.gif
│   │   │   └── log.txt
│   └── output_of_test_cases/
│       ├── exact_velocity.gif
│       ├── high_velocity_interception_falling_ball_50_50_50_150.gif
│       ├── interception_delay0.gif
│       ├── long_distance_interception_falling_ball_50_50_150_10.gif
│       ├── low_velocity_interception_falling_ball_50_50_50_300.gif
│       ├── slow_target_interception_falling_ball_320_50_100_50.gif
├── sturm-liouville-solver/                    # Eigenvalue problem solver
│   ├── sturm_liouville_solver.py              # ODE eigenvalue solver
│   └── Sturm-Liouville.pptx                   # Presentation
└── README.md                                  # This overview
```

## Requirements

```bash
pip install numpy matplotlib opencv-python scipy
```

## Projects

### 1. Ball Interceptor System

A comprehensive projectile interception simulation that combines computer vision, kinematics, and optimization to solve real-world targeting problems.

#### Problem Statement

Design a system that can intercept a moving projectile by:
- Detecting and tracking a falling ball from video footage
- Predicting its future trajectory using kinematic equations
- Computing optimal launch parameters (velocity and angle) to intercept the target
- Accounting for realistic constraints like launch delays

#### System Components

**Interception Engine (`ball_interceptor.py`)**
Core interception logic and animation:
- Predicts target position at any future time using kinematic equations
- Performs grid search optimization over launch velocity and angle ranges
- Accounts for launch delays in the interception calculation
- Uses 4th-order Runge-Kutta integration for accurate trajectory simulation

**Computer Vision Detection (`detect_ball.py`)**
- Extracts ball position and velocity from video using OpenCV
- Uses HSV color space filtering and contour detection
- Implements linear regression to estimate initial velocity from early frames
- Converts pixel coordinates to real-world measurements

**Video Generation (`create_falling_ball_video.py`)**
- Generates synthetic video footage of a falling ball with customizable physics
- Configurable initial conditions, gravity, and visual parameters
- Creates test data for the detection system

**Visualization System**
- Real-time matplotlib animation showing both projectile and target trajectories
- Visual confirmation of successful interception
- Trajectory plotting and analysis tools

#### Key Features

- **Motion Prediction**: Calculates future position of targets using physics-based models
- **Optimization**: Grid search algorithm finds optimal launch parameters
- **Delay Compensation**: Handles realistic launch delays in timing calculations
- **Real-time Visualization**: Animated interception scenarios with matplotlib
- **Modular Design**: Separate components for detection, prediction, and visualization

#### Test Cases

Available test cases include:
- Exact velocity matching
- High velocity interceptions
- Interception delays
- Long distance targeting
- Slow target scenarios

Test case parameters can be modified, and outputs are available in the `output_of_test_cases` directory.

#### Usage

```bash
python ball_interceptor.py
```

#### Example Output

```yaml
Detected Initial Position: (6.40, 1.00) meters
Calculated Initial Velocity: (2.00, 1.00) m/s
Launch velocity: 17.34 m/s
Launch angle: 45.2 degrees
Total interception time: 2.15 s
Flight time: 1.15 s
```

#### Applications

- **Defense Systems**: Anti-missile and projectile defense calculations
- **Robotics**: Autonomous catching and interception tasks
- **Sports Analytics**: Trajectory prediction for ball sports
- **Computer Graphics**: Realistic physics simulation in games

### 2. Sturm-Liouville Eigenvalue Solver

Advanced numerical solver for Sturm-Liouville boundary value problems using the shooting method combined with adaptive integration and binary search optimization.

**Key Techniques**: Shooting method, RK45 integration, binary search, eigenfunction normalization

#### Components

- **Input**: Sturm-Liouville problem
- **Task**: Find first 8 eigenvalues and eigenfunctions
- **Approach**: Visualization of eigenvalues and eigenfunctions

#### Problem Statement

Solve the singular Sturm-Liouville equation:

```math
-1/2 * cos⁴(x) * u''(x) - 1/2 * cos³(x)cos(2x)/sin(x) * u'(x) + [m²cos²(x)/(2sin²(x)) - cos(x)/sin(x)] * u(x) = λu(x)
```

**Boundary Conditions**: `u(0) = 0` and `u(π/2) = 0`

This type of equation appears in quantum mechanics, vibration analysis, and heat transfer problems with variable coefficients.

#### Mathematical Approach

**Shooting Method Implementation**
- Converts second-order boundary value problem to initial value problem
- Uses `u(0) = 0, u'(0) = 1` as initial conditions
- Searches for eigenvalues λ where `u(π/2) ≈ 0`

**Adaptive Integration**
- Employs SciPy's `solve_ivp` with RK45 (Runge-Kutta-Fehlberg) method
- Automatically adjusts step size for optimal accuracy
- Handles singular points near domain boundaries

**Binary Search Optimization**
- Iteratively narrows eigenvalue search interval
- Convergence tolerance: `1e-6`
- Robust bracketing strategy with automatic interval expansion

#### Key Features

- **Singularity Handling**: Careful treatment of singular points at x=0 and x=π/2
- **Domain Shrinkage**: Uses [0.0001, π/2-0.0001] to avoid numerical instabilities
- **Eigenfunction Normalization**: L² normalization using trapezoidal integration
- **Progressive Search**: Automatically finds multiple eigenvalues sequentially
- **Comprehensive Visualization**: Multi-panel plots showing all eigenfunctions

#### Numerical Methods Demonstrated

- **Shooting Method**: Boundary value problem reduction technique
- **Adaptive Integration**: RK45 with automatic step size control
- **Binary Search**: Root-finding for eigenvalue determination
- **System Reduction**: Second-order to first-order ODE conversion
- **Numerical Integration**: Trapezoidal rule for normalization

#### Usage

```bash
python sturm_liouville_solver.py
```

#### Example Output

```bash
Initialized solver with domain [0.000100, 1.570696] using 1000 points

Finding 8 eigenvalues and eigenfunctions...

Searching for eigenvalue 1/8
  Iteration 1: λ = -2.500000, u(π/2) = -15.234567
  Iteration 2: λ = 1.250000, u(π/2) = 8.876543
  ...
  Found eigenvalue λ = 0.374593 after 23 iterations

Computing eigenfunction for λ_1 = 0.374593
Normalized eigenfunction with norm factor: 0.816497

Eigenvalues:
λ_1 = 0.374593
λ_2 = 2.811684
λ_3 = 7.248775
```

#### Output Files

- `eigenfunctions.png` - Grid visualization of all computed eigenfunctions
- Console output with detailed iteration tracking and eigenvalue results

#### Applications

- **Quantum Mechanics**: Schrödinger equation with variable potentials
- **Structural Engineering**: Vibration analysis of non-uniform beams
- **Heat Transfer**: Temperature distribution in variable-property materials
- **Mathematical Physics**: Separation of variables in PDE solutions

#### Technical Highlights

- Handles challenging singular differential equations
- Demonstrates robustness of shooting method for eigenvalue problems
- Shows integration of multiple numerical techniques in a single solver
- Provides educational insight into spectral theory computations

## Technologies & Methods

### Languages
- Python

### Core Libraries
- NumPy, SciPy, Matplotlib

### Numerical Methods
- Ordinary Differential Equations (ODEs)
- Eigenvalue problems
- Root finding algorithms
- Numerical integration
- Optimization techniques

## Development

This is an active repository with ongoing additions of new numerical programming projects and methods. Each project focuses on different aspects of computational mathematics while maintaining code quality and educational value.

## Credits

Created as part of advanced simulations and mathematical modeling coursework. Demonstrates numerical integration, differential equation solving, and animation in Python.

## License

MIT License
