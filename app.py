import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import time
import math
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from PIL import Image

# =======================
# Title
# =======================
st.title("Secondary 3 Maths - Application of Quadratic Equations")
st.write("Visualising quadratic equations using projectile motion")

st.markdown("""
### The scenario: 
                 Imagine playing with a toy rocket launcher. 
                        As one vary height and speed,  
                        the movement of the rocket changes. 
                        
Today, through the use of quadratic graphs, we will able to plot a rough idea on
the relationship between time, speed of rocket, and the height the rocket with released.  
""")

# =======================
# Inputs
# =======================
c = st.slider("Initial height, **c** (m)", 0, 50, 10)
b = st.slider("Initial upward velocity, **b**", 5, 40, 20)

a = -5  # gravity (negative → curve opens downward)

# =======================
# Time Setup
# =======================
t_max_graph = 10.0
t_values = np.linspace(0.0, t_max_graph, 400)

h_values = a * t_values**2 + b * t_values + c
h_values[h_values < 0] = np.nan

# Vertex (maximum height)
t_vertex = -b / (2 * a)
h_vertex = a * t_vertex**2 + b * t_vertex + c

# =======================
# Controls
# =======================
animate = st.checkbox("▶ Animate Rocket")

t_current = st.slider(
    "Time (seconds)",
    min_value=0.0,
    max_value=t_max_graph,
    value=0.0,
    step=0.1
)

plot_area = st.empty()

# =======================
# Load Rocket Image
# =======================
rocket_img = Image.open("rocket.png")

# =======================
# Plot Function
# =======================
def draw_plot(t_now):
    h_now = a * t_now**2 + b * t_now + c

    # Velocity (slope of curve)
    slope = 2 * a * t_now + b

    # Angle of motion from horizontal
    angle_from_horizontal = math.degrees(math.atan(slope))

    # Convert to image rotation (image faces UP)
    image_angle = angle_from_horizontal - 90

    fig, ax = plt.subplots(figsize=(7, 5))

    # Quadratic path
    ax.plot(t_values, h_values, label="Rocket Path")
    ax.scatter(t_vertex, h_vertex, label="Maximum Height")

    # Draw rocket image
    if h_now >= 0:
        rotated_rocket = rocket_img.rotate(
            -image_angle,
            expand=True
        )

        imagebox = OffsetImage(rotated_rocket, zoom=0.08)
        ab = AnnotationBbox(
            imagebox,
            (t_now, h_now),
            frameon=False
        )
        ax.add_artist(ab)

    ax.set_xlim(0, t_max_graph)
    ax.set_ylim(0, max(h_vertex + 15, 70))

    ax.set_xlabel("Time (seconds)")
    ax.set_ylabel("Height (meters)")
    ax.set_title("Height–Time Graph (Quadratic)")
    ax.legend()
    ax.grid(True)

    plot_area.pyplot(fig)

# =======================
# Animation
# =======================
if animate:
    for t in np.linspace(0.0, t_max_graph, 100):
        draw_plot(t)
        time.sleep(0.04)
else:
    draw_plot(t_current)

# =======================
# Explanation
# =======================
st.header("Explanations:")

st.markdown(f"""
### Quadratic Equation
**h(t) = {a}t² + {b}t + {c}**

In which the standard quadratic equation is: **h(t) = at² + bt + c**
- **a** → Gravity (In simple terms: negative → downward opening curve)

            Why? --> The Gravitational Field is a region in which a mass experiences gravitational acceleration.
                     In this case, gravity pulls the objects down towards the Earth's core. Hence, the 
                     trajectory of the rocket is that it will accelerate upwards, and descend after reaching
                     its maximum height. Hence, the graph plots a negative parabolic curve. 
- **b** → Initial upward velocity

            How? --> The value **b** represents how fast the rocket is moving upwards at launch.
                - Larger **b** will show a steeper graph, in which we will find a greater maximum height.

- **c** → Initial height (The initial starting point of the rocket) 

            Example --> Rocket launched on a building? On the ground? 
""")

st.markdown("""
### 🚀 Direction of Motion
The rocket points in the **direction of velocity**.

Velocity is the gradient of the height–time graph:
**v(t) = 2at + b**

- v > 0 → rocket rises
- v = 0 → maximum height
- v < 0 → rocket falls
""")

st.write(f"""
**Maximum height:** {h_vertex:.2f} m  
**Time of maximum height:** {t_vertex:.2f} s
""")



st.markdown("""
### Extension Question: 
    Using your values from the graph: 
    a) Calculate the maximum height that the rocket can go. 
    b) Calculate the time taken for the rocket to fall on the ground. 
""")