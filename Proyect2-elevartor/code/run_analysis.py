import numpy as np
import matplotlib.pyplot as plt
from io import StringIO

print("\n" + "="*120)
print("TASK F & G: ANALYSIS - SECTION 7 (Analysis) - WITH REAL DATA")
print("="*120)

# ============ DEFINE MATH FUNCTIONS (from Maths.py) ============
def integrate_vector(t, y, initial_value=0):
    dt = np.diff(t)
    y_avg = (y[1:] + y[:-1]) / 2
    areas = y_avg * dt
    return np.concatenate(([initial_value], initial_value + np.cumsum(areas)))

def differentiate_vector(t, y):
    res = np.zeros(len(t))
    res[1:-1] = (y[2:] - y[:-2]) / (t[2:] - t[:-2])  # Central
    res[0] = (y[1] - y[0]) / (t[1] - t[0])           # Forward
    res[-1] = (y[-1] - y[-2]) / (t[-1] - t[-2])      # Backward
    return res

def moving_average(y, W):
    n = len(y)
    res = np.zeros(n)
    k = (W - 1) // 2
    for i in range(n):
        start = max(0, i - k)
        end = min(n, i + k + 1)
        res[i] = np.mean(y[start:end])
    return res

# ============ LOAD DATA ============
print("\n[LOADING DATA]")

# Load acceleration data
data_acc = np.loadtxt('Proyect2-elevartor/code/subida_1.csv', delimiter=',', skiprows=1)
t_acc, acc_raw = data_acc[:, 0], data_acc[:, 1]

# Load pressure/barometer data
data_pre = np.genfromtxt('Proyect2-elevartor/code/Pressure and velocity.csv', delimiter=',', 
                         skip_header=1, missing_values='""', filling_values=0)

if np.isnan(data_pre[-1]).any(): 
    data_pre = data_pre[:-1]

t_pre, p_pre, h_pre, t_vel, v_pre = data_pre[:, 0], data_pre[:, 1], data_pre[:, 2], data_pre[:, 3], data_pre[:, 4]

# Relative altitude
h_relative = h_pre - h_pre[0]

# Calculate bias
quiet_mask = t_acc < 5
bias = np.mean(acc_raw[quiet_mask])
acc_calibrated = acc_raw - bias

# Apply filter
W = 15
acc_filtered = moving_average(acc_calibrated, W)

print(f"✓ Data loaded successfully")
print(f"  - Acceleration time points: {len(t_acc)}")
print(f"  - Pressure time points: {len(t_pre)}")
print(f"  - Bias calculated (first 5 sec): {bias:.6f} m/s²")
print(f"  - Moving average window size: {W}")
print(f"  - Total measurement time: {t_acc[-1]:.2f} s")
print(f"  - Elevator height (barometer): {h_relative[-1]:.6f} m")

print("\n" + "="*120)
print("QUESTION 1: THE EFFECT OF THE SOFTWARE FILTER")
print("="*120)

print("\n[ANALYSIS 1.1: Raw vs Filtered Acceleration Statistics]")

# Calculate statistics
print("\nSTATISTICAL COMPARISON:")
print(f"{'Metric':<30} {'Raw Accel':<20} {'Filtered Accel':<20} {'Difference':<20}")
print("-"*90)

raw_mean = np.mean(acc_raw)
filtered_mean = np.mean(acc_filtered)
print(f"{'Mean (m/s²)':<30} {raw_mean:<20.6f} {filtered_mean:<20.6f} {abs(raw_mean-filtered_mean):<20.6f}")

raw_std = np.std(acc_raw)
filtered_std = np.std(acc_filtered)
print(f"{'Std Dev (m/s²)':<30} {raw_std:<20.6f} {filtered_std:<20.6f} {raw_std-filtered_std:<20.6f}")

raw_min = np.min(acc_raw)
filtered_min = np.min(acc_filtered)
print(f"{'Min (m/s²)':<30} {raw_min:<20.6f} {filtered_min:<20.6f} {raw_min-filtered_min:<20.6f}")

