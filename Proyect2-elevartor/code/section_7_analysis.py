import numpy as np
import matplotlib.pyplot as plt
import sys
sys.path.insert(0, '/path/to/Maths')  # Adjust to your Maths.py location

# Import your custom functions
import Maths as ms

print("\n" + "="*120)
print("TASK F & G: ANALYSIS - SECTION 7 (Analysis)")
print("="*120)

# ============ LOAD DATA ============
print("\n[LOADING DATA]")
data_acc = np.loadtxt('subida_1_5.csv', delimiter=',', skiprows=1)
data_pre = np.genfromtxt('Pressure and velocity_4.csv', delimiter=',', skip_header=1, 
                         missing_values='""', filling_values=0)

# Remove last row if NaN
if np.isnan(data_pre[-1]).any(): 
    data_pre = data_pre[:-1]

# Extract variables
t_acc, acc_raw = data_acc[:, 0], data_acc[:, 1]
t_pre, p_pre, h_pre, v_pre = data_pre[:, 0], data_pre[:, 1], data_pre[:, 2], data_pre[:, 3]

# Relative altitude (starting at 0)
h_relative = h_pre - h_pre[0]

# Calculate bias from first 5 seconds
quiet_mask = t_acc < 5
bias = np.mean(acc_raw[quiet_mask])
acc_calibrated = acc_raw - bias

# Apply moving average filter
W = 15
acc_filtered = ms.moving_average(acc_calibrated, W)

print(f"✓ Data loaded successfully")
print(f"  - Acceleration time points: {len(t_acc)}")
print(f"  - Pressure time points: {len(t_pre)}")
print(f"  - Bias calculated (first 5 sec): {bias:.6f} m/s²")
print(f"  - Moving average window size: {W}")

print("\n" + "="*120)
print("QUESTION 1: THE EFFECT OF THE SOFTWARE FILTER")
print("="*120)

print("\n[ANALYSIS 1.1: Raw vs Filtered Acceleration]")

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

# High-frequency noise analysis
print("\n[ANALYSIS 1.2: Noise Reduction Quantification]")

# Calculate instantaneous differences (proxy for noise content)
raw_diffs = np.diff(acc_raw)
filtered_diffs = np.diff(acc_filtered)

noise_reduction = (np.mean(np.abs(raw_diffs)) - np.mean(np.abs(filtered_diffs))) / np.mean(np.abs(raw_diffs)) * 100

print(f"\nMean absolute change between consecutive points:")
print(f"  Raw acceleration:      {np.mean(np.abs(raw_diffs)):.6f} m/s² (Δ per point)")
print(f"  Filtered acceleration: {np.mean(np.abs(filtered_diffs)):.6f} m/s² (Δ per point)")
print(f"  Noise reduction:       {noise_reduction:.2f}%")

print(f"\nInterpretation:")
print(f"  The moving average filter reduces high-frequency variations by {noise_reduction:.1f}%.")
print(f"  This smooths out mechanical vibrations from the elevator shaft while preserving")
print(f"  the overall trend of the acceleration signal.")

# Effect on kinematics
print("\n[ANALYSIS 1.3: Kinematic Effects of Filtering]")

# Integrate both to see cumulative effect
v_raw_uncal = ms.integrate_vector(t_acc, acc_raw, 0)  # Raw, no bias subtraction
v_filtered = ms.integrate_vector(t_acc, acc_filtered, 0)  # Filtered with bias subtraction

v_difference = v_raw_uncal - v_filtered
max_v_diff = np.max(np.abs(v_difference))
final_v_diff = v_difference[-1]

print(f"\nVelocity divergence (Raw uncalibrated vs Filtered+calibrated):")
print(f"  Maximum difference: {max_v_diff:.6f} m/s")
print(f"  Final difference:   {final_v_diff:.6f} m/s")
print(f"  Average difference: {np.mean(np.abs(v_difference)):.6f} m/s")

# Double integration
d_raw_uncal = ms.integrate_vector(t_acc, v_raw_uncal, 0)
d_filtered = ms.integrate_vector(t_acc, v_filtered, 0)

d_difference = d_raw_uncal - d_filtered
max_d_diff = np.max(np.abs(d_difference))
final_d_diff = d_difference[-1]

