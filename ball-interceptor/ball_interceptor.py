import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from scipy.integrate import solve_ivp


class BallInterceptor:
    def __init__(self, g=9.81):
        self.g = g

    def predict_target_position(self, initial_pos, initial_vel, t):
        """Predict target position at time t given initial conditions"""
        x = initial_pos[0] + initial_vel[0] * t
        y = initial_pos[1] + initial_vel[1] * t - 0.5 * self.g * t ** 2
        return np.array([x, y])

    def ball_motion(self, t, y):
        """Differential equations for projectile motion"""
        return [y[1], 0, y[3], -self.g]

    def find_interception(self, target_pos, target_vel, delay=0.0, v0_range=(10, 30), angle_range=(0, 90)):
        """Find launch parameters to intercept moving target, accounting for initial delay"""
        best_dist = float('inf')
        best_params = None
        best_time = None

        # Create more granular search space for better accuracy
        v0s = np.linspace(*v0_range, 30)
        angles = np.linspace(*angle_range, 30)
        times = np.linspace(delay, 10.0 + delay, 1000)  # Extended time range with finer granularity

        for t_intercept in times:
            # Calculate target position at interception time (measured from start)
            target_future = self.predict_target_position(target_pos, target_vel, t_intercept)

            for v0 in v0s:
                for angle in angles:
                    # Calculate ball position after flight time (excluding delay)
                    flight_time = t_intercept - delay
                    if flight_time <= 0:
                        continue

                    angle_rad = np.deg2rad(angle)
                    vx = v0 * np.cos(angle_rad)
                    vy = v0 * np.sin(angle_rad)

                    # Ball position at flight_time
                    x = vx * flight_time
                    y = vy * flight_time - 0.5 * self.g * flight_time ** 2

                    ball_pos = np.array([x, y])
                    dist = np.linalg.norm(ball_pos - target_future)

                    if dist < best_dist:
                        best_dist = dist
                        best_params = (v0, angle)
                        best_time = t_intercept

                    if dist < 0.01:  # Hit threshold
                        return v0, angle, t_intercept

        return best_params[0], best_params[1], best_time

    def compute_trajectory(self, v0, angle, t_max=2.0):
        """Compute full trajectory with corrected equations"""
        angle_rad = np.deg2rad(angle)
        vx = v0 * np.cos(angle_rad)
        vy = v0 * np.sin(angle_rad)

        t = np.linspace(0, t_max, 100)
        x = vx * t
        y = vy * t - 0.5 * self.g * t ** 2

        return np.array([x, y]), t

    def animate_interception(self, v0, angle, target_pos, target_vel, t_intercept, delay=0.0):
        """Create animation of the interception with initial delay"""
        # Compute actual flight time (excluding delay)
        flight_time = t_intercept - delay

        # Compute shooter trajectory for the flight time
        shooter_traj, t = self.compute_trajectory(v0, angle, t_max=flight_time)

        # Calculate number of frames for delay (20 fps = 50ms interval)
        n_delay_frames = int(delay * 20)

        # Create arrays for delayed shooter position
        shooter_x = np.concatenate([np.zeros(n_delay_frames), shooter_traj[0]])
        shooter_y = np.concatenate([np.zeros(n_delay_frames), shooter_traj[1]])

        # Target trajectory for full time including delay
        n_total_frames = len(shooter_x)
        target_t = np.linspace(0, t_intercept, n_total_frames)
        target_x = target_pos[0] + target_vel[0] * target_t
        target_y = target_pos[1] + target_vel[1] * target_t - 0.5 * self.g * target_t ** 2

        fig, ax = plt.subplots(figsize=(10, 6))
        shooter_line, = ax.plot([], [], 'b-', label='Shooter')
        shooter_ball, = ax.plot([], [], 'bo', markersize=10)
        target_line, = ax.plot([], [], 'r-', label='Target')
        target_ball, = ax.plot([], [], 'ro', markersize=10)

        ax.set_xlim(min(min(shooter_x), min(target_x)) - 1,
                    max(max(shooter_x), max(target_x)) + 1)
        ax.set_ylim(min(min(shooter_y), min(target_y)) - 1,
                    max(max(shooter_y), max(target_y)) + 1)
        ax.grid(True)
        ax.legend()

        def init():
            shooter_line.set_data([], [])
            shooter_ball.set_data([], [])
            target_line.set_data([], [])
            target_ball.set_data([], [])
            return shooter_line, shooter_ball, target_line, target_ball

        def animate(frame):
            shooter_line.set_data(shooter_x[:frame], shooter_y[:frame])
            shooter_ball.set_data([shooter_x[frame - 1]], [shooter_y[frame - 1]])
            target_line.set_data(target_x[:frame], target_y[:frame])
            target_ball.set_data([target_x[frame - 1]], [target_y[frame - 1]])
            return shooter_line, shooter_ball, target_line, target_ball

        anim = FuncAnimation(fig, animate, init_func=init,
                             frames=len(target_t),
                             interval=50, blit=True)
        return anim



# Example usage
if __name__ == "__main__":
    interceptor = BallInterceptor()

    from CP2 import detect


    # Initial conditions for target
    target_pos, target_vel = detect("falling_ball.mp4")
    print(target_pos)
    print(target_vel)
    # Find interception parameters with a 1-second delay
    delay_time = 1
    v0, angle, t_intercept = interceptor.find_interception(
        target_pos, target_vel,
        delay=delay_time,
        v0_range=(0, 100),  # Adjusted velocity range
        angle_range=(-90, 90)  # Adjusted angle range
    )

    print(f"Launch velocity: {v0:.2f} m/s")
    print(f"Launch angle: {angle:.2f} degrees")
    print(f"Total interception time: {t_intercept:.2f} s")
    print(f"Flight time: {(t_intercept - delay_time):.2f} s")

    # Create and save animation
    anim = interceptor.animate_interception(v0, angle, target_pos, target_vel, t_intercept, delay=delay_time)
    anim.save('interception.gif', writer='pillow')