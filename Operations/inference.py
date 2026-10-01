from Operations.load_model import model
import torch.nn as nn 
import numpy as np
loss = nn.MSELoss()
def run_inference(data):
    output = model(data)
    mse = loss(output, data)
    return mse.item()