import numpy as np
import Maths as ms
import matplotlib.pyplot as plt

# 1. Carga de Datos y Limpieza
# Asegúrate de que estos nombres coincidan exactamente con tus archivos
data_acc = np.loadtxt('subida_1_5.csv', delimiter=',', skiprows=1)
data_pre = np.genfromtxt('Pressure and velocity_4.csv', delimiter=',', skip_header=1, missing_values='""', filling_values=0)

# Eliminar última fila si contiene NaNs (común en exportaciones de Phyphox)
if np.isnan(data_pre[-1]).any(): data_pre = data_pre[:-1]

# 2. Asignación de Variables
t_acc, acc_raw = data_acc[:, 0], data_acc[:, 1]
t_pre, p_pre, h_pre, v_pre = data_pre[:, 0], data_pre[:, 1], data_pre[:, 2], data_pre[:, 3]

# Sincronización de altitud relativa (empezar en cero)
h_relative = h_pre - h_pre[0]

# --- BLOQUE 1: CÁLCULOS SIN CALIBRAR ---
v_integ_uncal = ms.integrate_vector(t_acc, acc_raw, 0)
d_integ_uncal = ms.integrate_vector(t_acc, v_integ_uncal, 0)
v_diff_pre = ms.differentiate_vector(t_pre, h_pre)

# --- BLOQUE 2: CALIBRACIÓN Y FILTRADO ---
# Calculamos el bias usando los primeros 5 segundos de calma[cite: 14]
quiet_mask = t_acc < 5
bias = np.mean(acc_raw[quiet_mask])
acc_cal = acc_raw - bias

# Filtro de Media Móvil (W=15 para igualar al profesor)[cite: 14]
acc_filtered = ms.moving_average(acc_cal, 15)

# Cinemática Calibrada
v_final = ms.integrate_vector(t_acc, acc_filtered, 0)
d_final = ms.integrate_vector(t_acc, v_final, 0)

# --- FIGURA 1: DASHBOARD 1 (ESTADO NO CALIBRADO) ---
fig1, axs1 = plt.subplots(4, 1, figsize=(10, 12), sharex=True)
axs1[0].plot(t_acc, acc_raw, label='Recorded Accel (IMU)')
axs1[1].plot(t_pre, p_pre, color='brown', label='Recorded Pressure (Barometer)')
axs1[2].plot(t_pre, v_pre, '--', label='Provided Velocity (Phyphox)')
axs1[2].plot(t_acc, v_integ_uncal, label='Integrated Accel (Drifting)')
axs1[2].plot(t_pre, v_diff_pre, label='Differentiated Altitude')
axs1[3].plot(t_pre, h_relative, color='red', label='Provided Altitude (Truth)')
axs1[3].plot(t_acc, d_integ_uncal, color='purple', label='Double Integrated Accel (Error)')

for ax in axs1: 
    ax.grid(True)
    ax.legend(loc='upper right', fontsize='x-small')
axs1[0].set_ylabel('Acc [m/s²]'); axs1[1].set_ylabel('Pressure [hPa]')
axs1[2].set_ylabel('Vel [m/s]'); axs1[3].set_ylabel('Disp [m]')
fig1.suptitle('Dashboard 1: Sensor Telemetry (Uncalibrated State)')

# --- FIGURA 2: DASHBOARD 2 (ESTADO CALIBRADO Y FILTRADO) ---
fig2, axs2 = plt.subplots(3, 1, figsize=(10, 10), sharex=True)
axs2[0].plot(t_acc, acc_raw, alpha=0.3, label='Raw Accel', color='lightblue')
axs2[0].plot(t_acc, acc_filtered, label='Filtered & Zeroed Accel (W=15)', color='brown')
axs2[1].plot(t_pre, v_pre, '--', label='Provided Velocity', color='gray')
axs2[1].plot(t_acc, v_final, label='Integrated Filtered Accel', color='orange')
axs2[1].plot(t_pre, v_diff_pre, label='Differentiated Altitude', color='green')
axs2[2].plot(t_pre, h_relative, color='red', label='Provided Altitude (Truth)')
axs2[2].plot(t_acc, d_final, color='purple', label='Double Integrated Filtered Accel')

for ax in axs2: 
    ax.grid(True)
    ax.legend(loc='upper right', fontsize='x-small')
axs2[0].set_ylabel('Acc [m/s²]'); axs2[1].set_ylabel('Vel [m/s]'); axs2[2].set_ylabel('Disp [m]')
axs2[2].set_xlabel('Time [s]')
fig2.suptitle('Dashboard 2: Sensor Telemetry (Calibrated & Filtered)')

plt.tight_layout()
plt.show()