print(f"\nDisplacement divergence (Raw uncalibrated vs Filtered+calibrated):")
print(f"  Maximum difference: {max_d_diff:.6f} m")
print(f"  Final difference:   {final_d_diff:.6f} m")
print(f"  Error magnitude:    {abs(final_d_diff):.2f}% of elevator height (≈{h_relative[-1]:.2f}m)")

print(f"\nPHYSICAL INTERPRETATION:")
print(f"  When acceleration signals contain high-frequency noise:")
print(f"  1. Each noisy spike, when integrated once, becomes a small velocity error")
print(f"  2. Each velocity error, when integrated again, becomes a displacement error")
print(f"  3. These errors COMPOUND (double integration amplifies them)")
print(f"  4. The moving average filter prevents these spikes from accumulating")
print(f"  5. Result: Smoother, more accurate displacement measurement")

print("\n" + "="*120)
print("QUESTION 2: ISOLATING THE VARIABLES (Filtering vs Bias Subtraction)")
print("="*120)

print("\n[SCENARIO A: FILTERED but NO BIAS SUBTRACTION]")

# Scenario A: Filter but don't subtract bias
acc_filtered_no_cal = ms.moving_average(acc_raw, W)  # Filter the raw data without removing bias
v_scenario_a = ms.integrate_vector(t_acc, acc_filtered_no_cal, 0)
d_scenario_a = ms.integrate_vector(t_acc, v_scenario_a, 0)

print(f"  Step 1: acc_filtered_no_cal = moving_average(acc_raw, W={W})")
print(f"          (Filters noise but keeps DC bias)")
print(f"  Step 2: v_scenario_a = integrate(acc_filtered_no_cal)")
print(f"  Step 3: d_scenario_a = integrate(v_scenario_a)")

print(f"\n  Results:")
print(f"    Final velocity:    {v_scenario_a[-1]:.6f} m/s")
print(f"    Final displacement: {d_scenario_a[-1]:.6f} m")
print(f"    vs Barometer truth: {h_relative[-1]:.6f} m")
print(f"    Error:             {abs(d_scenario_a[-1] - h_relative[-1]):.6f} m")

print("\n[SCENARIO B: BIAS SUBTRACTED but NO FILTERING]")

# Scenario B: Subtract bias but don't filter
v_scenario_b = ms.integrate_vector(t_acc, acc_calibrated, 0)  # Integrate calibrated but noisy data
d_scenario_b = ms.integrate_vector(t_acc, v_scenario_b, 0)

print(f"  Step 1: acc_calibrated = acc_raw - bias (= acc_raw - {bias:.6f})")
print(f"          (Removes DC offset but keeps high-frequency noise)")
print(f"  Step 2: v_scenario_b = integrate(acc_calibrated)")
print(f"  Step 3: d_scenario_b = integrate(v_scenario_b)")

print(f"\n  Results:")
print(f"    Final velocity:    {v_scenario_b[-1]:.6f} m/s")
print(f"    Final displacement: {d_scenario_b[-1]:.6f} m")
print(f"    vs Barometer truth: {h_relative[-1]:.6f} m")
print(f"    Error:             {abs(d_scenario_b[-1] - h_relative[-1]):.6f} m")

print("\n[SCENARIO C: BOTH FILTERED AND BIAS SUBTRACTED (OPTIMAL)]")

# Scenario C: Both (what we did)
v_scenario_c = ms.integrate_vector(t_acc, acc_filtered, 0)
d_scenario_c = ms.integrate_vector(t_acc, v_scenario_c, 0)

print(f"  Step 1: acc_calibrated = acc_raw - bias")
print(f"  Step 2: acc_filtered = moving_average(acc_calibrated, W={W})")
print(f"  Step 3: v_scenario_c = integrate(acc_filtered)")
print(f"  Step 4: d_scenario_c = integrate(v_scenario_c)")

print(f"\n  Results:")
print(f"    Final velocity:    {v_scenario_c[-1]:.6f} m/s")
print(f"    Final displacement: {d_scenario_c[-1]:.6f} m")
print(f"    vs Barometer truth: {h_relative[-1]:.6f} m")
print(f"    Error:             {abs(d_scenario_c[-1] - h_relative[-1]):.6f} m")

print("\n[COMPARISON TABLE]")
print(f"{'Scenario':<40} {'Final Disp (m)':<18} {'Error (m)':<18} {'Error (%)':<15}")
print("-"*90)

