import numpy as np
from scipy.integrate import solve_ivp
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Mass and initial positions for 3 bodies
m1, m2, m3 = 1.0, 1.0, 1.0
G = 1.0

# Initial positions and velocities
r1 = np.array([-1.0, 0.0])
r2 = np.array([1.0, 0.0])
r3 = np.array([0.0, 0.5])

v1 = np.array([0.0, 0.3])
v2 = np.array([0.0, -0.3])
v3 = np.array([0.5, 0.0])


# System of differential equations
def three_body(t, y):
    r1 = y[0:2]
    r2 = y[2:4]
    r3 = y[4:6]
    v1 = y[6:8]
    v2 = y[8:10]
    v3 = y[10:12]

    def acc(rA, rB, mB):
        r = rB - rA
        return G * mB * r / (np.linalg.norm(r) ** 3 + 1e-5)

    a1 = acc(r1, r2, m2) + acc(r1, r3, m3)
    a2 = acc(r2, r1, m1) + acc(r2, r3, m3)
    a3 = acc(r3, r1, m1) + acc(r3, r2, m2)

    return np.concatenate((v1, v2, v3, a1, a2, a3))


# The initial vector
y0 = np.concatenate((r1, r2, r3, v1, v2, v3))

# Simulation time
t_span = (0, 50)
t_eval = np.linspace(t_span[0], t_span[1], 2000)

sol = solve_ivp(three_body, t_span, y0, t_eval=t_eval, rtol=1e-9)

x1, y1 = sol.y[0], sol.y[1]
x2, y2 = sol.y[2], sol.y[3]
x3, y3 = sol.y[4], sol.y[5]


# Setup animation
fig, ax = plt.subplots(figsize=(6, 6))
ax.set_xlim(-3, 3)
ax.set_ylim(-3, 3)
ax.set_aspect('equal')
ax.set_title("Three Body Problem")

ax.tick_params(axis='both', colors='white', direction='inout', length=6)
ax.spines['bottom'].set_color('white')
ax.spines['left'].set_color('white')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.xaxis.label.set_color('white')
ax.yaxis.label.set_color('white')
ax.grid(False)

ax.set_facecolor('#111111')

np.random.seed(42)
n_stars = 300
stars_x = np.random.uniform(-5, 5, n_stars)
stars_y = np.random.uniform(-5, 5, n_stars)
stars_sizes = np.random.uniform(0.3, 2.0, n_stars)
stars_alpha = np.random.uniform(0.3, 0.8, n_stars)

for x, y, s, a in zip(stars_x, stars_y, stars_sizes, stars_alpha):
    ax.scatter(x, y, s=s, color='white', alpha=a, edgecolors='none')


# Add a frame (border)
ax.spines['top'].set_color('black')
ax.spines['top'].set_linewidth(1)
ax.spines['bottom'].set_color('black')
ax.spines['bottom'].set_linewidth(1)
ax.spines['left'].set_color('black')
ax.spines['left'].set_linewidth(1)
ax.spines['right'].set_color('black')
ax.spines['right'].set_linewidth(1)

# Points and trajectories
p1, = ax.plot([], [], 'ro', markersize=8, label='Body 1')
p2, = ax.plot([], [], 'bo', markersize=8, label='Body 2')
p3, = ax.plot([], [], 'go', markersize=8, label='Body 3')
plt.legend(loc='upper right', frameon=False, fontsize=10, labelcolor='white')


trail1, = ax.plot([], [], 'r-', lw=0.5)
trail2, = ax.plot([], [], 'b-', lw=0.5)
trail3, = ax.plot([], [], 'g-', lw=0.5)


def update(i):
    # Points
    p1.set_data([x1[i]], [y1[i]])
    p2.set_data([x2[i]], [y2[i]])
    p3.set_data([x3[i]], [y3[i]])
    # Routes
    trail1.set_data(x1[:i], y1[:i])
    trail2.set_data(x2[:i], y2[:i])
    trail3.set_data(x3[:i], y3[:i])

    # Automatic limit adjustment depending on the position of the 3 bodies
    margin = 0.5
    all_x = np.concatenate([x1[:i], x2[:i], x3[:i]])
    all_y = np.concatenate([y1[:i], y2[:i], y3[:i]])
    if len(all_x) > 0 and len(all_y) > 0:
        ax.set_xlim(all_x.min() - margin, all_x.max() + margin)
        ax.set_ylim(all_y.min() - margin, all_y.max() + margin)

    return p1, p2, p3, trail1, trail2, trail3


ani = FuncAnimation(fig, update, frames=len(t_eval), interval=20, blit=True)
plt.show()
