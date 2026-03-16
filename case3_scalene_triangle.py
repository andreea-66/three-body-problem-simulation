import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from scipy.integrate import solve_ivp

# Constants and parameters
G = 1
m1 = m2 = m3 = 1.0  # Identical body mass

# Initial positions forming a scalene triangle
pos0 = np.array([[1.0, 0.5], [-1.2, -0.7], [0.2, -1.2]])

vel0 = np.zeros((3, 2))
initial_state = np.concatenate((pos0.flatten(), vel0.flatten()))

# Function for calculating derivatives (velocity and acceleration)
def derivatives(t, state):
    pos = state[:6].reshape((3, 2))
    vel = state[6:].reshape((3, 2))
    acc = np.zeros_like(pos)
    for i in range(3):
        for j in range(3):
            if i != j:
                r_vec = pos[j] - pos[i]
                r_mag = np.linalg.norm(r_vec)
                acc[i] += G * r_vec / r_mag**3
    return np.concatenate((vel.flatten(), acc.flatten()))

# Long-term simulation to obtain complex trajectories
sol = solve_ivp(derivatives, [0, 100], initial_state, t_eval=np.linspace(0, 100, 5000))
positions = sol.y[:6].reshape((3, 2, -1))

# Center of mass calculation at each step
masses = np.array([m1, m2, m3])
cm_x = np.sum(masses[:, np.newaxis] * positions[:, 0, :], axis=0) / np.sum(masses)
cm_y = np.sum(masses[:, np.newaxis] * positions[:, 1, :], axis=0) / np.sum(masses)

# Refocus to fix the center of mass
positions[0, 0, :] -= cm_x
positions[0, 1, :] -= cm_y
positions[1, 0, :] -= cm_x
positions[1, 1, :] -= cm_y
positions[2, 0, :] -= cm_x
positions[2, 1, :] -= cm_y

# Figure creation and graphic settings
fig, ax = plt.subplots(figsize=(6, 6))
ax.set_xlim(-2, 2)
ax.set_ylim(-2, 2)
ax.set_aspect('equal')
ax.set_title("Three-Body Problem")
lines = [ax.plot([], [], 'o', markersize=8)[0] for _ in range(3)]
cm_point, = ax.plot(0, 0, 'rx', markersize=10)
trails = [ax.plot([], [], '-', linewidth=1, alpha=0.7)[0] for _ in range(3)]
trail_data = [([], []) for _ in range(3)]

# Animation update function
def update(frame):
    for i, line in enumerate(lines):
        x, y = positions[i, 0, frame], positions[i, 1, frame]
        line.set_data([x], [y])
        trail_data[i][0].append(x)
        trail_data[i][1].append(y)
        trails[i].set_data(trail_data[i][0], trail_data[i][1])
    cm_point.set_data([0], [0])  # Centru de masa fix in (0,0)
    return lines + trails + [cm_point]

# Creating the animation
ani = FuncAnimation(fig, update, frames=len(sol.t), blit=True, interval=20)
plt.show()