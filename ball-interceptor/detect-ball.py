import cv2
import numpy as np
from typing import List, Tuple


def detect_ball(frame: np.ndarray) -> Tuple[int, int]:
    """
    Detect the ball in a frame using color detection and contour analysis
    Returns the center coordinates of the ball (x, y)
    """
    # Convert to HSV color space for better color detection
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Define red color range (assuming red ball from previous script)
    # For red color we need two ranges as it wraps around in HSV
    lower_red1 = np.array([0, 100, 100])
    upper_red1 = np.array([10, 255, 255])
    lower_red2 = np.array([160, 100, 100])
    upper_red2 = np.array([180, 255, 255])

    # Create masks for red color
    mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
    mask = cv2.add(mask1, mask2)

    # Find contours
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        # Get the largest contour (should be the ball)
        largest_contour = max(contours, key=cv2.contourArea)

        # Calculate centroid
        M = cv2.moments(largest_contour)
        if M["m00"] != 0:
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])
            return (cx, cy)

    return None


def pixel_to_meters(pixel_pos: Tuple[int, int], scale: float) -> Tuple[float, float]:
    """Convert pixel coordinates to meters"""
    return (pixel_pos[0] / scale, pixel_pos[1] / scale)


def calculate_velocity(positions: List[Tuple[float, float]], dt: float) -> Tuple[float, float]:
    """
    Calculate initial velocity using linear regression on the first few positions
    to minimize the effect of gravity
    """
    if len(positions) < 2:
        return None

    # Use only the first few frames to minimize gravity effect
    use_frames = min(10, len(positions))
    times = np.array(range(use_frames)) * dt

    # Separate x and y coordinates
    x_coords = np.array([p[0] for p in positions[:use_frames]])
    y_coords = np.array([p[1] for p in positions[:use_frames]])

    # Linear regression for x-coordinate (constant velocity)
    vx = np.polyfit(times, x_coords, 1)[0]

    # For y-coordinate, use quadratic fit to account for gravity
    # and take the derivative at t=0 for initial velocity
    y_coeffs = np.polyfit(times, y_coords, 2)
    vy = y_coeffs[1]  # First derivative at t=0

    return (vx, vy)


def detect(path):
    # Video parameters (matching the generation script)
    SCALE = 50  # pixels per meter (same as in generation script)
    FPS = 60
    DT = 1 / FPS

    # Open the video file
    video = cv2.VideoCapture(path)
    if not video.isOpened():
        print("Error: Could not open video file")
        return

    # Store ball positions
    positions_pixels = []
    positions_meters = []
    frame_count = 0

    while video.isOpened() and frame_count < 60:
        ret, frame = video.read()
        if not ret:
            break

        # Detect ball
        ball_center = detect_ball(frame)
        if ball_center:
            positions_pixels.append(ball_center)
            positions_meters.append(pixel_to_meters(ball_center, SCALE))

        frame_count += 1

        # Visualize detection (for debugging)
        if ball_center:
            cv2.circle(frame, ball_center, 5, (0, 255, 0), -1)
            cv2.imshow('Detection', frame)
            cv2.waitKey(1)

    video.release()
    cv2.destroyAllWindows()

    if positions_meters:
        # Calculate initial position (first detected position)
        initial_pos = positions_meters[0]

        # Calculate initial velocity
        initial_vel = calculate_velocity(positions_meters, DT)

        print(f"Detected Initial Position: ({initial_pos[0]:.2f}, {initial_pos[1]:.2f}) meters")
        print(f"Calculated Initial Velocity: ({initial_vel[0]:.2f}, {initial_vel[1]:.2f}) meters/second")

        # Plot the detected positions
        import matplotlib.pyplot as plt
        plt.figure(figsize=(10, 6))
        x_coords = [p[0] for p in positions_meters]
        y_coords = [p[1] for p in positions_meters]
        plt.plot(x_coords, y_coords, 'bo-', label='Detected positions')
        plt.xlabel('X position (meters)')
        plt.ylabel('Y position (meters)')
        plt.title('Detected Ball Trajectory')
        plt.grid(True)
        plt.legend()
        plt.savefig('trajectory.png')
        plt.close()

        return initial_pos, initial_vel
    else:
        print("No ball detected in the video")


