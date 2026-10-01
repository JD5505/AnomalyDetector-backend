import torch.nn as nn


class GRU_AutoEncoder(nn.Module):
  def __init__(self, input_size):
    super().__init__()
    self.encoder = nn.GRU(
        input_size = input_size,
        hidden_size = 64,
        num_layers = 1,
        batch_first = True
    )

    self.to_latent = nn.Linear(
        in_features = 64,
        out_features = 32
    )

    self.from_latent = nn.Linear(
        in_features = 32,
        out_features = 64
    )

    self.decoder = nn.GRU(
        input_size = 64,
        hidden_size = 64,
        num_layers = 1,
        batch_first = True
    )

    self.output = nn.Linear(
        in_features = 64,
        out_features = input_size
    )

  def forward(self, x):
    _, hidden = self.encoder(x)

    hidden = hidden[-1]

    latent = self.to_latent(hidden)
    decoder_hidden = self.from_latent(latent)

    decoder_input = decoder_hidden.unsqueeze(1).repeat(
            1,
            x.size(1),
            1
        )

    decoded, _ = self.decoder(decoder_input)
    output = self.output(decoded)
    return output