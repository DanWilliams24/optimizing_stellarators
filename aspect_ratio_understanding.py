import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation

def torus_points(R, r, theta, phi):
    x = (R + r * np.cos(theta)) * np.cos(phi)
    y = (R + r * np.cos(theta)) * np.sin(phi)
    z = r * np.sin(theta)
    return x, y, z

def plot_torus(aspect_ratio):
    R = 2.0  # Major radius of the torus
    r = R / aspect_ratio  # Minor radius of the torus

    theta = np.linspace(0, 2 * np.pi, 100)
    phi = np.linspace(0, 2 * np.pi, 100)
    theta, phi = np.meshgrid(theta, phi)
    x, y, z = torus_points(R, r, theta, phi)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_surface(x, y, z, cmap='viridis')

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title(f'Torus (Aspect Ratio: {aspect_ratio:.2f})')

    return fig,

# Create an animation by varying the aspect ratios
aspect_ratios = np.linspace(0.1, 5.0, 200)  # Range of aspect ratios from 0.1 to 5.0
ani = FuncAnimation(plt.gcf(), plot_torus, frames=aspect_ratios, interval=100, blit=True)

# Save the animation as a GIF (optional)
# ani.save('torus_animation.gif', writer='imagemagick')

plt.show()