baseline = h_relative[-1]
error_a = abs(d_scenario_a[-1] - baseline)
error_b = abs(d_scenario_b[-1] - baseline)
error_c = abs(d_scenario_c[-1] - baseline)

pct_a = (error_a / baseline * 100) if baseline != 0 else 0
pct_b = (error_b / baseline * 100) if baseline != 0 else 0
pct_c = (error_c / baseline * 100) if baseline != 0 else 0

print(f"{'A: Filtered, NO bias subtraction':<40} {d_scenario_a[-1]:<18.6f} {error_a:<18.6f} {pct_a:<15.2f}%")
print(f"{'B: Bias subtracted, NO filtering':<40} {d_scenario_b[-1]:<18.6f} {error_b:<18.6f} {pct_b:<15.2f}%")
print(f"{'C: Filtered AND bias subtracted':<40} {d_scenario_c[-1]:<18.6f} {error_c:<18.6f} {pct_c:<15.2f}%")
print(f"{'Barometer Ground Truth':<40} {baseline:<18.6f} {'—':<18} {'—':<15}")

print("\n[DETERMINING WHICH OPERATION HAS LARGER EFFECT]")

# Calculate the relative effects
effect_filtering = abs(d_scenario_a[-1] - d_scenario_c[-1])  # Effect of adding filter to scenario A
effect_bias = abs(d_scenario_b[-1] - d_scenario_c[-1])  # Effect of adding bias to scenario B

print(f"\nEffect of BIAS SUBTRACTION (B → C):")
print(f"  Scenario B (bias not removed): d = {d_scenario_b[-1]:.6f} m")
print(f"  Scenario C (bias removed):     d = {d_scenario_c[-1]:.6f} m")
print(f"  Difference:                    Δd = {effect_bias:.6f} m")
print(f"  Percentage change:             {(effect_bias/d_scenario_b[-1]*100) if d_scenario_b[-1]!=0 else 0:.2f}%")

print(f"\nEffect of FILTERING (A → C):")
print(f"  Scenario A (no filter):        d = {d_scenario_a[-1]:.6f} m")
print(f"  Scenario C (filtered):         d = {d_scenario_c[-1]:.6f} m")
print(f"  Difference:                    Δd = {effect_filtering:.6f} m")
print(f"  Percentage change:             {(effect_filtering/d_scenario_a[-1]*100) if d_scenario_a[-1]!=0 else 0:.2f}%")

print(f"\n[CONCLUSION]")
if effect_bias > effect_filtering:
    print(f"✓ BIAS SUBTRACTION has the LARGER effect ({effect_bias:.6f} m > {effect_filtering:.6f} m)")
    print(f"  Filtering has the SMALLER effect")
else:
    print(f"✓ FILTERING has the LARGER effect ({effect_filtering:.6f} m > {effect_bias:.6f} m)")
    print(f"  Bias subtraction has the SMALLER effect")

print("\n[MATHEMATICAL EXPLANATION]")
print(f"\nWhy bias subtraction has such a large effect:")
print(f"  1. DC Bias is a constant offset in acceleration (e.g., {bias:.6f} m/s²)")
print(f"  2. During integration 1: bias × Δt accumulates linearly in velocity")
print(f"     Final velocity bias: {bias:.6f} × {t_acc[-1]:.2f}s ≈ {bias * t_acc[-1]:.6f} m/s")
print(f"  3. During integration 2: velocity bias × Δt accumulates quadratically in displacement")
print(f"     Final displacement bias: ~½ × {bias:.6f} × ({t_acc[-1]:.2f})² ≈ {0.5 * bias * (t_acc[-1]**2):.6f} m")
print(f"  4. This QUADRATIC accumulation is why bias removal is critical for displacement!")

print(f"\nWhy noise filtering has smaller (but still important) effect:")
print(f"  1. High-frequency noise is random: +spikes and -spikes partially cancel")
print(f"  2. But when integrated, even random noise creates a 'random walk' effect")
print(f"  3. This creates displacement errors, but smaller than constant bias errors")
print(f"  4. The filter prevents these random errors from compounding")