raw_max = np.max(acc_raw)
filtered_max = np.max(acc_filtered)
print(f"{'Max (m/s²)':<30} {raw_max:<20.6f} {filtered_max:<20.6f} {raw_max-filtered_max:<20.6f}")

raw_range = raw_max - raw_min
filtered_range = filtered_max - filtered_min
print(f"{'Range (m/s²)':<30} {raw_range:<20.6f} {filtered_range:<20.6f} {raw_range-filtered_range:<20.6f}")

# Noise analysis
print("\n[ANALYSIS 1.2: Noise Reduction Quantification]")

raw_diffs = np.diff(acc_raw)
filtered_diffs = np.diff(acc_filtered)

mean_raw_diff = np.mean(np.abs(raw_diffs))
mean_filtered_diff = np.mean(np.abs(filtered_diffs))
noise_reduction = (mean_raw_diff - mean_filtered_diff) / mean_raw_diff * 100

print(f"\nMean absolute change between consecutive points:")
print(f"  Raw acceleration:      {mean_raw_diff:.6f} m/s² (Δ per point)")
print(f"  Filtered acceleration: {mean_filtered_diff:.6f} m/s² (Δ per point)")
print(f"  Noise reduction:       {noise_reduction:.2f}%")

# Kinematics
print("\n[ANALYSIS 1.3: Kinematic Effects of Filtering]")

v_raw_uncal = integrate_vector(t_acc, acc_raw, 0)
v_filtered = integrate_vector(t_acc, acc_filtered, 0)
v_difference = v_raw_uncal - v_filtered
max_v_diff = np.max(np.abs(v_difference))
final_v_diff = v_difference[-1]

print(f"\nVelocity divergence (Raw uncalibrated vs Filtered+calibrated):")
print(f"  Maximum difference: {max_v_diff:.6f} m/s")
print(f"  Final difference:   {final_v_diff:.6f} m/s")
print(f"  Average difference: {np.mean(np.abs(v_difference)):.6f} m/s")

d_raw_uncal = integrate_vector(t_acc, v_raw_uncal, 0)
d_filtered = integrate_vector(t_acc, v_filtered, 0)
d_difference = d_raw_uncal - d_filtered
max_d_diff = np.max(np.abs(d_difference))
final_d_diff = d_difference[-1]

print(f"\nDisplacement divergence (Raw uncalibrated vs Filtered+calibrated):")
print(f"  Maximum difference: {max_d_diff:.6f} m")
print(f"  Final difference:   {final_d_diff:.6f} m")
error_pct_q1 = (abs(final_d_diff) / h_relative[-1] * 100) if h_relative[-1] != 0 else 0
print(f"  Error percentage:   {error_pct_q1:.2f}% of elevator height")

print("\n" + "="*120)
print("QUESTION 2: ISOLATING THE VARIABLES")
print("="*120)

print("\n[SCENARIO A: FILTERED but NO BIAS SUBTRACTION]")

acc_filtered_no_cal = moving_average(acc_raw, W)
v_scenario_a = integrate_vector(t_acc, acc_filtered_no_cal, 0)
d_scenario_a = integrate_vector(t_acc, v_scenario_a, 0)

print(f"  Final velocity:    {v_scenario_a[-1]:.6f} m/s")
print(f"  Final displacement: {d_scenario_a[-1]:.6f} m")
print(f"  vs Barometer truth: {h_relative[-1]:.6f} m")
error_a = abs(d_scenario_a[-1] - h_relative[-1])
print(f"  Error:             {error_a:.6f} m")

print("\n[SCENARIO B: BIAS SUBTRACTED but NO FILTERING]")

v_scenario_b = integrate_vector(t_acc, acc_calibrated, 0)
d_scenario_b = integrate_vector(t_acc, v_scenario_b, 0)

print(f"  Final velocity:    {v_scenario_b[-1]:.6f} m/s")
print(f"  Final displacement: {d_scenario_b[-1]:.6f} m")
print(f"  vs Barometer truth: {h_relative[-1]:.6f} m")
error_b = abs(d_scenario_b[-1] - h_relative[-1])
print(f"  Error:             {error_b:.6f} m")

print("\n[SCENARIO C: BOTH FILTERED AND BIAS SUBTRACTED (OPTIMAL)]")

