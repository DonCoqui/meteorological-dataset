import matplotlib.pyplot as plt
import numpy as np

print("\n" + "="*100)
print("TASK A: TRAPEZOIDAL RULE - NUMERICAL INTEGRATION")
print("="*100)

# ============ PART 1: PRELIMINARY HAND CALCULATIONS ============

print("\n" + "="*100)
print("PART 1: PRELIMINARY HAND CALCULATIONS")
print("="*100)

t = [0, 2, 4, 8, 12, 16]
v = [0, 4, 3, 0, -4, -2]
initial_value = 3

print("\nInput Data:")
print(f"t (Time array):              {t}")
print(f"v (Velocity array):          {v}")
print(f"initial_value (Initial displacement): {initial_value} m")

print("\n" + "-"*100)
print("MANUAL TRAPEZOID AREA CALCULATIONS:")
print("-"*100)

print("\nTrapezoid 0 (between t[0] and t[1]):")
print(f"  t[0] = {t[0]}, t[1] = {t[1]} → Δt = {t[1]} - {t[0]} = {t[1] - t[0]} s")
print(f"  v[0] = {v[0]}, v[1] = {v[1]} m/s")
area_0 = ((t[1] - t[0]) / 2) * (v[0] + v[1])
print(f"  Area = (Δt/2) × (v[0] + v[1]) = ({t[1] - t[0]}/2) × ({v[0]} + {v[1]}) = {area_0} m")

print("\nTrapezoid 1 (between t[1] and t[2]):")
print(f"  t[1] = {t[1]}, t[2] = {t[2]} → Δt = {t[2]} - {t[1]} = {t[2] - t[1]} s")
print(f"  v[1] = {v[1]}, v[2] = {v[2]} m/s")
area_1 = ((t[2] - t[1]) / 2) * (v[1] + v[2])
print(f"  Area = (Δt/2) × (v[1] + v[2]) = ({t[2] - t[1]}/2) × ({v[1]} + {v[2]}) = {area_1} m")

print("\nTrapezoid 2 (between t[2] and t[3]):")
print(f"  t[2] = {t[2]}, t[3] = {t[3]} → Δt = {t[3]} - {t[2]} = {t[3] - t[2]} s")
print(f"  v[2] = {v[2]}, v[3] = {v[3]} m/s")
area_2 = ((t[3] - t[2]) / 2) * (v[2] + v[3])
print(f"  Area = (Δt/2) × (v[2] + v[3]) = ({t[3] - t[2]}/2) × ({v[2]} + {v[3]}) = {area_2} m")

print("\nTrapezoid 3 (between t[3] and t[4]):")
print(f"  t[3] = {t[3]}, t[4] = {t[4]} → Δt = {t[4]} - {t[3]} = {t[4] - t[3]} s")
print(f"  v[3] = {v[3]}, v[4] = {v[4]} m/s")
area_3 = ((t[4] - t[3]) / 2) * (v[3] + v[4])
print(f"  Area = (Δt/2) × (v[3] + v[4]) = ({t[4] - t[3]}/2) × ({v[3]} + {v[4]}) = {area_3} m")

print("\nTrapezoid 4 (between t[4] and t[5]):")
print(f"  t[4] = {t[4]}, t[5] = {t[5]} → Δt = {t[5]} - {t[4]} = {t[5] - t[4]} s")
print(f"  v[4] = {v[4]}, v[5] = {v[5]} m/s")
area_4 = ((t[5] - t[4]) / 2) * (v[4] + v[5])
print(f"  Area = (Δt/2) × (v[4] + v[5]) = ({t[5] - t[4]}/2) × ({v[4]} + {v[5]}) = {area_4} m")

print("\n" + "-"*100)
print("CUMULATIVE DISPLACEMENT (RUNNING SUM):")
print("-"*100)

cumulative_0 = initial_value
print(f"\nIndex 0: displacement[0] = initial_value = {cumulative_0} m")

cumulative_1 = cumulative_0 + area_0
print(f"Index 1: displacement[1] = displacement[0] + area_0 = {cumulative_0} + {area_0} = {cumulative_1} m")

