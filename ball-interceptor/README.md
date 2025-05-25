
# Ball Interceptor
A comprehensive projectile interception simulation that combines computer vision, kinematics, and optimization to solve real-world targeting problems.

## Problem Statement
Design a system that can intercept a moving projectile by:
- Detecting and tracking a falling ball from video footage
- Predicting its future trajectory using kinematic equations
- Computing optimal launch parameters (velocity and angle) to intercept the target
- Accounting for realistic constraints like launch delays

## Requirements

```bash
pip install numpy matplotlib opencv-python scipy
```

## Project Structure
```
ball-interceptor/
├── Output of test cases
├── test cases
├── ball_interceptor.py              # Main interception engine
├── CP2.py                          # Computer vision detection
├── create_falling_ball_video.py    # Video generation utility
├── falling_ball.mp4                # Sample test video
├── interception.gif                # Output animation
├── Intercept a moving ball.pptx     # Project presentation
└── README.md                       # This file
```

## System Components

### Interception Engine (`ball_interceptor.py`)

Core interception logic and animation system:
- Predicts target position at any future time using kinematic equations
- Performs grid search optimization over launch velocity and angle ranges
- Accounts for launch delays in the interception calculation
- Creates real-time matplotlib animations

**Key Classes and Methods:**
- `BallInterceptor`: Main class handling physics and optimization
- `predict_target_position()`: Kinematic trajectory prediction
- `find_interception()`: Grid search optimization algorithm
- `animate_interception()`: Real-time visualization system

### Computer Vision Detection (`CP2.py`)

Ball tracking and motion analysis system:
- Extracts ball position and velocity from video using OpenCV
- Uses HSV color space filtering and contour detection
- Implements linear regression to estimate initial velocity from early frames
- Converts pixel coordinates to real-world measurements

**Key Functions:**
- `detect_ball()`: Color-based ball detection in video frames
- `pixel_to_meters()`: Coordinate system conversion
- `calculate_velocity()`: Linear regression for velocity estimation
- `detect()`: Main function that processes entire video

### Video Generation (`create_falling_ball_video.py`)

Synthetic test data creation:
- Generates realistic video footage of falling balls
- Configurable initial conditions, gravity, and visual parameters
- Creates controlled test scenarios for system validation

## Usage

### Generate Test Video

```bash
python create_falling_ball_video.py
```

### Run Interception Simulation

```bash
python ball_interceptor.py
```

### Custom Parameters

Modify parameters in the main execution block:

```python
# Adjust interception parameters
delay_time = 1.0  # Launch delay in seconds
v0_range = (0, 100)  # Velocity search range
angle_range = (-90, 90)  # Angle search range
```

## Key Features

- **Motion Prediction**: Physics-based trajectory forecasting
- **Grid Search Optimization**: Exhaustive parameter space exploration
- **Delay Compensation**: Realistic launch timing constraints
- **Real-time Visualization**: Animated interception scenarios
- **Modular Design**: Separate components for detection, prediction, and visualization
- **Test Data Generation**: Synthetic video creation for validation

## Example Output

```yaml
Detected Initial Position: (6.40, 1.00) meters
Calculated Initial Velocity: (2.00, 1.00) m/s
Launch velocity: 17.34 m/s
Launch angle: 45.2 degrees
Total interception time: 2.15 s
Flight time: 1.15 s
```

## Numerical Methods Demonstrated

- **Grid Search Optimization**: Brute-force parameter optimization
- **Kinematic Modeling**: Projectile motion under gravity
- **Computer Vision**: Color filtering and contour detection
- **Linear Regression**: Velocity estimation from position data
- **Real-time Animation**: Dynamic visualization with matplotlib

## Applications

- **Defense Systems**: Anti-missile and projectile defense calculations
- **Robotics**: Autonomous catching and interception tasks
- **Sports Analytics**: Trajectory prediction for ball sports
- **Computer Graphics**: Realistic physics simulation in games
- **Education**: Interactive physics demonstrations

## Test Cases

The system includes various test scenarios:
- Exact velocity matching
- High-speed interceptions
- Long-distance targeting
- Variable launch delays
- Different initial conditions

Results and logs available in project outputs.

## Technical Highlights

- Handles realistic physics constraints and timing delays
- Robust color-based object detection in video
- Efficient grid search with early termination
- Smooth animation with proper frame timing
- Modular architecture for easy extension

## Contributing

Feel free to submit issues and enhancement requests. Areas for improvement:
- Kalman filtering for better motion prediction
- 3D trajectory extension
- Wind resistance modeling
- Multi-target scenarios

## License

MIT License