v_scenario_c = integrate_vector(t_acc, acc_filtered, 0)
d_scenario_c = integrate_vector(t_acc, v_scenario_c, 0)

print(f"  Final velocity:    {v_scenario_c[-1]:.6f} m/s")
print(f"  Final displacement: {d_scenario_c[-1]:.6f} m")
print(f"  vs Barometer truth: {h_relative[-1]:.6f} m")
error_c = abs(d_scenario_c[-1] - h_relative[-1])
print(f"  Error:             {error_c:.6f} m")

print("\n[COMPARISON TABLE]")
print(f"{'Scenario':<40} {'Final Disp (m)':<18} {'Error (m)':<18} {'Error (%)':<15}")
print("-"*90)

baseline = h_relative[-1]
pct_a = (error_a / baseline * 100) if baseline != 0 else 0
pct_b = (error_b / baseline * 100) if baseline != 0 else 0
pct_c = (error_c / baseline * 100) if baseline != 0 else 0

print(f"{'A: Filtered, NO bias subtraction':<40} {d_scenario_a[-1]:<18.6f} {error_a:<18.6f} {pct_a:<15.2f}%")
print(f"{'B: Bias subtracted, NO filtering':<40} {d_scenario_b[-1]:<18.6f} {error_b:<18.6f} {pct_b:<15.2f}%")
print(f"{'C: Filtered AND bias subtracted':<40} {d_scenario_c[-1]:<18.6f} {error_c:<18.6f} {pct_c:<15.2f}%")
print(f"{'Barometer Ground Truth':<40} {baseline:<18.6f} {'—':<18} {'—':<15}")

print("\n[DETERMINING WHICH OPERATION HAS LARGER EFFECT]")

effect_bias = abs(d_scenario_b[-1] - d_scenario_c[-1])
effect_filtering = abs(d_scenario_a[-1] - d_scenario_c[-1])

print(f"\nEffect of BIAS SUBTRACTION (B → C):")
print(f"  Scenario B (bias not removed): d = {d_scenario_b[-1]:.6f} m")
print(f"  Scenario C (bias removed):     d = {d_scenario_c[-1]:.6f} m")
print(f"  Difference:                    Δd = {effect_bias:.6f} m")
pct_change_bias = (effect_bias/abs(d_scenario_b[-1])*100) if d_scenario_b[-1]!=0 else 0
print(f"  Percentage change:             {pct_change_bias:.2f}%")

print(f"\nEffect of FILTERING (A → C):")
print(f"  Scenario A (no filter):        d = {d_scenario_a[-1]:.6f} m")
print(f"  Scenario C (filtered):         d = {d_scenario_c[-1]:.6f} m")
print(f"  Difference:                    Δd = {effect_filtering:.6f} m")
pct_change_filter = (effect_filtering/abs(d_scenario_a[-1])*100) if d_scenario_a[-1]!=0 else 0
print(f"  Percentage change:             {pct_change_filter:.2f}%")

print(f"\n[CONCLUSION]")
if effect_bias > effect_filtering:
    dominant_op = "BIAS SUBTRACTION"
    larger_effect = effect_bias
    smaller_effect = effect_filtering
    print(f"✓ {dominant_op} has the LARGER effect ({effect_bias:.6f} m > {effect_filtering:.6f} m)")
else:
    dominant_op = "FILTERING"
    larger_effect = effect_filtering
    smaller_effect = effect_bias
    print(f"✓ {dominant_op} has the LARGER effect ({effect_filtering:.6f} m > {effect_bias:.6f} m)")

print(f"\n[MATHEMATICAL ANALYSIS]")
velocity_bias = bias * t_acc[-1]
displacement_bias = 0.5 * bias * (t_acc[-1]**2)

print(f"\nBias accumulation over {t_acc[-1]:.2f} seconds:")
print(f"  Constant bias: {bias:.6f} m/s²")
print(f"  Final velocity bias: {velocity_bias:.6f} m/s")
print(f"  Final displacement bias: {displacement_bias:.6f} m")

# ============ VISUALIZATION ============
print("\n" + "="*120)
print("GENERATING VISUALIZATION FIGURES")
print("="*120)