cumulative_2 = cumulative_1 + area_1
print(f"Index 2: displacement[2] = displacement[1] + area_1 = {cumulative_1} + {area_1} = {cumulative_2} m")

cumulative_3 = cumulative_2 + area_2
print(f"Index 3: displacement[3] = displacement[2] + area_2 = {cumulative_2} + {area_2} = {cumulative_3} m")

cumulative_4 = cumulative_3 + area_3
print(f"Index 4: displacement[4] = displacement[3] + area_3 = {cumulative_3} + {area_3} = {cumulative_4} m")

cumulative_5 = cumulative_4 + area_4
print(f"Index 5: displacement[5] = displacement[4] + area_4 = {cumulative_4} + {area_4} = {cumulative_5} m")

expected_displacement = [cumulative_0, cumulative_1, cumulative_2, cumulative_3, cumulative_4, cumulative_5]
print("\n" + "-"*100)
print(f"EXPECTED DISPLACEMENT ARRAY: {expected_displacement}")
print(f"Final displacement: {cumulative_5} m")
print(f"Maximum displacement: {max(expected_displacement)} m")
print("-"*100)


# ============ PART 2: PYTHON FUNCTIONS ============

print("\n" + "="*100)
print("PART 2: PYTHON FUNCTIONS")
print("="*100)

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

print("\n" + "="*100)
print("PART 3: DESK CHECK VALIDATION")
print("="*100)

print("\n" + "-"*100)
print("FUNCTION: trapezoidal_rule_loop(x, y, initial_value)")
print("-"*100)

print("\nINPUT PARAMETERS:")
print(f"  x = {t}")
print(f"  y = {v}")
print(f"  initial_value = {initial_value}")

print("\nINITIAL STATE:")
print(f"  n = len(x) = len({t}) = {len(t)}")
print(f"  displacement = [initial_value] = [{initial_value}]")
print(f"  Loop will execute: for i in range({len(t)} - 1) = range(5) = [0, 1, 2, 3, 4]")

print("\n" + "DETAILED STEP-BY-STEP EXECUTION:" + "-"*80)

print("\n[ITERATION i=0]")
print(f"  i = 0")
print(f"  x[i] = x[0] = {t[0]}")
print(f"  x[i+1] = x[1] = {t[1]}")
print(f"  y[i] = y[0] = {v[0]}")
print(f"  y[i+1] = y[1] = {v[1]}")
print(f"  delta_x = x[i+1] - x[i] = {t[1]} - {t[0]} = {t[1] - t[0]}")
print(f"  trapezoid_area = (delta_x / 2) × (y[i] + y[i+1])")
print(f"               = ({t[1] - t[0]} / 2) × ({v[0]} + {v[1]})")
print(f"               = {(t[1] - t[0]) / 2} × {v[0] + v[1]}")
print(f"               = {((t[1] - t[0]) / 2) * (v[0] + v[1])}")
print(f"  new_displacement = displacement[i] + trapezoid_area")
print(f"                   = displacement[0] + {((t[1] - t[0]) / 2) * (v[0] + v[1])}")
print(f"                   = {initial_value} + {((t[1] - t[0]) / 2) * (v[0] + v[1])}")
print(f"                   = {initial_value + ((t[1] - t[0]) / 2) * (v[0] + v[1])}")
print(f"  displacement.append({initial_value + ((t[1] - t[0]) / 2) * (v[0] + v[1])})")
print(f"  displacement = [{initial_value}, {initial_value + ((t[1] - t[0]) / 2) * (v[0] + v[1])}]")

