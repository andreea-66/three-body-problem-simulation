import numpy as np                           # Library for fast numerical and matrix calculations
import matplotlib.pyplot as plt              # Graphics and visualization library
from matplotlib.animation import FuncAnimation  # For animations in matplotlib
from scipy.integrate import solve_ivp        # For numerical integration of differential equations

# Constants
G = 1.0
m1 = 1.0                                     # Star 1
m2 = 1.0                                     # Star 2
m3 = 0.001                                   # Small planet

# Initial positions and velocities
r1 = np.array([-0.5, 0.0])
v1 = np.array([0.0, 0.3])

r2 = np.array([0.5, 0.0])
v2 = np.array([0.0, -0.3])

r3 = np.array([0.0, 1.0])
v3 = np.array([0.5, 0.0])

# Concatenate all positions and velocities into a single vector for numerical integration
y0 = np.concatenate((r1, r2, r3, v1, v2, v3))

# We define the function that calculates the time derivatives (the equations of motion)
def derivatives(t, y):
    # Extract the positions and velocities from the y vector
    r1 = y[0:2]
    r2 = y[2:4]
    r3 = y[4:6]

    v1 = y[6:8]
    v2 = y[8:10]
    v3 = y[10:12]

    # We calculate the distance vectors between the bodies
    r12 = r2 - r1
    r13 = r3 - r1
    r23 = r3 - r2

    # We calculate scalar distances (vector norms)
    d12 = np.linalg.norm(r12)
    d13 = np.linalg.norm(r13)
    d23 = np.linalg.norm(r23)

    # We calculate the accelerations according to the law of gravity:
    a1 = G * m2 * r12 / d12**3 + G * m3 * r13 / d13**3
    a2 = G * m1 * (-r12) / d12**3 + G * m3 * r23 / d23**3
    a3 = G * m1 * (-r13) / d13**3 + G * m2 * (-r23) / d23**3

    # The state derivative is the concatenated vector of velocities and accelerations
    dydt = np.concatenate((v1, v2, v3, a1, a2, a3))
    return dydt

# Define the time interval for the simulation
t_span = (0, 100)
t_eval = np.linspace(t_span[0], t_span[1], 5000)

# We numerically integrate the system of differential equations using solve_ivp
sol = solve_ivp(derivatives, t_span, y0, t_eval=t_eval, rtol=1e-9, atol=1e-9)

# Extract the positions of all bodies from the calculated solution
r1_sol = sol.y[0:2, :]
r2_sol = sol.y[2:4, :]
r3_sol = sol.y[4:6, :]

# Configure the graph to display the animation
fig, ax = plt.subplots()
ax.set_aspect('equal')

ax.set_facecolor('black')

# We generate white stars as discrete dots on the background, with varying positions, sizes, and transparencies
np.random.seed(42)
n_stars = 300
stars_x = np.random.uniform(-2.5, 2.5, n_stars)
stars_y = np.random.uniform(-2.5, 2.5, n_stars)
stars_sizes = np.random.uniform(0.3, 1.2, n_stars)
stars_alpha = np.random.uniform(0.3, 0.9, n_stars)

for x, y, s, a in zip(stars_x, stars_y, stars_sizes, stars_alpha):
    ax.scatter(x, y, s=s, color='white', alpha=a, edgecolors='none')

# We set the initial limits of the graph
ax.set_xlim(-2, 2)
ax.set_ylim(-2, 2)

# Style the axes: white color, no grid, no top/right borders
ax.tick_params(axis='both', colors='white', direction='inout', length=6)
ax.spines['bottom'].set_color('white')
ax.spines['left'].set_color('white')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.xaxis.label.set_color('white')
ax.yaxis.label.set_color('white')
ax.grid(False)
ax.set_title("Three Body Problem")

# We define the points and paths of the bodies for animation
line1, = ax.plot([], [], 'ro', markersize=8, label='Star 1')
line2, = ax.plot([], [], 'bo', markersize=8, label='Star 2')
line3, = ax.plot([], [], 'go', markersize=4, label='Planet')

# Lines for body tracks
trail1, = ax.plot([], [], 'r-', linewidth=1, alpha=0.6)
trail2, = ax.plot([], [], 'b-', linewidth=1, alpha=0.6)
trail3, = ax.plot([], [], 'g-', linewidth=1, alpha=0.6)

# Lists that will store positions for routes
trail_data_1 = ([], [])
trail_data_2 = ([], [])
trail_data_3 = ([], [])

# Animation initialization function
def init():
    line1.set_data([], [])
    line2.set_data([], [])
    line3.set_data([], [])
    trail1.set_data([], [])
    trail2.set_data([], [])
    trail3.set_data([], [])
    return line1, line2, line3, trail1, trail2, trail3

# Function called at each frame of the animation
def update(frame):
    # We take the positions at the current time
    x1, y1 = r1_sol[0, frame], r1_sol[1, frame]
    x2, y2 = r2_sol[0, frame], r2_sol[1, frame]
    x3, y3 = r3_sol[0, frame], r3_sol[1, frame]

    # Update the positions of the points (bodies)
    line1.set_data([x1], [y1])
    line2.set_data([x2], [y2])
    line3.set_data([x3], [y3])

    # We add new positions to the routes
    trail_data_1[0].append(x1)
    trail_data_1[1].append(y1)
    trail_data_2[0].append(x2)
    trail_data_2[1].append(y2)
    trail_data_3[0].append(x3)
    trail_data_3[1].append(y3)

    # We update the route lines
    trail1.set_data(trail_data_1[0], trail_data_1[1])
    trail2.set_data(trail_data_2[0], trail_data_2[1])
    trail3.set_data(trail_data_3[0], trail_data_3[1])

    # We calculate the center of the bodies for zooming and refocusing
    all_x = np.array([x1, x2, x3])
    all_y = np.array([y1, y2, y3])
    center_x = np.mean(all_x)
    center_y = np.mean(all_y)

    # Determine the maximum window size (the largest interval between bodies on the x or y axes)
    max_dist = max(np.max(all_x) - np.min(all_x), np.max(all_y) - np.min(all_y))
    margin = 1.0

    # We set the zoom to include all bodies with a safety margin
    zoom_range = max(max_dist + margin, 2.5)

    xmin = center_x - zoom_range / 2
    xmax = center_x + zoom_range / 2
    ymin = center_y - zoom_range / 2
    ymax = center_y + zoom_range / 2

    # Update the axis limits with the calculated values for dynamic zoom
    ax.set_xlim(xmin, xmax)
    ax.set_ylim(ymin, ymax)

    return line1, line2, line3, trail1, trail2, trail3

# We create the animation using FuncAnimation
ani = FuncAnimation(fig, update, frames=len(t_eval), init_func=init, blit=True, interval=20)

# Show legend
plt.legend()

# Show animation
plt.show()

#This code simulates the motion of a system consisting of two stars and a small planet using the laws of gravity and animations in Python.