# Figure 1: Effect of Filter
fig1, axs = plt.subplots(3, 2, figsize=(14, 12))
fig1.suptitle('Analysis Question 1: Effect of Software Filter', fontsize=16, fontweight='bold')

# Row 1: Acceleration comparison
axs[0,0].plot(t_acc, acc_raw, alpha=0.6, linewidth=1, label='Raw Acceleration', color='red')
axs[0,0].plot(t_acc, acc_filtered, linewidth=2, label='Filtered Acceleration', color='blue')
axs[0,0].axhline(y=0, color='k', linestyle='--', alpha=0.3)
axs[0,0].set_ylabel('Acceleration (m/s²)', fontsize=11)
axs[0,0].set_title('Raw vs Filtered Acceleration', fontsize=12, fontweight='bold')
axs[0,0].legend(fontsize=10)
axs[0,0].grid(True, alpha=0.3)

# Row 1: Acceleration differences
axs[0,1].plot(t_acc, np.abs(raw_diffs), alpha=0.6, linewidth=1, label='Raw Changes', color='red')
axs[0,1].plot(t_acc[:-1], np.abs(filtered_diffs), linewidth=2, label='Filtered Changes', color='blue')
axs[0,1].set_ylabel('|Δ Acceleration| (m/s²)', fontsize=11)
axs[0,1].set_title(f'High-Frequency Content (Noise Reduction: {noise_reduction:.1f}%)', fontsize=12, fontweight='bold')
axs[0,1].legend(fontsize=10)
axs[0,1].grid(True, alpha=0.3)

# Row 2: Velocity comparison
axs[1,0].plot(t_pre, v_pre, '--', linewidth=2, label='Provided Velocity (Phyphox)', color='gray')
axs[1,0].plot(t_acc, v_raw_uncal, alpha=0.7, linewidth=1.5, label='Raw Uncalibrated', color='red')
axs[1,0].plot(t_acc, v_filtered, linewidth=2, label='Filtered + Calibrated', color='blue')
axs[1,0].set_ylabel('Velocity (m/s)', fontsize=11)
axs[1,0].set_title('Velocity: Integrated Acceleration', fontsize=12, fontweight='bold')
axs[1,0].legend(fontsize=10)
axs[1,0].grid(True, alpha=0.3)

# Row 2: Velocity error
axs[1,1].plot(t_acc, v_difference, linewidth=2, color='purple')
axs[1,1].fill_between(t_acc, v_difference, alpha=0.3, color='purple')
axs[1,1].axhline(y=0, color='k', linestyle='--', alpha=0.3)
axs[1,1].set_ylabel('Velocity Difference (m/s)', fontsize=11)
axs[1,1].set_title('Velocity Error (Raw Uncal. - Filtered Cal.)', fontsize=12, fontweight='bold')
axs[1,1].grid(True, alpha=0.3)

# Row 3: Displacement comparison
axs[2,0].plot(t_pre, h_relative, linewidth=2.5, label='Barometer (Truth)', color='green', marker='o', markersize=3)
axs[2,0].plot(t_acc, d_raw_uncal, alpha=0.7, linewidth=1.5, label='Raw Uncalibrated', color='red')
axs[2,0].plot(t_acc, d_filtered, linewidth=2, label='Filtered + Calibrated', color='blue')
axs[2,0].set_xlabel('Time (s)', fontsize=11)
axs[2,0].set_ylabel('Displacement (m)', fontsize=11)
axs[2,0].set_title('Displacement: Double Integrated Acceleration', fontsize=12, fontweight='bold')
axs[2,0].legend(fontsize=10)
axs[2,0].grid(True, alpha=0.3)

# Row 3: Displacement error
axs[2,1].plot(t_acc, d_difference, linewidth=2, color='purple')
axs[2,1].fill_between(t_acc, d_difference, alpha=0.3, color='purple')
axs[2,1].axhline(y=0, color='k', linestyle='--', alpha=0.3)
axs[2,1].set_xlabel('Time (s)', fontsize=11)
axs[2,1].set_ylabel('Displacement Error (m)', fontsize=11)
axs[2,1].set_title(f'Displacement Error\nFinal Error: {final_d_diff:.4f} m ({error_pct_q1:.2f}%)', 
                   fontsize=12, fontweight='bold')