print("\n[ITERATION i=1]")
print(f"  i = 1")
print(f"  x[i] = x[1] = {t[1]}")
print(f"  x[i+1] = x[2] = {t[2]}")
print(f"  y[i] = y[1] = {v[1]}")
print(f"  y[i+1] = y[2] = {v[2]}")
print(f"  delta_x = x[i+1] - x[i] = {t[2]} - {t[1]} = {t[2] - t[1]}")
print(f"  trapezoid_area = (delta_x / 2) × (y[i] + y[i+1])")
print(f"               = ({t[2] - t[1]} / 2) × ({v[1]} + {v[2]})")
print(f"               = {(t[2] - t[1]) / 2} × {v[1] + v[2]}")
print(f"               = {((t[2] - t[1]) / 2) * (v[1] + v[2])}")
print(f"  new_displacement = displacement[i] + trapezoid_area")
print(f"                   = displacement[1] + {((t[2] - t[1]) / 2) * (v[1] + v[2])}")
print(f"                   = {cumulative_1} + {((t[2] - t[1]) / 2) * (v[1] + v[2])}")
print(f"                   = {cumulative_1 + ((t[2] - t[1]) / 2) * (v[1] + v[2])}")
print(f"  displacement.append({cumulative_1 + ((t[2] - t[1]) / 2) * (v[1] + v[2])})")
print(f"  displacement = [{initial_value}, {cumulative_1}, {cumulative_1 + ((t[2] - t[1]) / 2) * (v[1] + v[2])}]")

print("\n[ITERATION i=2]")
print(f"  i = 2")
print(f"  x[i] = x[2] = {t[2]}")
print(f"  x[i+1] = x[3] = {t[3]}")
print(f"  y[i] = y[2] = {v[2]}")
print(f"  y[i+1] = y[3] = {v[3]}")
print(f"  delta_x = x[i+1] - x[i] = {t[3]} - {t[2]} = {t[3] - t[2]}")
print(f"  trapezoid_area = (delta_x / 2) × (y[i] + y[i+1])")
print(f"               = ({t[3] - t[2]} / 2) × ({v[2]} + {v[3]})")
print(f"               = {(t[3] - t[2]) / 2} × {v[2] + v[3]}")
print(f"               = {((t[3] - t[2]) / 2) * (v[2] + v[3])}")
print(f"  new_displacement = displacement[i] + trapezoid_area")
print(f"                   = displacement[2] + {((t[3] - t[2]) / 2) * (v[2] + v[3])}")
print(f"                   = {cumulative_2} + {((t[3] - t[2]) / 2) * (v[2] + v[3])}")
print(f"                   = {cumulative_2 + ((t[3] - t[2]) / 2) * (v[2] + v[3])}")
print(f"  displacement.append({cumulative_2 + ((t[3] - t[2]) / 2) * (v[2] + v[3])})")
print(f"  displacement = [{initial_value}, {cumulative_1}, {cumulative_2}, {cumulative_2 + ((t[3] - t[2]) / 2) * (v[2] + v[3])}]")

print("\n[ITERATION i=3]")
print(f"  i = 3")
print(f"  x[i] = x[3] = {t[3]}")
print(f"  x[i+1] = x[4] = {t[4]}")
print(f"  y[i] = y[3] = {v[3]}")
print(f"  y[i+1] = y[4] = {v[4]}")
print(f"  delta_x = x[i+1] - x[i] = {t[4]} - {t[3]} = {t[4] - t[3]}")
print(f"  trapezoid_area = (delta_x / 2) × (y[i] + y[i+1])")
print(f"               = ({t[4] - t[3]} / 2) × ({v[3]} + {v[4]})")
print(f"               = {(t[4] - t[3]) / 2} × {v[3] + v[4]}")
print(f"               = {((t[4] - t[3]) / 2) * (v[3] + v[4])}")
print(f"  new_displacement = displacement[i] + trapezoid_area")
print(f"                   = displacement[3] + {((t[4] - t[3]) / 2) * (v[3] + v[4])}")
print(f"                   = {cumulative_3} + {((t[4] - t[3]) / 2) * (v[3] + v[4])}")
print(f"                   = {cumulative_3 + ((t[4] - t[3]) / 2) * (v[3] + v[4])}")
print(f"  displacement.append({cumulative_3 + ((t[4] - t[3]) / 2) * (v[3] + v[4])})")
print(f"  displacement = [{initial_value}, {cumulative_1}, {cumulative_2}, {cumulative_3}, {cumulative_3 + ((t[4] - t[3]) / 2) * (v[3] + v[4])}]")