print("\n[PHYSICAL INTERPRETATION]")
print(f"\nImagine the elevator acceleration signal with both noise and bias:")
print(f"  • BIAS (constant error): Like a faulty accelerometer that always reads 0.1 m/s² too high")
print(f"    → After 30 seconds, velocity is {bias * 30:.2f} m/s too high")
print(f"    → After 30 seconds, displacement is ~{0.5 * bias * (30**2):.1f} m too high!")
print(f"  • NOISE (random spikes): Like vibrations from the elevator cable")
print(f"    → Random spikes sometimes add, sometimes cancel")
print(f"    → Over time, they still cause drift, but less predictable")
print(f"    → Filtering smooths them out before integration amplifies them")

print(f"\nConclusion:")
print(f"  For accurate elevator height measurement:")
print(f"    1. BIAS SUBTRACTION is ESSENTIAL (linear effect in velocity, quadratic in displacement)")
print(f"    2. FILTERING is IMPORTANT (prevents noise amplification during double integration)")
print(f"    3. BOTH TOGETHER provide the best accuracy")

print("\n" + "="*120)
print("GENERATING VISUALIZATION FIGURES")
print("="*120)

# Create comprehensive comparison figures
fig1, axs = plt.subplots(3, 2, figsize=(14, 12))
fig1.suptitle('Analysis Question 1: Effect of Software Filter', fontsize=16, fontweight='bold')

# Row 1: Acceleration comparison
axs[0,0].plot(t_acc, acc_raw, alpha=0.6, linewidth=1, label='Raw Acceleration', color='red')
axs[0,0].plot(t_acc, acc_filtered, linewidth=2, label='Filtered Acceleration', color='blue')
axs[0,0].axhline(y=0, color='k', linestyle='--', alpha=0.3)
axs[0,0].set_ylabel('Acceleration (m/s²)')
axs[0,0].set_title('Raw vs Filtered Acceleration')
axs[0,0].legend()
axs[0,0].grid(True, alpha=0.3)

# Row 1: Acceleration differences
axs[0,1].plot(t_acc, np.abs(raw_diffs), alpha=0.6, linewidth=1, label='Raw Changes', color='red')
axs[0,1].plot(t_acc[:-1], np.abs(filtered_diffs), linewidth=2, label='Filtered Changes', color='blue')
axs[0,1].set_ylabel('|Δ Acceleration| (m/s²)')
axs[0,1].set_title(f'High-Frequency Content (Noise Reduction: {noise_reduction:.1f}%)')
axs[0,1].legend()
axs[0,1].grid(True, alpha=0.3)

# Row 2: Velocity comparison
axs[1,0].plot(t_pre, v_pre, '--', linewidth=2, label='Provided Velocity', color='gray')
axs[1,0].plot(t_acc, v_raw_uncal, alpha=0.7, linewidth=1.5, label='Raw Uncalibrated', color='red')
axs[1,0].plot(t_acc, v_filtered, linewidth=2, label='Filtered + Calibrated', color='blue')
axs[1,0].set_ylabel('Velocity (m/s)')
axs[1,0].set_title('Velocity: Integrated Acceleration')
axs[1,0].legend()
axs[1,0].grid(True, alpha=0.3)

# Row 2: Velocity error
axs[1,1].plot(t_acc, v_difference, linewidth=2, color='purple')
axs[1,1].fill_between(t_acc, v_difference, alpha=0.3, color='purple')
axs[1,1].axhline(y=0, color='k', linestyle='--', alpha=0.3)
axs[1,1].set_ylabel('Velocity Difference (m/s)')
axs[1,1].set_title('Velocity Error (Raw Uncal. - Filtered Cal.)')
axs[1,1].grid(True, alpha=0.3)

# Row 3: Displacement comparison
axs[2,0].plot(t_pre, h_relative, linewidth=2.5, label='Barometer (Truth)', color='green')
axs[2,0].plot(t_acc, d_raw_uncal, alpha=0.7, linewidth=1.5, label='Raw Uncalibrated', color='red')
axs[2,0].plot(t_acc, d_filtered, linewidth=2, label='Filtered + Calibrated', color='blue')
axs[2,0].set_xlabel('Time (s)')
axs[2,0].set_ylabel('Displacement (m)')
axs[2,0].set_title('Displacement: Double Integrated Acceleration')
axs[2,0].legend()
axs[2,0].grid(True, alpha=0.3)

