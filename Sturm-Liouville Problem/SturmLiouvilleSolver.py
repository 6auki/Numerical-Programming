import numpy as np
from scipy.integrate import solve_ivp
import matplotlib
import matplotlib.pyplot as plt

matplotlib.use('TkAgg')


class SturmLiouvilleSolver:
    def __init__(self, x_start=0.0001, x_end=np.pi / 2 - 0.0001, num_points=1000):
        """
        Initializing the solver with domain parameters
        slightly shrinking the domain to avoid singular points
        """
        self.x_start = x_start
        self.x_end = x_end
        self.num_points = num_points
        self.x = np.linspace(x_start, x_end, num_points)
        self.m = 1
        print(f"Initialized solver with domain [{x_start:.6f}, {x_end:.6f}] using {num_points} points")


    def equation_system(self, x, y, lambda_val):
        """
        converting second-order ODE to a system of first-order ODEs.
        y[0] = u
        y[1] = du/dx
        """
        u, du = y

        cos_x = np.cos(x)
        sin_x = np.sin(x)
        cos_2x = np.cos(2 * x)

        if abs(sin_x) < 1e-10:
            sin_x = 1e-10

        # calculating second derivative coefficient
        p = -0.5 * cos_x ** 4

        # first derivative coefficient
        q = -0.5 * (cos_x ** 3 * cos_2x / sin_x)

        # calculating function coefficient
        r = (self.m ** 2 * cos_x ** 2) / (2 * sin_x ** 2) - cos_x / sin_x

        # system of first-order ODEs
        return [
            du,
            (-q * du - (r - lambda_val) * u) / p
        ]

    def solve_ivp_with_shooting(self, lambda_val, initial_slope=1.0):
        # initial conditions are: u(0) = 0, u'(0) = slope
        y0 = [0, initial_slope]

        solution = solve_ivp(
            fun=lambda x, y: self.equation_system(x, y, lambda_val),
            t_span=(self.x_start, self.x_end),
            y0=y0,
            method='RK45',
            t_eval=self.x
        )

        return solution.y[0], solution.y[1]  # Return u and du/dx

    def find_eigenvalue(self, lambda_guess, tolerance=1e-6, max_iterations=100):
        # using shooting method with binary search

        print(f"\nSearching for eigenvalue near λ = {lambda_guess:.6f}")
        lambda_left = lambda_guess - 5
        lambda_right = lambda_guess + 5
        iteration = 0

        for iteration in range(max_iterations):
            lambda_mid = (lambda_left + lambda_right) / 2
            u, _ = self.solve_ivp_with_shooting(lambda_mid)
            end_value = u[-1]

            print(f"  Iteration {iteration + 1}: λ = {lambda_mid:.6f}, u(π/2) = {end_value:.6f}")

            # checking if we found an eigenvalue (u(π/2) ≈ 0)
            if abs(end_value) < tolerance:
                print(f"  Found eigenvalue λ = {lambda_mid:.6f} after {iteration + 1} iterations")
                return lambda_mid

            # updating search interval based on end value
            if end_value > 0:
                lambda_right = lambda_mid
            else:
                lambda_left = lambda_mid

        raise ValueError(f"Failed to converge for lambda_guess = {lambda_guess} after {max_iterations} iterations")

    def find_multiple_eigenvalues(self, num_eigenvalues=8):
        # finding multiple eigenvalues and their corresponding eigenfunctions.

        print(f"\nFinding {num_eigenvalues} eigenvalues and eigenfunctions...")
        eigenvalues = []
        eigenfunctions = []

        # inital guess for the first eigenvalue
        lambda_guess = 1.0

        for i in range(num_eigenvalues):
            print(f"\nSearching for eigenvalue {i + 1}/{num_eigenvalues}")

            # finding eigenvalue
            lambda_val = self.find_eigenvalue(lambda_guess)
            eigenvalues.append(lambda_val)

            # finding corresponding eigenfunction
            print(f"Computing eigenfunction for λ_{i + 1} = {lambda_val:.6f}")
            u, _ = self.solve_ivp_with_shooting(lambda_val)

            # normalizing eigenfunction
            norm = np.sqrt(np.trapezoid(u ** 2, self.x))
            u = u / norm
            print(f"Normalized eigenfunction with norm factor: {norm:.6f}")

            eigenfunctions.append(u)

            # updating guess for next eigenvalue
            lambda_guess = lambda_val + 5
            print(f"Next eigenvalue guess: {lambda_guess:.6f}")

        print("\nCompleted eigenvalue and eigenfunction calculations!")
        return np.array(eigenvalues), np.array(eigenfunctions)

    def plot_results(self, eigenvalues, eigenfunctions):
        print("\nPlotting results...")

        plt.figure(figsize=(15, 10))

        for i, (lambda_val, u) in enumerate(zip(eigenvalues, eigenfunctions)):
            plt.subplot(2, 4, i + 1)
            plt.plot(self.x, u, 'b-', label=f'λ_{i + 1} = {lambda_val:.2f}')
            plt.grid(True)
            plt.title(f'Eigenfunction {i + 1}')
            plt.xlabel('x')
            plt.ylabel('u(x)')
            plt.legend()

        plt.tight_layout()
        plt.savefig('eigenfunctions.png')
        plt.close()
        print("Plot saved as 'eigenfunctions.png'")

        print("\nEigenvalues:")
        for i, lambda_val in enumerate(eigenvalues):
            print(f"λ_{i + 1} = {lambda_val:.6f}")


if __name__ == "__main__":
    print("Starting Sturm-Liouville problem solver...")
    solver = SturmLiouvilleSolver()
    eigenvalues, eigenfunctions = solver.find_multiple_eigenvalues()
    solver.plot_results(eigenvalues, eigenfunctions)
    print("\nSolver completed successfully!")