print("\n[ITERATION i=4]")
print(f"  i = 4")
print(f"  x[i] = x[4] = {t[4]}")
print(f"  x[i+1] = x[5] = {t[5]}")
print(f"  y[i] = y[4] = {v[4]}")
print(f"  y[i+1] = y[5] = {v[5]}")
print(f"  delta_x = x[i+1] - x[i] = {t[5]} - {t[4]} = {t[5] - t[4]}")
print(f"  trapezoid_area = (delta_x / 2) × (y[i] + y[i+1])")
print(f"               = ({t[5] - t[4]} / 2) × ({v[4]} + {v[5]})")
print(f"               = {(t[5] - t[4]) / 2} × {v[4] + v[5]}")
print(f"               = {((t[5] - t[4]) / 2) * (v[4] + v[5])}")
print(f"  new_displacement = displacement[i] + trapezoid_area")
print(f"                   = displacement[4] + {((t[5] - t[4]) / 2) * (v[4] + v[5])}")
print(f"                   = {cumulative_4} + {((t[5] - t[4]) / 2) * (v[4] + v[5])}")
print(f"                   = {cumulative_4 + ((t[5] - t[4]) / 2) * (v[4] + v[5])}")
print(f"  displacement.append({cumulative_4 + ((t[5] - t[4]) / 2) * (v[4] + v[5])})")
print(f"  displacement = [{initial_value}, {cumulative_1}, {cumulative_2}, {cumulative_3}, {cumulative_4}, {cumulative_4 + ((t[5] - t[4]) / 2) * (v[4] + v[5])}]")

print("\nLOOP ENDS (i = 5 is not in range(5))")

print("\nRETURN:")
print(f"  return displacement = [{initial_value}, {cumulative_1}, {cumulative_2}, {cumulative_3}, {cumulative_4}, {cumulative_4 + ((t[5] - t[4]) / 2) * (v[4] + v[5])}]")

print("\n" + "-"*100)
print("TESTING LOOP-BASED FUNCTION")
print("-"*100)

displacement_loop = trapezoidal_rule_loop(t, v, initial_value)
print(f"\nResult: displacement_loop = {displacement_loop}")

print("\nTrace Table - Loop Function:")
print(f"{'i':<4} {'t[i]':<8} {'t[i+1]':<8} {'v[i]':<8} {'v[i+1]':<8} {'Δt':<8} {'trapezoid_area':<18} {'displacement[i]':<18} {'After append':<20}")
print("-"*120)
print(f"{'—':<4} {'—':<8} {'—':<8} {'—':<8} {'—':<8} {'—':<8} {'—':<18} {'—':<18} {initial_value:<20}")

for i in range(len(t) - 1):
    delta_t = t[i+1] - t[i]
    trap_area = (delta_t / 2) * (v[i] + v[i+1])
    disp_before = displacement_loop[i]
    disp_after = displacement_loop[i+1]
    print(f"{i:<4} {t[i]:<8} {t[i+1]:<8} {v[i]:<8} {v[i+1]:<8} {delta_t:<8} {trap_area:<18.1f} {disp_before:<18.1f} {disp_after:<20.1f}")

print("\n" + "-"*100)
print("TESTING NUMPY-BASED FUNCTION")
print("-"*100)

displacement_numpy = trapezoidal_rule_numpy(t, v, initial_value)
print(f"\nResult: displacement_numpy = {displacement_numpy.tolist()}")

print("\nTrace Table - NumPy Function (step-by-step operations):")
print("\nStep 1: Convert to NumPy arrays")
print(f"  x = np.array({t})")
print(f"  y = np.array({v})")

print("\nStep 2: Calculate delta_x = np.diff(x)")
delta_x_array = np.diff(t)
print(f"  delta_x = {delta_x_array.tolist()}")

print("\nStep 3: Calculate trapezoid_areas = (delta_x / 2) × (y[:-1] + y[1:])")
print(f"  y[:-1] = {v[:-1]} (all except last)")
print(f"  y[1:] = {v[1:]} (all except first)")
print(f"  y[:-1] + y[1:] = {[v[i] + v[i+1] for i in range(len(v)-1)]}")
trap_areas_array = (delta_x_array / 2) * (np.array(v[:-1]) + np.array(v[1:]))
print(f"  trapezoid_areas = {trap_areas_array.tolist()}")