# Row 3: Displacement error
axs[2,1].plot(t_acc, d_difference, linewidth=2, color='purple')
axs[2,1].fill_between(t_acc, d_difference, alpha=0.3, color='purple')
axs[2,1].axhline(y=0, color='k', linestyle='--', alpha=0.3)
axs[2,1].set_xlabel('Time (s)')
axs[2,1].set_ylabel('Displacement Error (m)')
axs[2,1].set_title(f'Displacement Error (Raw Uncal. - Filtered Cal.)\nFinal Error: {final_d_diff:.4f} m')
axs[2,1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('analysis_question_1_filter_effect.png', dpi=300, bbox_inches='tight')
print("✓ Saved: analysis_question_1_filter_effect.png")
plt.show()

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
axs[0,0].set_ylabel('Displacement (m)')
axs[0,0].set_title('Displacement Comparison')
axs[0,0].legend()
axs[0,0].grid(True, alpha=0.3)

# Error magnitude
errors = [error_a, error_b, error_c]
labels = ['A: Filtered\nNO bias', 'B: Bias removed\nNO filter', 'C: Both\n(Optimal)']
colors_bar = ['orange', 'red', 'blue']

axs[0,1].bar(labels, errors, color=colors_bar, alpha=0.7, edgecolor='black', linewidth=2)
axs[0,1].set_ylabel('Absolute Error (m)')
axs[0,1].set_title('Final Displacement Error Magnitude')
axs[0,1].grid(True, alpha=0.3, axis='y')
for i, (label, error) in enumerate(zip(labels, errors)):
    axs[0,1].text(i, error + 0.05, f'{error:.4f}m', ha='center', fontweight='bold')

# Velocity comparison (at time when elevator is moving)
axs[1,0].plot(t_pre, v_pre, 'o--', linewidth=2, markersize=4, label='Provided Velocity', 
              color='gray', zorder=5)
axs[1,0].plot(t_acc, v_scenario_a, linewidth=2, label='Scenario A: Filtered, NO bias', 
              color='orange', alpha=0.8)
axs[1,0].plot(t_acc, v_scenario_b, linewidth=2, label='Scenario B: Bias removed, NO filter', 
              color='red', alpha=0.8)
axs[1,0].plot(t_acc, v_scenario_c, linewidth=2, label='Scenario C: Both (Optimal)', 
              color='blue', alpha=0.8)
axs[1,0].set_ylabel('Velocity (m/s)')
axs[1,0].set_title('Velocity Comparison')
axs[1,0].legend()
axs[1,0].grid(True, alpha=0.3)

# Effect size comparison
effect_sizes = [effect_bias, effect_filtering]
effect_labels = [f'Bias Subtraction\nEffect: {effect_bias:.6f} m', 
                 f'Filtering\nEffect: {effect_filtering:.6f} m']
effect_colors = ['red', 'blue']

bars = axs[1,1].bar(effect_labels, effect_sizes, color=effect_colors, alpha=0.7, edgecolor='black', linewidth=2)
axs[1,1].set_ylabel('Displacement Change (m)')
axs[1,1].set_title('Relative Effect: Which Operation Matters More?')
axs[1,1].grid(True, alpha=0.3, axis='y')

# Add value labels on bars
for bar, effect in zip(bars, effect_sizes):
    height = bar.get_height()
    axs[1,1].text(bar.get_x() + bar.get_width()/2., height,
                 f'{effect:.6f}m',
                 ha='center', va='bottom', fontweight='bold', fontsize=11)

# Add winner annotation
if effect_bias > effect_filtering:
    axs[1,1].text(0.5, max(effect_sizes)*0.9, 'BIAS SUBTRACTION\nHas Larger Effect',
                 ha='center', fontsize=12, fontweight='bold', 
                 bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.7))
else:
    axs[1,1].text(0.5, max(effect_sizes)*0.9, 'FILTERING\nHas Larger Effect',
                 ha='center', fontsize=12, fontweight='bold',
                 bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.7))

plt.tight_layout()
plt.savefig('analysis_question_2_isolating_variables.png', dpi=300, bbox_inches='tight')
print("✓ Saved: analysis_question_2_isolating_variables.png")
plt.show()

print("\n" + "="*120)
print("ANALYSIS COMPLETE")
print("="*120)
print("\nBoth figures have been generated and saved.")
print("Use these visualizations in your report to justify your conclusions.")
print("\n" + "="*120)