axs[2,1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('Proyect2-elevartor/code/analysis_question_1_filter_effect.png', dpi=300, bbox_inches='tight')
print("✓ Saved: analysis_question_1_filter_effect.png")
plt.close()

# Figure 2: Isolating variables
fig2, axs = plt.subplots(2, 2, figsize=(14, 10))
fig2.suptitle('Analysis Question 2: Isolating Variables (Filtering vs Bias Subtraction)', 
              fontsize=16, fontweight='bold')

# Displacement comparison
axs[0,0].plot(t_pre, h_relative, 'o-', linewidth=2.5, markersize=4, label='Barometer (Truth)', 
              color='green', zorder=5)
axs[0,0].plot(t_acc, d_scenario_a, linewidth=2, label='Scenario A: Filtered, NO bias', 
              color='orange', alpha=0.8)
axs[0,0].plot(t_acc, d_scenario_b, linewidth=2, label='Scenario B: Bias removed, NO filter', 
              color='red', alpha=0.8)
axs[0,0].plot(t_acc, d_scenario_c, linewidth=2, label='Scenario C: Both (Optimal)', 
              color='blue', alpha=0.8)
axs[0,0].set_ylabel('Displacement (m)', fontsize=11)
axs[0,0].set_title('Displacement Comparison', fontsize=12, fontweight='bold')
axs[0,0].legend(fontsize=10)
axs[0,0].grid(True, alpha=0.3)

# Error magnitude
errors = [error_a, error_b, error_c]
labels = ['A: Filtered\nNO bias', 'B: Bias removed\nNO filter', 'C: Both\n(Optimal)']
colors_bar = ['orange', 'red', 'blue']

bars = axs[0,1].bar(labels, errors, color=colors_bar, alpha=0.7, edgecolor='black', linewidth=2)
axs[0,1].set_ylabel('Absolute Error (m)', fontsize=11)
axs[0,1].set_title('Final Displacement Error Magnitude', fontsize=12, fontweight='bold')
axs[0,1].grid(True, alpha=0.3, axis='y')
for i, (label, error) in enumerate(zip(labels, errors)):
    axs[0,1].text(i, error + 0.05, f'{error:.4f}m', ha='center', fontweight='bold', fontsize=10)

# Velocity comparison
axs[1,0].plot(t_pre, v_pre, 'o--', linewidth=2, markersize=4, label='Provided Velocity', 
              color='gray', zorder=5)
axs[1,0].plot(t_acc, v_scenario_a, linewidth=2, label='Scenario A: Filtered, NO bias', 
              color='orange', alpha=0.8)
axs[1,0].plot(t_acc, v_scenario_b, linewidth=2, label='Scenario B: Bias removed, NO filter', 
              color='red', alpha=0.8)
axs[1,0].plot(t_acc, v_scenario_c, linewidth=2, label='Scenario C: Both (Optimal)', 
              color='blue', alpha=0.8)
axs[1,0].set_ylabel('Velocity (m/s)', fontsize=11)
axs[1,0].set_title('Velocity Comparison', fontsize=12, fontweight='bold')
axs[1,0].legend(fontsize=10)
axs[1,0].grid(True, alpha=0.3)

# Effect size comparison
effect_sizes = [effect_bias, effect_filtering]
effect_labels = [f'Bias Subtraction\nEffect: {effect_bias:.6f} m', 
                 f'Filtering\nEffect: {effect_filtering:.6f} m']
effect_colors = ['red', 'blue']

bars = axs[1,1].bar(effect_labels, effect_sizes, color=effect_colors, alpha=0.7, edgecolor='black', linewidth=2)
axs[1,1].set_ylabel('Displacement Change (m)', fontsize=11)
axs[1,1].set_title('Relative Effect: Which Operation Matters More?', fontsize=12, fontweight='bold')
axs[1,1].grid(True, alpha=0.3, axis='y')

for bar, effect in zip(bars, effect_sizes):
    height = bar.get_height()
    axs[1,1].text(bar.get_x() + bar.get_width()/2., height,
                 f'{effect:.6f}m',
                 ha='center', va='bottom', fontweight='bold', fontsize=10)

# Add winner annotation
max_effect = max(effect_sizes)
if effect_bias > effect_filtering:
    axs[1,1].text(0.5, max_effect*0.85, 'BIAS SUBTRACTION\nHas Larger Effect',
                 ha='center', fontsize=11, fontweight='bold', 
                 bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.8))
