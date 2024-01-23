"""
EXERCISE 1:
Write a code implementing the 2-D forward and centered numerical scheme of the heat equation (see
lecture, Eq. (19) slide 89, for a 1-D scheme). Space step is set to 1, time step is chosen by the user. Experiment
the CFL condition.
"""

import numpy as np
import argparse
import os
import cv2
import matplotlib.pyplot as plt

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def heat_equation_2d(im, c, dt, dx, num_steps):
    u = im.copy()
    for _ in range(num_steps):
        u_temp=u[1:-1, 1:-1] + c * dt / (dx**2) * (
            u[2:, 1:-1] + u[:-2, 1:-1] + u[1:-1, 2:] + u[1:-1, :-2] - 4 * u[1:-1, 1:-1]
        )
    return u_temp

def main(args):
    image_name= args.image
    c = args.c
    dx = args.dx
    dy = args.dy
    dt = args.dt
    num_steps = args.num_steps

    # Load image
    image_path = os.path.join(BASE_DIR, "img", image_name)
    u = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE).astype(np.float32)

    # CFL condition check
    cfl = c * (dt / (dx**2) + dt / (dy**2)) <= 0.5# Courant-Friedrichs-Lewy condition
    # instead of the cfl, we can use the following condition (see report)
    if dt > 10.25:
        print("CFL condition is not satisfied. Choose a smaller time step.")
    else:
        # Simulation
        u=heat_equation_2d(u, c, dt, dx, num_steps)
        # write image on disk
        print("Saving image: ", "results/heat_equation/"+image_name[:-4]+"_"+str(dt)+".png")
        cv2.imwrite("results/heat_equation/"+image_name[:-4]+"_"+str(dt)+".png", u)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="2D Heat Equation Simulation")
    parser.add_argument("--image" , required=True, type=str, help="Image to be processed")
    parser.add_argument("--c", type=float, default=1.0, help="c parameter")
    parser.add_argument("--dx", type=float, default=1.0, help="Space step")
    parser.add_argument("--dy", type=float, default=1.0, help="Space step")
    parser.add_argument("--dt", required=True, type=float, help="Time step (ensure CFL condition is satisfied)")
    parser.add_argument("--num_steps", type=int, default=10, help="Number of time steps")
    args = parser.parse_args()
    main(args)
 