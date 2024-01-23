"""
EXERCISE 2:
Write a code implementing the Perona-Malik scheme, such that given in lecture slides 111. You can use
a linear interpolation and/or the simplification given in slide 112, and compare the results
"""
import argparse
import numpy as np
import matplotlib.pyplot as plt
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def lorentz_conductivity(x, K, alpha=1):
    return 1 / (1 + (x / K)**(1+alpha))

def tukey_conductivity(x, K):
    return np.exp(-(x / K)**2)

def linear_interpolation(A, B, alpha):
    return (1 - alpha) * A + alpha * B

def perona_malik_simplification(im, num_iterations, dt, K, g_function, interpolation, alpha):
    image=im.copy()
    for _ in range(num_iterations):
        gradient_N = np.roll(image, shift=-1, axis=0) - image
        gradient_E = np.roll(image, shift=-1, axis=1) - image
        gradient_S = np.roll(image, shift=1, axis=0) - image
        gradient_W = np.roll(image, shift=1, axis=1) - image

        C_N = g_function(np.abs(gradient_N), K, alpha)
        C_E = g_function(np.abs(gradient_E), K,alpha)
        C_S = g_function(np.abs(gradient_S), K,alpha)
        C_W = g_function(np.abs(gradient_W), K,alpha)

        image += dt * (
            C_N * gradient_N +
            C_E * gradient_E +
            C_S * gradient_S +
            C_W * gradient_W
        )

    return image

def perona_malik_interpolation(L, num_iterations, dt, K, g, interpolation=False):
    rows, cols = L.shape
    L_next = np.zeros_like(L)

    for _ in range(num_iterations):
        for i in range(1, rows - 1):
            for j in range(1, cols - 1):
                dNL = L[i-1, j] - L[i, j]
                dEL = L[i, j+1] - L[i, j]
                dSL = L[i+1, j] - L[i, j]
                dWL = L[i, j-1] - L[i, j]
                #apply linear interpolation
                CN=g(((L[i,j]-L[i+1,j])/2) - ((L[i-1,j]-L[i,j+1])/2),K)
                CS=g(((L[i+1,j]-L[i,j])/2) - ((L[i,j]-L[i-1,j])/2),K)
                CE=g(((L[i,j]-L[i,j+1])/2) - ((L[i,j-1]-L[i,j])/2),K)
                CW=g(((L[i,j+1]-L[i,j])/2) - ((L[i,j]-L[i,j-1])/2),K)
                L_next[i, j] = L[i, j] + dt * (CN * dNL + CS * dSL + CE * dEL + CW * dWL)

    return L_next

def main(args):
    input_image_name = args.input
    output_image_name = args.output
    num_iterations = args.num_iterations
    dt = args.dt
    K = args.K
    interpolation = args.interpolation
    alpha = args.alpha

    # Read the image
    image_path = os.path.join(BASE_DIR, "img", input_image_name)
    img = plt.imread(image_path).astype(float)

    # Choose the g function
    if args.g_function == "lorentz":
        g_function = lorentz_conductivity
    elif args.g_function == "tukey":
        g_function = tukey_conductivity
    else:
        raise ValueError("Invalid choice for g function. Choose 'lorentz' or 'tukey'.")

    # Clone the image to preserve the original
    denoised_img = img.copy()

    if len(denoised_img.shape) == 3:
        print("Reducing shape from",denoised_img.shape, "to", denoised_img[:,:,0].shape, "for processing.")
        denoised_img = denoised_img[:,:,0] # use gray

    # Apply Perona-Malik scheme with simplification
    denoised_img = perona_malik_simplification(denoised_img, num_iterations, dt, K, g_function, interpolation, alpha)

    # Normalize the image if not in range [0, 1]
    if np.min(denoised_img) < 0 or np.max(denoised_img) > 1:
        min_val = np.min(denoised_img)
        max_val = np.max(denoised_img)
        denoised_img =    (denoised_img - min_val) / (max_val - min_val)

    # Write the denoised image to disk
    plt.imsave("results/perona/"+input_image_name[:-4]+
                str(num_iterations)+"_"+
                str(dt)+"_"+
                str(K)+"_"+
                args.g_function+"_"+
                str(interpolation)+"_"+
                str(alpha)+
                ".png",
                denoised_img, cmap='gray')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Perona-Malik Image Denoising")

    parser.add_argument("--input", type=str, required=True, help="Input image file path")
    parser.add_argument("--output", type=str, default="cameraman_perona.png", help="Output denoised image file path")
    parser.add_argument("--num_iterations", type=int, default=10, help="Number of iterations")
    parser.add_argument("--dt", type=float, default=0.25, help="Time step")
    parser.add_argument("--K", type=float, default=100, help="Inflection point of the g function")
    parser.add_argument("--interpolation", default=False, type=bool, help="Use linear interpolation for gradient or not")
    parser.add_argument("--g_function", choices=["lorentz", "tukey"], default="lorentz", help="Choose the g function")
    parser.add_argument("--alpha", type=float, default=1, help="Alpha value for Lorentz g function")

    args = parser.parse_args()
    print("Processing image: ", args.input,"\n")
    main(args)