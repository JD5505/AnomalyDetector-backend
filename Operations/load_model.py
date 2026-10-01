import torch
from Operations.model_structure import GRU_AutoEncoder

state_dict = torch.load("gruautoencoder/gru_autoencoder_model.pth", map_location = 'cpu')

model = GRU_AutoEncoder(4)
model.load_state_dict(state_dict)
model.eval()
