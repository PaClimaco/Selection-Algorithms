#Author: Paolo Climaco
#Contact: climaco@ins.uni-bonn.de

import torch
from tqdm import tqdm
import numpy as np


def FPS(points_i, initialization, b):
    """
    Selects a set of points using Farthest Point Sampling (FPS) algorithm.

    Inputs:
    - points_i (numpy.ndarray or torch.Tensor): Input points, representing a set of data points.
      If not already a torch.Tensor, it will be converted using torch.from_numpy().
    - initialization (list): List of indices representing the initial set of centers.
    - b (int): The desired number of points to select.

    Returns:
    - centers (list): List of indices representing the selected points using the FPS algorithm.
    """
    
    # Check if the number of points to select is larger than the number of available points
    if b > len(points_i):
        print('Error: number of points to select larger than the number of available points')
        return
   
    # Convert points to torch.Tensor if not already
    if not torch.is_tensor(points_i):
        points_t = torch.from_numpy(points_i)
    else:
        points_t = points_i
        
    # Check if a GPU is available, and if not, use the CPU
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")  
    points = points_t.to(device)

    # Initialize the first centers
    centers = initialization

    # Compute distances from all points to the initial centers
    distances = torch.min(torch.cdist(points, points[centers], p=2), dim=1)[0]

    # Iterate to select additional points until reaching the desired number
    for n in tqdm(range(b - len(initialization))):
        # Find the point farthest from all current centers
        farthest_point = torch.argmax(distances)

        # Add it as a new center
        centers.append(farthest_point.item())

        # Recalculate distances from all points to the new center
        new_distances = torch.min(torch.norm(points - points[farthest_point], dim=1), distances)
        distances = new_distances

    # Return the final set of selected centers
    return centers
