# Sturm-Liouville Eigenvalue Solver

Advanced numerical solver for Sturm-Liouville boundary value problems using the shooting method combined with adaptive integration and binary search optimization.

## Problem Statement

Solve the singular Sturm-Liouville equation:

```math
-1/2 * cos⁴(x) * u''(x) - 1/2 * cos³(x)cos(2x)/sin(x) * u'(x) + [m²cos²(x)/(2sin²(x)) - cos(x)/sin(x)] * u(x) = λu(x)
```

**Boundary Conditions:** `u(0) = 0` and `u(π/2) = 0`

This type of equation appears in quantum mechanics, vibration analysis, and heat transfer problems with variable coefficients.

## Requirements

```bash
pip install numpy scipy matplotlib
```

## Project Structure

```
sturm-liouville-solver/
├── sturm_liouville_solver.py   # Main solver implementation
├──                             # Your generated output visualization
├── Sturm-Liouville.pptx        # Project presentation
└── README.md                   # This file
```

## Mathematical Approach

### Shooting Method Implementation

- Converts second-order boundary value problem to initial value problem
- Uses `u(0) = 0, u'(0) = 1` as initial conditions
- Searches for eigenvalues λ where `u(π/2) ≈ 0`

### Adaptive Integration

- Employs SciPy's `solve_ivp` with RK45 (Runge-Kutta-Fehlberg) method
- Automatically adjusts step size for optimal accuracy
- Handles singular points near domain boundaries

### Binary Search Optimization

- Iteratively narrows eigenvalue search interval
- Convergence tolerance: `1e-6`
- Robust bracketing strategy with automatic interval expansion

## Usage

### Basic Execution

```bash
python sturm_liouville_solver.py
```

### Custom Parameters

Modify the solver initialization:

```python
# Initialize solver with custom domain
solver = SturmLiouvilleSolver(
    x_start=0.0001,           # Domain start (avoid singularity)
    x_end=np.pi/2 - 0.0001,   # Domain end (avoid singularity)
    num_points=1000           # Grid resolution
)

# Find multiple eigenvalues
eigenvalues, eigenfunctions = solver.find_multiple_eigenvalues(num_eigenvalues=8)
```

## Key Features

- **Singularity Handling**: Careful treatment of singular points at x=0 and x=π/2
- **Domain Shrinkage**: Uses `[0.0001, π/2-0.0001]` to avoid numerical instabilities
- **Eigenfunction Normalization**: L² normalization using trapezoidal integration
- **Progressive Search**: Automatically finds multiple eigenvalues sequentially
- **Comprehensive Visualization**: Multi-panel plots showing all eigenfunctions
- **Verbose Output**: Detailed iteration tracking and convergence monitoring

## Example Output

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
λ_4 = 15.312867
```

## Output Files

- `eigenfunctions.png` - Grid visualization of all computed eigenfunctions
- Console output with detailed iteration tracking and eigenvalue results

## Numerical Methods Demonstrated

- **Shooting Method**: Boundary value problem reduction technique
- **Adaptive Integration**: RK45 with automatic step size control
- **Binary Search**: Root-finding for eigenvalue determination
- **System Reduction**: Second-order to first-order ODE conversion
- **Numerical Integration**: Trapezoidal rule for normalization
- **Singularity Treatment**: Domain modification and limit handling

## Applications

- **Quantum Mechanics**: Schrödinger equation with variable potentials
- **Structural Engineering**: Vibration analysis of non-uniform beams
- **Heat Transfer**: Temperature distribution in variable-property materials
- **Mathematical Physics**: Separation of variables in PDE solutions
- **Spectral Theory**: Eigenvalue analysis of differential operators

## Class Structure

### SturmLiouvilleSolver

**Key Methods:**

- `equation_system(x, y, lambda_val)`: Converts second-order ODE to first-order system
- `solve_ivp_with_shooting(lambda_val)`: Integrates ODE system for given eigenvalue
- `find_eigenvalue(lambda_guess)`: Uses binary search to find individual eigenvalue
- `find_multiple_eigenvalues(num_eigenvalues)`: Finds sequence of eigenvalues
- `plot_results(eigenvalues, eigenfunctions)`: Creates visualization plots

**Key Attributes:**

- `x_start`, `x_end`: Domain boundaries (avoiding singularities)
- `num_points`: Grid resolution for numerical integration
- `m`: Parameter in the differential equation

## Technical Highlights

- Handles challenging singular differential equations with variable coefficients
- Demonstrates robustness of shooting method for eigenvalue problems
- Shows integration of multiple numerical techniques in a single solver
- Provides educational insight into spectral theory computations
- Efficient eigenvalue search with automatic bracketing

## Algorithm Details

### Shooting Method Process

1. Convert boundary value problem to initial value problem
2. Guess eigenvalue λ and integrate from x=0 to x=π/2
3. Check if boundary condition u(π/2)=0 is satisfied
4. Use binary search to refine eigenvalue guess
5. Repeat until convergence

### Singularity Treatment

The equation has singularities at x=0 and x=π/2. The solver:
- Shrinks domain slightly to avoid singular points
- Uses epsilon values for numerical stability
- Handles division by zero with conditional logic

## Contributing

Areas for enhancement:
- Implementation of other boundary value problem solvers
- Extension to systems of ODEs
- Alternative eigenvalue algorithms (inverse iteration, QR method)
- Performance optimization for large-scale problems

## License

MIT License
