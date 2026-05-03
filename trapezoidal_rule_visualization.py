import matplotlib.pyplot as plt
import numpy as np

# ============ PART 2: PYTHON FUNCTIONS ============

def trapezoidal_rule_loop(x, y, initial_value=0):
    """
    Calculate cumulative integral using the Trapezoidal Rule with loops.
    
    Parameters:
    -----------
    x : list or 1D array
        X-axis values (e.g., time)
    y : list or 1D array
        Y-axis values (e.g., velocity)
    initial_value : float, optional
        Initial value of the cumulative integral (default is 0)
    
    Returns:
    --------
    displacement : list
        Cumulative integral values at each x point
    """
    n = len(x)
    displacement = [initial_value]  # Start with initial value
    
    # Calculate trapezoid areas and accumulate
    for i in range(n - 1):
        delta_x = x[i + 1] - x[i]
        trapezoid_area = (delta_x / 2) * (y[i] + y[i + 1])
        new_displacement = displacement[i] + trapezoid_area
        displacement.append(new_displacement)
    
    return displacement


def trapezoidal_rule_numpy(x, y, initial_value=0):
    """
    Calculate cumulative integral using the Trapezoidal Rule with NumPy.
    
    Parameters:
    -----------
    x : array-like
        X-axis values (e.g., time)
    y : array-like
        Y-axis values (e.g., velocity)
    initial_value : float, optional
        Initial value of the cumulative integral (default is 0)
    
    Returns:
    --------
    displacement : ndarray
        Cumulative integral values at each x point
    """
    x = np.array(x)
    y = np.array(y)
    
    # Calculate differences between consecutive x values
    delta_x = np.diff(x)
    
    # Calculate trapezoid areas: (Δx/2) * (y[i] + y[i+1])
    trapezoid_areas = (delta_x / 2) * (y[:-1] + y[1:])
    
    # Cumulative sum starting with initial_value
    displacement = np.concatenate(([initial_value], initial_value + np.cumsum(trapezoid_areas)))
    
    return displacement


# ============ PART 3: DESK CHECK VALIDATION ============

# Toy data from the Trapezoidal Rule project
time = [0, 2, 4, 8, 12, 16]
velocity = [0, 4, 3, 0, -4, -2]
initial_value = 3

print("="*70)
print("PART 3: DESK CHECK VALIDATION")
print("="*70)
print("\nInput Data:")
print(f"Time array:           {time}")
print(f"Velocity array:       {velocity}")
print(f"Initial displacement: {initial_value} m")

# Expected results from hand calculations
expected_displacement = [3, 7, 14, 20, 12, 0]

print("\n" + "-"*70)
print("EXPECTED VALUES (from Part 1 hand calculations):")
print("-"*70)
print("Displacement array:", expected_displacement)

print("\n" + "-"*70)
print("TESTING LOOP-BASED FUNCTION:")
print("-"*70)
displacement_loop = trapezoidal_rule_loop(time, velocity, initial_value)
print("Result from trapezoidal_rule_loop():", displacement_loop)

# Detailed trace table for loop function
print("\nDetailed Trace Table (Loop Function):")
print(f"{'i':<3} {'x[i]':<6} {'x[i+1]':<6} {'y[i]':<6} {'y[i+1]':<6} {'Δx':<6} {'Area':<8} {'Cumulative':<12}")
print("-"*70)
print(f"{-1:<3} {'-':<6} {'-':<6} {'-':<6} {'-':<6} {'-':<6} {'-':<8} {initial_value:<12.1f}")

cumulative = initial_value
for i in range(len(time) - 1):
    delta_x = time[i + 1] - time[i]
    area = (delta_x / 2) * (velocity[i] + velocity[i + 1])
    cumulative = cumulative + area
    print(f"{i:<3} {time[i]:<6} {time[i+1]:<6} {velocity[i]:<6} {velocity[i+1]:<6} {delta_x:<6} {area:<8.1f} {cumulative:<12.1f}")

print("\n" + "-"*70)
print("TESTING NUMPY-BASED FUNCTION:")
print("-"*70)
displacement_numpy = trapezoidal_rule_numpy(time, velocity, initial_value)
print("Result from trapezoidal_rule_numpy():", displacement_numpy.tolist())

# Detailed trace table for numpy function
print("\nDetailed Trace Table (NumPy Function):")
print("Step 1: Calculate Δx (differences between consecutive x values)")
delta_x_array = np.diff(time)
print(f"  Δx = np.diff(x) = {delta_x_array}")

print("\nStep 2: Calculate trapezoid areas")
trapezoid_areas = (delta_x_array / 2) * (np.array(velocity[:-1]) + np.array(velocity[1:]))
print(f"  Areas = (Δx/2) × (y[i] + y[i+1]) = {trapezoid_areas}")

print("\nStep 3: Cumulative sum of areas")
cumsum_areas = np.cumsum(trapezoid_areas)
print(f"  Cumsum of areas = {cumsum_areas}")

