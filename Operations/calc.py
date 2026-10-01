from Operations.load_scaler import scaler
import numpy as np
import torch

def preprocess(coords: np.ndarray, times: np.ndarray) -> torch.Tensor:
    """
    coords: shape (N, 2) dtype=np.float64
    times:  shape (N,)   dtype=np.float64 (Unix epoch seconds)
    """
    N = coords.shape[0]
    
    if N < 2:
        return torch.zeros((1, max(N - 1, 0), 4), dtype=torch.float32)

    speed = np.zeros(N)
    acc = np.zeros(N)
    bearing = np.zeros(N)
    change_in_dir = np.zeros(N)
    is_stationary = np.zeros(N)

    lat1 = np.radians(coords[:-1, 0])
    lat2 = np.radians(coords[1:, 0])
    lon1 = np.radians(coords[:-1, 1])
    lon2 = np.radians(coords[1:, 1])

    # Time Delta in seconds
    dt = times[1:] - times[:-1]
    dt_safe = np.where(dt == 0, 1e-9, dt)  # Prevent division by zero

    # Distance (Vectorized Haversine)
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = np.sin(dlat / 2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2)**2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
    dist = 6371000 * c  # Earth radius in meters

    speed[1:] = dist / dt_safe
    dv = speed[1:] - speed[:-1]
    acc[1:] = dv / dt_safe
    
    x = np.sin(dlon) * np.cos(lat2)
    y = np.cos(lat1) * np.sin(lat2) - (np.sin(lat1) * np.cos(lat2) * np.cos(dlon))
    theta = np.degrees(np.arctan2(x, y))
    bearing[1:] = (theta + 360) % 360

    db = np.abs(bearing[1:] - bearing[:-1])
    change_in_dir[1:] = np.minimum(db, 360 - db)
    
    current_stationary_time = 0.0
    for i in range(1, N):
        if speed[i] <= 0.3:
            current_stationary_time += dt[i - 1]
            if current_stationary_time >= 60:
                is_stationary[i] = 1
        else:
            current_stationary_time = 0.0

    features = np.column_stack((speed, acc, change_in_dir, is_stationary))
    
    scaled = scaler.transform(features[1:])
    # Return batch tensor [1, 30, 4]
    return torch.tensor(scaled, dtype=torch.float32).unsqueeze(0)