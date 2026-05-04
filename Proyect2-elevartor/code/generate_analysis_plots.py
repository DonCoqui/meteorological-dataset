#!/usr/bin/env python3
"""
SECTION 7 ANALYSIS - FIGURE GENERATION
Generates PNG figures for Question 1 and Question 2 analysis
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend for saving

print("\n" + "="*120)
print("GENERATING ANALYSIS FIGURES")
print("="*120)

# ============ DEFINE MATH FUNCTIONS ============
def integrate_vector(t, y, initial_value=0):
    dt = np.diff(t)
    y_avg = (y[1:] + y[:-1]) / 2
    areas = y_avg * dt
    return np.concatenate(([initial_value], initial_value + np.cumsum(areas)))

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

data_acc = np.loadtxt('subida_1.csv', delimiter=',', skiprows=1)
t_acc, acc_raw = data_acc[:, 0], data_acc[:, 1]

data_pre = np.genfromtxt('Pressure and velocity.csv', delimiter=',', 
                         skip_header=1, missing_values='""', filling_values=0)

if np.isnan(data_pre[-1]).any(): 
    data_pre = data_pre[:-1]

t_pre, p_pre, h_pre, t_vel, v_pre = data_pre[:, 0], data_pre[:, 1], data_pre[:, 2], data_pre[:, 3], data_pre[:, 4]

h_relative = h_pre - h_pre[0]

# Calculate bias
quiet_mask = t_acc < 5
bias = np.mean(acc_raw[quiet_mask])
acc_calibrated = acc_raw - bias

# Apply filter
W = 15
acc_filtered = moving_average(acc_calibrated, W)

print(f"✓ Data loaded successfully")
print(f"  - Acceleration points: {len(t_acc)}")
print(f"  - Pressure points: {len(t_pre)}")
print(f"  - Bias: {bias:.6f} m/s²")
print(f"  - Time span: {t_acc[-1]:.2f} s")

# ============ CALCULATIONS ============
print("\n[PERFORMING CALCULATIONS]")

# Scenario A: Filtered, NO bias
acc_filtered_no_cal = moving_average(acc_raw, W)
v_scenario_a = integrate_vector(t_acc, acc_filtered_no_cal, 0)
d_scenario_a = integrate_vector(t_acc, v_scenario_a, 0)

# Scenario B: Bias removed, NO filter
v_scenario_b = integrate_vector(t_acc, acc_calibrated, 0)
d_scenario_b = integrate_vector(t_acc, v_scenario_b, 0)

# Scenario C: Both
v_scenario_c = integrate_vector(t_acc, acc_filtered, 0)
d_scenario_c = integrate_vector(t_acc, v_scenario_c, 0)

# Raw uncalibrated
v_raw_uncal = integrate_vector(t_acc, acc_raw, 0)
d_raw_uncal = integrate_vector(t_acc, v_raw_uncal, 0)

# Differences
v_difference = v_raw_uncal - v_scenario_c
d_difference = d_raw_uncal - d_scenario_c

# Statistics
raw_diffs = np.diff(acc_raw)
filtered_diffs = np.diff(acc_filtered)
mean_raw_diff = np.mean(np.abs(raw_diffs))
mean_filtered_diff = np.mean(np.abs(filtered_diffs))
noise_reduction = (mean_raw_diff - mean_filtered_diff) / mean_raw_diff * 100

print(f"✓ Calculations complete")
print(f"  - Noise reduction: {noise_reduction:.2f}%")

# ============ FIGURE 1: FILTER EFFECT ============
print("\n[GENERATING FIGURE 1: Filter Effect]")

fig1, axs = plt.subplots(3, 2, figsize=(14, 12))
fig1.suptitle('Question 1: The Effect of the Software Filter', fontsize=16, fontweight='bold')

# Row 1: Acceleration
axs[0,0].plot(t_acc, acc_raw, alpha=0.6, linewidth=1, label='Raw Acceleration', color='red')
axs[0,0].plot(t_acc, acc_filtered, linewidth=2, label='Filtered Acceleration', color='blue')
axs[0,0].axhline(y=0, color='k', linestyle='--', alpha=0.3)
axs[0,0].set_ylabel('Acceleration (m/s²)', fontsize=11)
axs[0,0].set_title('Raw vs Filtered Acceleration', fontsize=12, fontweight='bold')
axs[0,0].legend(fontsize=10)
axs[0,0].grid(True, alpha=0.3)

# Row 1: Acceleration changes
axs[0,1].plot(t_acc, np.abs(raw_diffs), alpha=0.6, linewidth=1, label='Raw Changes', color='red')
axs[0,1].plot(t_acc[:-1], np.abs(filtered_diffs), linewidth=2, label='Filtered Changes', color='blue')
axs[0,1].set_ylabel('|Δ Acceleration| (m/s²)', fontsize=11)
axs[0,1].set_title(f'High-Frequency Content (Noise: {noise_reduction:.1f}%)', fontsize=12, fontweight='bold')
axs[0,1].legend(fontsize=10)
axs[0,1].grid(True, alpha=0.3)

# Row 2: Velocity
axs[1,0].plot(t_pre, v_pre, '--', linewidth=2, label='Provided Velocity', color='gray')
axs[1,0].plot(t_acc, v_raw_uncal, alpha=0.7, linewidth=1.5, label='Raw Uncalibrated', color='red')
axs[1,0].plot(t_acc, v_scenario_c, linewidth=2, label='Filtered + Calibrated', color='blue')
axs[1,0].set_ylabel('Velocity (m/s)', fontsize=11)
axs[1,0].set_title('Velocity: Integrated Acceleration', fontsize=12, fontweight='bold')
axs[1,0].legend(fontsize=10)
axs[1,0].grid(True, alpha=0.3)

# Row 2: Velocity error
axs[1,1].plot(t_acc, v_difference, linewidth=2, color='purple')
axs[1,1].fill_between(t_acc, v_difference, alpha=0.3, color='purple')
axs[1,1].axhline(y=0, color='k', linestyle='--', alpha=0.3)
axs[1,1].set_ylabel('Velocity Difference (m/s)', fontsize=11)
axs[1,1].set_title('Velocity Error (Raw - Processed)', fontsize=12, fontweight='bold')
axs[1,1].grid(True, alpha=0.3)

# Row 3: Displacement
axs[2,0].plot(t_pre, h_relative, linewidth=2.5, label='Barometer (Truth)', color='green', marker='o', markersize=3)
axs[2,0].plot(t_acc, d_raw_uncal, alpha=0.7, linewidth=1.5, label='Raw Uncalibrated', color='red')
axs[2,0].plot(t_acc, d_scenario_c, linewidth=2, label='Filtered + Calibrated', color='blue')
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
error_pct = (abs(d_difference[-1]) / h_relative[-1] * 100) if h_relative[-1] != 0 else 0
axs[2,1].set_title(f'Displacement Error (Final: {d_difference[-1]:.4f}m, {error_pct:.2f}%)', 
                   fontsize=12, fontweight='bold')
axs[2,1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('analysis_question_1_filter_effect.png', dpi=300, bbox_inches='tight')
print(f"✓ Saved: analysis_question_1_filter_effect.png")
plt.close()

# ============ FIGURE 2: ISOLATING VARIABLES ============
print("\n[GENERATING FIGURE 2: Isolating Variables]")

fig2, axs = plt.subplots(2, 2, figsize=(14, 10))
fig2.suptitle('Question 2: Isolating Variables (Filtering vs Bias Subtraction)', 
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
error_a = abs(d_scenario_a[-1] - h_relative[-1])
error_b = abs(d_scenario_b[-1] - h_relative[-1])
error_c = abs(d_scenario_c[-1] - h_relative[-1])
errors = [error_a, error_b, error_c]
labels = ['A: Filtered\nNO bias', 'B: Bias removed\nNO filter', 'C: Both\n(Optimal)']
colors_bar = ['orange', 'red', 'blue']

bars = axs[0,1].bar(labels, errors, color=colors_bar, alpha=0.7, edgecolor='black', linewidth=2)
axs[0,1].set_ylabel('Absolute Error (m)', fontsize=11)
axs[0,1].set_title('Final Displacement Error', fontsize=12, fontweight='bold')
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
effect_bias = abs(d_scenario_b[-1] - d_scenario_c[-1])
effect_filtering = abs(d_scenario_a[-1] - d_scenario_c[-1])
effect_sizes = [effect_bias, effect_filtering]
effect_labels = [f'Bias\nSubtraction\n{effect_bias:.6f}m', 
                 f'Filtering\n{effect_filtering:.6f}m']
effect_colors = ['red', 'blue']

bars = axs[1,1].bar(effect_labels, effect_sizes, color=effect_colors, alpha=0.7, edgecolor='black', linewidth=2)
axs[1,1].set_ylabel('Displacement Change (m)', fontsize=11)
axs[1,1].set_title('Which Operation Matters More?', fontsize=12, fontweight='bold')
axs[1,1].grid(True, alpha=0.3, axis='y')

for bar, effect in zip(bars, effect_sizes):
    height = bar.get_height()
    axs[1,1].text(bar.get_x() + bar.get_width()/2., height,
                 f'{effect:.6f}m',
                 ha='center', va='bottom', fontweight='bold', fontsize=10)

# Add winner annotation
max_effect = max(effect_sizes)
if effect_bias > effect_filtering:
    winner_text = 'BIAS SUBTRACTION\nHas Larger Effect'
    color = 'yellow'
else:
    winner_text = 'FILTERING\nHas Larger Effect'
    color = 'yellow'

axs[1,1].text(0.5, max_effect*0.7, winner_text,
             ha='center', fontsize=11, fontweight='bold',
             bbox=dict(boxstyle='round', facecolor=color, alpha=0.8))

plt.tight_layout()
plt.savefig('analysis_question_2_isolating_variables.png', dpi=300, bbox_inches='tight')
print(f"✓ Saved: analysis_question_2_isolating_variables.png")
plt.close()

# ============ PRINT SUMMARY ============
print("\n" + "="*120)
print("NUMERICAL RESULTS SUMMARY")
print("="*120)

print(f"\n[QUESTION 1 - FILTER EFFECT]")
print(f"Noise reduction: {noise_reduction:.2f}%")
print(f"Max velocity difference: {np.max(np.abs(v_difference)):.6f} m/s")
print(f"Final velocity difference: {v_difference[-1]:.6f} m/s")
print(f"Max displacement difference: {np.max(np.abs(d_difference)):.6f} m")
print(f"Final displacement difference: {d_difference[-1]:.6f} m")
print(f"Error percentage: {error_pct:.2f}%")

print(f"\n[QUESTION 2 - ISOLATING VARIABLES]")
print(f"Scenario A (Filtered, NO bias):")
print(f"  Final displacement: {d_scenario_a[-1]:.6f} m")
print(f"  Error: {error_a:.6f} m ({error_a/h_relative[-1]*100:.2f}%)")
print(f"Scenario B (Bias removed, NO filter):")
print(f"  Final displacement: {d_scenario_b[-1]:.6f} m")
print(f"  Error: {error_b:.6f} m ({error_b/h_relative[-1]*100:.2f}%)")
print(f"Scenario C (Both optimal):")
print(f"  Final displacement: {d_scenario_c[-1]:.6f} m")
print(f"  Error: {error_c:.6f} m ({error_c/h_relative[-1]*100:.2f}%)")
print(f"Barometer ground truth: {h_relative[-1]:.6f} m")
print(f"\nBias subtraction effect: {effect_bias:.6f} m")
print(f"Filtering effect: {effect_filtering:.6f} m")
if effect_bias > effect_filtering:
    print(f"→ BIAS SUBTRACTION has larger effect")
else:
    print(f"→ FILTERING has larger effect")

print(f"\nBias value: {bias:.6f} m/s²")
print(f"Time span: {t_acc[-1]:.2f} s")
print(f"Predicted displacement bias: {0.5 * bias * (t_acc[-1]**2):.6f} m")
print(f"Predicted velocity bias: {bias * t_acc[-1]:.6f} m/s")

print("\n" + "="*120)
print("✅ COMPLETE - Check PNG files in current directory")
print("="*120)