print("\nStep 4: Calculate cumulative sum = np.cumsum(trapezoid_areas)")
cumsum_areas = np.cumsum(trap_areas_array)
print(f"  cumsum = {cumsum_areas.tolist()}")

print("\nStep 5: Add initial_value and concatenate")
print(f"  initial_value + cumsum = {initial_value} + {cumsum_areas.tolist()}")
print(f"                         = {(initial_value + cumsum_areas).tolist()}")
print(f"  np.concatenate(([{initial_value}], [combined])) = {displacement_numpy.tolist()}")

print("\n" + "-"*100)
print("COMPARISON: Expected vs Loop vs NumPy")
print("-"*100)
print(f"{'Index':<8} {'t[i]':<8} {'Expected':<15} {'Loop':<15} {'NumPy':<15} {'Match?':<10}")
print("-"*100)

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
    print(f"{i:<8} {t[i]:<8} {expected_val:<15.1f} {loop_val:<15.1f} {numpy_val:<15.1f} {match_str:<10}")

print("-"*100)
if all_match:
    print("✓ SUCCESS: All values match perfectly!")
else:
    print("✗ ERROR: Values do not match. Logic needs to be fixed.")

print("\n" + "="*100)
print("SUMMARY:")
print("="*100)
print(f"Displacement Array (Loop):    {[f'{v:.1f}' for v in displacement_loop]}")
print(f"Displacement Array (NumPy):   {[f'{v:.1f}' for v in displacement_numpy]}")
print(f"Expected Displacement Array:  {[f'{v:.1f}' for v in expected_displacement]}")
print(f"\nInitial Displacement:  {displacement_loop[0]} m")
print(f"Final Displacement:    {displacement_loop[-1]} m")
print(f"Maximum Displacement:  {max(displacement_loop)} m at index {displacement_loop.index(max(displacement_loop))}")
print("="*100 + "\n")


# ============ VISUALIZATION ============

print("Generating visualization graphs...")

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))

# ============ GRAPH 1: Velocity vs Time with Trapezoids ============
ax1.set_title('Velocity vs Time - Trapezoidal Rule Integration', fontsize=14, fontweight='bold')
ax1.set_xlabel('Time (s)', fontsize=12)
ax1.set_ylabel('Velocity (m/s)', fontsize=12)
ax1.grid(True, alpha=0.3)
ax1.axhline(y=0, color='k', linewidth=0.5)

# Plot the velocity line
ax1.plot(t, v, 'o-', color='darkblue', linewidth=2, markersize=8, label='Velocity Data')

# Fill trapezoids and calculate areas for visualization
for i in range(len(t) - 1):
    t1, t2 = t[i], t[i+1]
    v1, v2 = v[i], v[i+1]
    
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
ax2.plot(t, displacement_loop, 'o-', color='darkgreen', linewidth=2, markersize=8, label='Displacement')

# Fill area under displacement curve
ax2.fill_between(t, 0, displacement_loop, color='lightgreen', alpha=0.5, label='Accumulated Displacement')

# Add value labels on each point
for ti, di in zip(t, displacement_loop):
    ax2.text(ti, di + 0.8, f'{di:.0f}m', ha='center', va='bottom', fontsize=10, fontweight='bold')

# Mark the maximum displacement with a black circle
max_idx = displacement_loop.index(max(displacement_loop))
ax2.plot(t[max_idx], displacement_loop[max_idx], 'o', color='black', markersize=15, 
         label=f'Maximum: {max(displacement_loop):.0f}m', markerfacecolor='none', markeredgewidth=2)

ax2.legend(loc='upper right', fontsize=11)
ax2.set_xlim(-1, 17)
ax2.set_ylim(-2, 24)

# Adjust layout and display
plt.tight_layout()
plt.savefig('task_a_trapezoidal_rule_visualization.png', dpi=300, bbox_inches='tight')
print("Graph saved as 'task_a_trapezoidal_rule_visualization.png'")
plt.show()
