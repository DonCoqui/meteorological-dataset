import numpy as np

# --- (TASK A): TRAPEZOIDAL INTEGRATION ---
def integrate_loop(t, y, initial_value=0):
    n = len(t)
    res = np.zeros(n)
    res[0] = initial_value
    for i in range(1, n):
        dt = t[i] - t[i-1]
        area = 0.5 * (y[i] + y[i-1]) * dt
        res[i] = res[i-1] + area
    return res

def integrate_vector(t, y, initial_value=0):
    dt = np.diff(t)
    y_avg = (y[1:] + y[:-1]) / 2
    areas = y_avg * dt
    return np.concatenate(([initial_value], initial_value + np.cumsum(areas)))

# --- (TASK B): CENTRAL DIFFERENCES ---
def differentiate_loop(t, y):
    n = len(t)
    res = np.zeros(n)
    for i in range(n):
        if i == 0: # Forward
            res[i] = (y[i+1] - y[i]) / (t[i+1] - t[i])
        elif i == n - 1: # Backward
            res[i] = (y[i] - y[i-1]) / (t[i] - t[i-1])
        else: # Central
            res[i] = (y[i+1] - y[i-1]) / (t[i+1] - t[i-1])
    return res

def differentiate_vector(t, y):
    res = np.zeros(len(t))
    res[1:-1] = (y[2:] - y[:-2]) / (t[2:] - t[:-2])  # Central
    res[0] = (y[1] - y[0]) / (t[1] - t[0])           # Forward
    res[-1] = (y[-1] - y[-2]) / (t[-1] - t[-2])      # Backward
    return res

# --- (TASK C): MOVING AVERAGE ---
def moving_average(y, W):
    n = len(y)
    res = np.zeros(n)
    k = (W - 1) // 2
    for i in range(n):
        start = max(0, i - k)
        end = min(n, i + k + 1)
        res[i] = np.mean(y[start:end])
    return res


            
            
            
            
            