import numpy as np
import cv2


def create_falling_ball_video(output_filename,
                              initial_position=(320, 50),
                              initial_velocity=(0, 0),
                              duration=5,
                              fps=60,
                              resolution=(640, 480),
                              ball_radius=20,
                              ball_color=(255, 0, 0),
                              background_color=(255, 255, 255)):
    """
    Generate a video of a falling ball with given initial conditions.

    Parameters:
    -----------
    output_filename : str
        Name of the output MP4 file
    initial_position : tuple
        Initial (x, y) position of the ball in pixels
    initial_velocity : tuple
        Initial (vx, vy) velocity in pixels per second
    duration : float
        Duration of the video in seconds
    fps : int
        Frames per second
    resolution : tuple
        Video resolution (width, height) in pixels
    ball_radius : int
        Radius of the ball in pixels
    ball_color : tuple
        Ball color in BGR format
    background_color : tuple
        Background color in BGR format
    """

    # Constants
    gravity = 9.81 * 100  # Convert to pixels/s^2 (assuming 100 pixels = 1 meter)

    # Calculate number of frames
    n_frames = int(duration * fps)

    # Initialize video writer
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_filename, fourcc, fps, resolution)

    # Time array
    dt = 1 / fps
    times = np.arange(n_frames) * dt

    # Calculate positions
    x = initial_position[0] + initial_velocity[0] * times
    y = (initial_position[1] + initial_velocity[1] * times +
         0.5 * gravity * times ** 2)

    # Create frames
    for i in range(n_frames):
        # Create blank frame
        frame = np.full((resolution[1], resolution[0], 3),
                        background_color,
                        dtype=np.uint8)

        # Current ball position
        ball_x = int(x[i])
        ball_y = int(y[i])

        # Check if ball hits the ground
        if ball_y >= resolution[1] - ball_radius:
            ball_y = resolution[1] - ball_radius

        # Draw the ball
        cv2.circle(frame,
                   (ball_x, ball_y),
                   ball_radius,
                   ball_color,
                   -1)  # -1 means filled circle

        # Write frame
        out.write(frame)

    # Release video writer
    out.release()


# Example usage
if __name__ == "__main__":
    # Example parameters
    params = {
        'output_filename': 'falling_ball.mp4',
        'initial_position': (320, 50),  # Start from middle-top
        'initial_velocity': (100, 50),  # Initial horizontal velocity
        'duration': 3,  # 3 seconds video
        'fps': 60,  # 60 frames per second
        'resolution': (640, 480),  # Standard 640x480 resolution
        'ball_radius': 20,  # 20 pixels radius
        'ball_color': (0, 0, 255),  # Red ball (BGR format)
        'background_color': (255, 255, 255)  # White background
    }

    create_falling_ball_video(**params)