print("\nStep 4: Add initial value")
displacement_final = initial_value + np.concatenate(([0], cumsum_areas))
print(f"  Displacement = initial_value + cumsum = {displacement_final}")

print("\n" + "-"*70)
print("COMPARISON:")
print("-"*70)
print(f"{'Index':<8} {'Expected':<12} {'Loop Result':<12} {'NumPy Result':<12} {'Match?':<10}")
print("-"*70)

all_match = True
for i in range(len(expected_displacement)):
    loop_val = displacement_loop[i]
    numpy_val = displacement_numpy[i]
    expected_val = expected_displacement[i]
    
    match_loop = abs(loop_val - expected_val) < 1e-10
    match_numpy = abs(numpy_val - expected_val) < 1e-10
    match_all = match_loop and match_numpy
    
    if not match_all:
        all_match = False
    
    match_str = "✓" if match_all else "✗"
    print(f"{i:<8} {expected_val:<12.1f} {loop_val:<12.1f} {numpy_val:<12.1f} {match_str:<10}")

print("-"*70)
if all_match:
    print("✓ SUCCESS: All values match perfectly!")
else:
    print("✗ ERROR: Values do not match. Logic needs to be fixed.")

print("\n" + "="*70)
print("SUMMARY:")
print("="*70)
print(f"Initial displacement:  {displacement_loop[0]} m")
print(f"Final displacement:    {displacement_loop[-1]} m")
print(f"Maximum displacement:  {max(displacement_loop)} m at index {displacement_loop.index(max(displacement_loop))}")
print("="*70 + "\n")


# ============ VISUALIZATION ============

# Create a figure with two subplots
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))

# ============ GRAPH 1: Velocity vs Time with Trapezoids ============
ax1.set_title('Velocity vs Time - Trapezoidal Rule Integration', fontsize=14, fontweight='bold')
ax1.set_xlabel('Time (s)', fontsize=12)
ax1.set_ylabel('Velocity (m/s)', fontsize=12)
ax1.grid(True, alpha=0.3)
ax1.axhline(y=0, color='k', linewidth=0.5)

# Plot the velocity line
ax1.plot(time, velocity, 'o-', color='darkblue', linewidth=2, markersize=8, label='Velocity Data')

# Fill trapezoids and calculate areas for visualization
for i in range(len(time) - 1):
    t1, t2 = time[i], time[i+1]
    v1, v2 = velocity[i], velocity[i+1]
    
    # Create trapezoid coordinates
    x_trap = [t1, t2, t2, t1, t1]
    y_trap = [0, 0, v2, v1, 0]
    
    # Color based on sign (positive = blue, negative = red)
    if v1 >= 0 or v2 >= 0:
        color = 'lightblue'
        alpha = 0.6
    else:
        color = 'lightcoral'
        alpha = 0.6
    
    # Fill the trapezoid
    ax1.fill(x_trap, y_trap, color=color, alpha=alpha, edgecolor='black', linewidth=1.5)
    
    # Calculate and display trapezoid area
    delta_t = t2 - t1
    area = (delta_t / 2) * (v1 + v2)
    mid_x = (t1 + t2) / 2
    mid_y = (v1 + v2) / 2
    
    ax1.text(mid_x, mid_y, f'{area:.0f}m', ha='center', va='center', 
             fontsize=10, fontweight='bold', bbox=dict(boxstyle='round', 
             facecolor='white', alpha=0.8))

ax1.legend(loc='upper right', fontsize=11)
ax1.set_xlim(-1, 17)

# ============ GRAPH 2: Displacement vs Time ============
ax2.set_title('Displacement vs Time - Cumulative Integration', fontsize=14, fontweight='bold')
ax2.set_xlabel('Time (s)', fontsize=12)
ax2.set_ylabel('Displacement (m)', fontsize=12)
ax2.grid(True, alpha=0.3)

# Plot the displacement curve
ax2.plot(time, displacement_loop, 'o-', color='darkgreen', linewidth=2, markersize=8, label='Displacement')

# Fill area under displacement curve
ax2.fill_between(time, 0, displacement_loop, color='lightgreen', alpha=0.5, label='Accumulated Displacement')

# Add value labels on each point
for t, d in zip(time, displacement_loop):
    ax2.text(t, d + 0.8, f'{d}m', ha='center', va='bottom', fontsize=10, fontweight='bold')

# Mark the maximum displacement with a black circle
max_idx = displacement_loop.index(max(displacement_loop))
ax2.plot(time[max_idx], displacement_loop[max_idx], 'o', color='black', markersize=15, 
         label=f'Maximum: {max(displacement_loop)}m', markerfacecolor='none', markeredgewidth=2)

ax2.legend(loc='upper right', fontsize=11)
ax2.set_xlim(-1, 17)
ax2.set_ylim(-2, 24)

# Adjust layout and display
plt.tight_layout()
plt.savefig('trapezoidal_rule_visualization.png', dpi=300, bbox_inches='tight')
print("Graph saved as 'trapezoidal_rule_visualization.png'")
plt.show()
