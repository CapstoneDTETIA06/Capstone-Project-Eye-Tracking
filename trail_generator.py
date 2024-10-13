import numpy as np
import random
from sklearn.preprocessing import MinMaxScaler

TIME = 60
FPS = 25 * TIME

def wave(x):
    y1 = 2 * np.sin(2 * np.pi * .01 * x + random.random()*2*np.pi)
    y2 = -2 * np.sin(2 * np.pi * 0.002 * x + random.random()*2*np.pi)
    y3 = 2.6 * np.sin(2 * np.pi * 0.03 * x + random.random()*2*np.pi)
    y4 = .75 * np.sin(2 * np.pi * 0.1 * x + random.random()*2*np.pi)
    y5 = -.6 * np.sin(2 * np.pi * 0.05 * x + random.random()*2*np.pi)
    y6 = -.75 * np.sin(2 * np.pi * .08 * x + random.random()*2*np.pi)
    y7 = .2 * np.sin(2 * np.pi * .05 * x + random.random()*2*np.pi)

    Y = (y1+y2+y3 +y4 +y5+y6+y7) * 4

    scaler = MinMaxScaler(feature_range=(-1, 1))
    Y_norm = scaler.fit_transform(Y.reshape(-1,1))

    return Y_norm*120


def generate_trail(screen_width, screen_height):
    timeseries = np.linspace(0, TIME , num=FPS)
    y = wave(timeseries)
    y_reshaped = y.reshape(1, -1)[0]

    x_coord = [(300*np.cos(np.pi*_y/180))+(screen_width/2) for _y in y_reshaped]
    y_coord = [(300*np.sin(np.pi*_y/180))+(screen_height/2) for _y in y_reshaped]

    x_coord = np.array(x_coord).tolist()
    y_coord = np.array(y_coord).tolist()
    
    return x_coord, y_coord