else:
    axs[1,1].text(0.5, max_effect*0.85, 'FILTERING\nHas Larger Effect',
                 ha='center', fontsize=11, fontweight='bold',
                 bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.8))

plt.tight_layout()
plt.savefig('Proyect2-elevartor/code/analysis_question_2_isolating_variables.png', dpi=300, bbox_inches='tight')
print("✓ Saved: analysis_question_2_isolating_variables.png")
plt.close()

print("\n" + "="*120)
print("SUMMARY OF ALL NUMBERS FOR YOUR REPORT")
print("="*120)

print("\n[QUESTION 1 - NUMBERS TO INSERT IN REPORT]")
print(f"\nFilter Effect Summary:")
print(f"  [X] = Noise reduction percentage = {noise_reduction:.2f}%")
print(f"  [Y] = Mean raw acceleration change = {mean_raw_diff:.6f} m/s²")
print(f"  [Z] = Mean filtered acceleration change = {mean_filtered_diff:.6f} m/s²")
print(f"  [A] = Max velocity difference = {max_v_diff:.6f} m/s")
print(f"  [B] = Final velocity difference = {final_v_diff:.6f} m/s")
print(f"  [C] = Average velocity difference = {np.mean(np.abs(v_difference)):.6f} m/s")
print(f"  [D] = Max displacement difference = {max_d_diff:.6f} m")
print(f"  [E] = Final displacement difference = {final_d_diff:.6f} m")
print(f"  [F] = Error percentage of height = {error_pct_q1:.2f}%")

print("\n[QUESTION 2 - NUMBERS TO INSERT IN REPORT]")
print(f"\nVariable Isolation Summary:")
print(f"  [value_A] = Scenario A final displacement = {d_scenario_a[-1]:.6f} m")
print(f"  [error_A] = Scenario A error = {error_a:.6f} m")
print(f"  [pct_A] = Scenario A error percentage = {pct_a:.2f}%")
print(f"  [value_B] = Scenario B final displacement = {d_scenario_b[-1]:.6f} m")
print(f"  [error_B] = Scenario B error = {error_b:.6f} m")
print(f"  [pct_B] = Scenario B error percentage = {pct_b:.2f}%")
print(f"  [value_C] = Scenario C final displacement = {d_scenario_c[-1]:.6f} m")
print(f"  [error_C] = Scenario C error = {error_c:.6f} m")
print(f"  [pct_C] = Scenario C error percentage = {pct_c:.2f}%")
print(f"  [baseline] = Barometer ground truth = {baseline:.6f} m")
print(f"  [effect_bias] = Bias subtraction effect = {effect_bias:.6f} m")
print(f"  [pct_change_bias] = Bias effect percentage = {pct_change_bias:.2f}%")
print(f"  [effect_filtering] = Filtering effect = {effect_filtering:.6f} m")
print(f"  [pct_change_filter] = Filtering effect percentage = {pct_change_filter:.2f}%")
print(f"  [OPERATION_WITH_LARGER_EFFECT] = {dominant_op}")
print(f"  [larger_value] = {larger_effect:.6f} m")
print(f"  [smaller_value] = {smaller_effect:.6f} m")
print(f"  [bias_value] = {bias:.6f} m/s²")
print(f"  [t_final] = {t_acc[-1]:.2f} s")
print(f"  [velocity_bias] = {velocity_bias:.6f} m/s")
print(f"  [displacement_bias] = {displacement_bias:.6f} m")

print("\n" + "="*120)
print("✅ ANALYSIS COMPLETE - ALL FILES SAVED")
print("="*120)
print("\nFigures saved:")
print("  1. analysis_question_1_filter_effect.png")
print("  2. analysis_question_2_isolating_variables.png")
