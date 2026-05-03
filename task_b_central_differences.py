import matplotlib.pyplot as plt
import numpy as np

print("\n" + "="*100)
print("TASK B: CENTRAL DIFFERENCES - NUMERICAL DIFFERENTIATION")
print("="*100)

# ============ PART 1: PRELIMINARY HAND CALCULATIONS ============

print("\n" + "="*100)
print("PART 1: PRELIMINARY HAND CALCULATIONS")
print("="*100)

t = [0, 2, 6, 10]
d = [0, 2, 12, 6]

print("\nInput Data:")
print(f"t (Time array):         {t}")
print(f"d (Displacement array): {d}")

print("\n" + "-"*100)
print("MANUAL VELOCITY CALCULATIONS:")
print("-"*100)

print("\n1. FORWARD DIFFERENCE at t[0] (index 0)")
print("   No point before index 0, so use forward difference (index 0 to 1)")
print(f"   Formula: v[0] = (d[1] - d[0]) / (t[1] - t[0])")
print(f"   v[0] = ({d[1]} - {d[0]}) / ({t[1]} - {t[0]})")
print(f"   v[0] = {d[1] - d[0]} / {t[1] - t[0]}")
v_0 = (d[1] - d[0]) / (t[1] - t[0])
print(f"   v[0] = {v_0} m/s")

print("\n2. CENTRAL DIFFERENCE at t[1] (index 1)")
print("   Use points before and after (index 0 to 2)")
print(f"   Formula: v[1] = (d[2] - d[0]) / (t[2] - t[0])")
print(f"   v[1] = ({d[2]} - {d[0]}) / ({t[2]} - {t[0]})")
print(f"   v[1] = {d[2] - d[0]} / {t[2] - t[0]}")
v_1 = (d[2] - d[0]) / (t[2] - t[0])
print(f"   v[1] = {v_1} m/s")

print("\n3. CENTRAL DIFFERENCE at t[2] (index 2)")
print("   Use points before and after (index 1 to 3)")
print(f"   Formula: v[2] = (d[3] - d[1]) / (t[3] - t[1])")
print(f"   v[2] = ({d[3]} - {d[1]}) / ({t[3]} - {t[1]})")
print(f"   v[2] = {d[3] - d[1]} / {t[3] - t[1]}")
v_2 = (d[3] - d[1]) / (t[3] - t[1])
print(f"   v[2] = {v_2} m/s (= -3/2)")

print("\n4. BACKWARD DIFFERENCE at t[3] (index 3)")
print("   No point after index 3, so use backward difference (index 2 to 3)")
print(f"   Formula: v[3] = (d[3] - d[2]) / (t[3] - t[2])")
print(f"   v[3] = ({d[3]} - {d[2]}) / ({t[3]} - {t[2]})")
print(f"   v[3] = {d[3] - d[2]} / {t[3] - t[2]}")
v_3 = (d[3] - d[2]) / (t[3] - t[2])
print(f"   v[3] = {v_3} m/s (= -3/2)")

expected_velocity = [v_0, v_1, v_2, v_3]
print("\n" + "-"*100)
print(f"EXPECTED VELOCITY ARRAY: {expected_velocity}")
print(f"Expected (as fractions): [1, 2, -3/2, -3/2]")
print("-"*100)


# ============ PART 2: PYTHON FUNCTIONS ============

print("\n" + "="*100)
print("PART 2: PYTHON FUNCTIONS")
print("="*100)

def central_difference_loop(x, y):
    """
    Calculate numerical differentiation using Central Differences with loops.
    
    Parameters:
    -----------
    x : list or 1D array
        X-axis values (e.g., time)
    y : list or 1D array
        Y-axis values (e.g., displacement)
    
    Returns:
    --------
    velocity : list
        Derivative values at each x point (same size as x and y)
    """
    n = len(x)
    velocity = []
    
    for i in range(n):
        if i == 0:
            # Forward Difference at first point
            dy = y[1] - y[0]
            dx = x[1] - x[0]
            slope = dy / dx
        elif i == n - 1:
            # Backward Difference at last point
            dy = y[n-1] - y[n-2]
            dx = x[n-1] - x[n-2]
            slope = dy / dx
        else:
            # Central Difference at interior points
            dy = y[i+1] - y[i-1]
            dx = x[i+1] - x[i-1]
            slope = dy / dx
        
        velocity.append(slope)
    
    return velocity


def central_difference_numpy(x, y):
    """
    Calculate numerical differentiation using Central Differences with NumPy.
    
    Parameters:
    -----------
    x : array-like
        X-axis values (e.g., time)
    y : array-like
        Y-axis values (e.g., displacement)
    
    Returns:
    --------
    velocity : ndarray
        Derivative values at each x point (same size as x and y)
    """
    x = np.array(x, dtype=float)
    y = np.array(y, dtype=float)
    n = len(x)
    
    velocity = np.zeros(n)
    
    # Forward Difference at first point
    velocity[0] = (y[1] - y[0]) / (x[1] - x[0])
    
    # Central Difference at interior points
    for i in range(1, n-1):
        velocity[i] = (y[i+1] - y[i-1]) / (x[i+1] - x[i-1])
    
    # Backward Difference at last point
    velocity[n-1] = (y[n-1] - y[n-2]) / (x[n-1] - x[n-2])
    
    return velocity


# ============ PART 3: DESK CHECK VALIDATION ============

print("\n" + "="*100)
print("PART 3: DESK CHECK VALIDATION")
print("="*100)

print("\n" + "-"*100)
print("FUNCTION: central_difference_loop(x, y)")
print("-"*100)

print("\nINPUT PARAMETERS:")
print(f"  x = {t}")
print(f"  y = {d}")

print("\nINITIAL STATE:")
print(f"  n = len(x) = len({t}) = {len(t)}")
print(f"  velocity = []  (empty list)")
print(f"  Loop will execute: for i in range({len(t)}) = range(4) = [0, 1, 2, 3]")

print("\n" + "DETAILED STEP-BY-STEP EXECUTION:" + "-"*75)

print("\n[ITERATION i=0]")
print(f"  i = 0")
print(f"  Condition: i == 0? YES → Use FORWARD DIFFERENCE")
print(f"  x[1] = {t[1]}, x[0] = {t[0]}")
print(f"  y[1] = {d[1]}, y[0] = {d[0]}")
print(f"  dy = y[1] - y[0] = {d[1]} - {d[0]} = {d[1] - d[0]}")
print(f"  dx = x[1] - x[0] = {t[1]} - {t[0]} = {t[1] - t[0]}")
print(f"  slope = dy / dx = {d[1] - d[0]} / {t[1] - t[0]} = {(d[1] - d[0]) / (t[1] - t[0])}")
print(f"  velocity.append({(d[1] - d[0]) / (t[1] - t[0])})")
print(f"  velocity = [{(d[1] - d[0]) / (t[1] - t[0])}]")

print("\n[ITERATION i=1]")
print(f"  i = 1")
print(f"  Condition: i == 0? NO")
print(f"  Condition: i == n-1? i == 3? NO → Use CENTRAL DIFFERENCE")
print(f"  x[i+1] = x[2] = {t[2]}, x[i-1] = x[0] = {t[0]}")
print(f"  y[i+1] = y[2] = {d[2]}, y[i-1] = y[0] = {d[0]}")
print(f"  dy = y[i+1] - y[i-1] = {d[2]} - {d[0]} = {d[2] - d[0]}")
print(f"  dx = x[i+1] - x[i-1] = {t[2]} - {t[0]} = {t[2] - t[0]}")
print(f"  slope = dy / dx = {d[2] - d[0]} / {t[2] - t[0]} = {(d[2] - d[0]) / (t[2] - t[0])}")
print(f"  velocity.append({(d[2] - d[0]) / (t[2] - t[0])})")
print(f"  velocity = [{(d[1] - d[0]) / (t[1] - t[0])}, {(d[2] - d[0]) / (t[2] - t[0])}]")

print("\n[ITERATION i=2]")
print(f"  i = 2")
print(f"  Condition: i == 0? NO")
print(f"  Condition: i == n-1? i == 3? NO → Use CENTRAL DIFFERENCE")
print(f"  x[i+1] = x[3] = {t[3]}, x[i-1] = x[1] = {t[1]}")
print(f"  y[i+1] = y[3] = {d[3]}, y[i-1] = y[1] = {d[1]}")
print(f"  dy = y[i+1] - y[i-1] = {d[3]} - {d[1]} = {d[3] - d[1]}")
print(f"  dx = x[i+1] - x[i-1] = {t[3]} - {t[1]} = {t[3] - t[1]}")
print(f"  slope = dy / dx = {d[3] - d[1]} / {t[3] - t[1]} = {(d[3] - d[1]) / (t[3] - t[1])}")
print(f"  velocity.append({(d[3] - d[1]) / (t[3] - t[1])})")
print(f"  velocity = [{(d[1] - d[0]) / (t[1] - t[0])}, {(d[2] - d[0]) / (t[2] - t[0])}, {(d[3] - d[1]) / (t[3] - t[1])}]")

print("\n[ITERATION i=3]")
print(f"  i = 3")
print(f"  Condition: i == 0? NO")
print(f"  Condition: i == n-1? i == 3? YES → Use BACKWARD DIFFERENCE")
print(f"  n = {len(t)}")
print(f"  x[n-1] = x[3] = {t[3]}, x[n-2] = x[2] = {t[2]}")
print(f"  y[n-1] = y[3] = {d[3]}, y[n-2] = y[2] = {d[2]}")
print(f"  dy = y[n-1] - y[n-2] = {d[3]} - {d[2]} = {d[3] - d[2]}")
print(f"  dx = x[n-1] - x[n-2] = {t[3]} - {t[2]} = {t[3] - t[2]}")
print(f"  slope = dy / dx = {d[3] - d[2]} / {t[3] - t[2]} = {(d[3] - d[2]) / (t[3] - t[2])}")
print(f"  velocity.append({(d[3] - d[2]) / (t[3] - t[2])})")
print(f"  velocity = [{(d[1] - d[0]) / (t[1] - t[0])}, {(d[2] - d[0]) / (t[2] - t[0])}, {(d[3] - d[1]) / (t[3] - t[1])}, {(d[3] - d[2]) / (t[3] - t[2])}]")

print("\nLOOP ENDS (i = 4 is not in range(4))")

print("\nRETURN:")
print(f"  return velocity = [{(d[1] - d[0]) / (t[1] - t[0])}, {(d[2] - d[0]) / (t[2] - t[0])}, {(d[3] - d[1]) / (t[3] - t[1])}, {(d[3] - d[2]) / (t[3] - t[2])}]")

print("\n" + "-"*100)
print("TESTING LOOP-BASED FUNCTION")
print("-"*100)

velocity_loop = central_difference_loop(t, d)
print(f"\nResult: velocity_loop = {velocity_loop}")

print("\nTrace Table - Loop Function:")
print(f"{'i':<4} {'Type':<12} {'Formula':<50} {'dy':<8} {'dx':<8} {'slope':<10}")
print("-"*120)

for i in range(len(t)):
    if i == 0:
        dtype = "Forward"
        formula = f"(d[1]-d[0])/(t[1]-t[0]) = ({d[1]}-{d[0]})/({t[1]}-{t[0]})"
        dy = d[1] - d[0]
        dx = t[1] - t[0]
    elif i == len(t) - 1:
        dtype = "Backward"
        formula = f"(d[{i}]-d[{i-1}])/(t[{i}]-t[{i-1}]) = ({d[i]}-{d[i-1]})/({t[i]}-{t[i-1]})"
        dy = d[i] - d[i-1]
        dx = t[i] - t[i-1]
    else:
        dtype = "Central"
        formula = f"(d[{i+1}]-d[{i-1}])/(t[{i+1}]-t[{i-1}]) = ({d[i+1]}-{d[i-1]})/({t[i+1]}-{t[i-1]})"
        dy = d[i+1] - d[i-1]
        dx = t[i+1] - t[i-1]
    
    slope = dy / dx
    print(f"{i:<4} {dtype:<12} {formula:<50} {dy:<8} {dx:<8} {slope:<10.4f}")

print("\n" + "-"*100)
print("FUNCTION: central_difference_numpy(x, y)")
print("-"*100)

print("\nINPUT PARAMETERS:")
print(f"  x = {t}")
print(f"  y = {d}")

print("\nSTEP-BY-STEP EXECUTION:")

print("\nStep 1: Convert to NumPy arrays and get n")
print(f"  x = np.array({t}, dtype=float)")
print(f"  y = np.array({d}, dtype=float)")
print(f"  n = len(x) = {len(t)}")

print("\nStep 2: Create velocity array initialized with zeros")
print(f"  velocity = np.zeros({len(t)}) = {np.zeros(len(t)).tolist()}")

print("\nStep 3: FORWARD DIFFERENCE at velocity[0]")
print(f"  velocity[0] = (y[1] - y[0]) / (x[1] - x[0])")
print(f"              = ({d[1]} - {d[0]}) / ({t[1]} - {t[0]})")
print(f"              = {d[1] - d[0]} / {t[1] - t[0]}")
print(f"              = {(d[1] - d[0]) / (t[1] - t[0])}")
print(f"  velocity = [{(d[1] - d[0]) / (t[1] - t[0])}, 0.0, 0.0, 0.0]")

print("\nStep 4: CENTRAL DIFFERENCE at interior points (i = 1, 2)")
print(f"  Loop: for i in range(1, {len(t)}-1) = range(1, 3) = [1, 2]")

print(f"\n  [ITERATION i=1]")
print(f"    velocity[1] = (y[2] - y[0]) / (x[2] - x[0])")
print(f"               = ({d[2]} - {d[0]}) / ({t[2]} - {t[0]})")
print(f"               = {d[2] - d[0]} / {t[2] - t[0]}")
print(f"               = {(d[2] - d[0]) / (t[2] - t[0])}")
print(f"    velocity = [{(d[1] - d[0]) / (t[1] - t[0])}, {(d[2] - d[0]) / (t[2] - t[0])}, 0.0, 0.0]")

print(f"\n  [ITERATION i=2]")
print(f"    velocity[2] = (y[3] - y[1]) / (x[3] - x[1])")
print(f"               = ({d[3]} - {d[1]}) / ({t[3]} - {t[1]})")
print(f"               = {d[3] - d[1]} / {t[3] - t[1]}")
print(f"               = {(d[3] - d[1]) / (t[3] - t[1])}")
print(f"    velocity = [{(d[1] - d[0]) / (t[1] - t[0])}, {(d[2] - d[0]) / (t[2] - t[0])}, {(d[3] - d[1]) / (t[3] - t[1])}, 0.0]")

print("\nStep 5: BACKWARD DIFFERENCE at velocity[n-1]")
print(f"  n-1 = {len(t)-1}")
print(f"  velocity[{len(t)-1}] = (y[{len(t)-1}] - y[{len(t)-2}]) / (x[{len(t)-1}] - x[{len(t)-2}])")
print(f"                 = ({d[3]} - {d[2]}) / ({t[3]} - {t[2]})")
print(f"                 = {d[3] - d[2]} / {t[3] - t[2]}")
print(f"                 = {(d[3] - d[2]) / (t[3] - t[2])}")
print(f"  velocity = [{(d[1] - d[0]) / (t[1] - t[0])}, {(d[2] - d[0]) / (t[2] - t[0])}, {(d[3] - d[1]) / (t[3] - t[1])}, {(d[3] - d[2]) / (t[3] - t[2])}]")

print("\nRETURN:")
print(f"  return velocity = {expected_velocity}")

print("\n" + "-"*100)
print("TESTING NUMPY-BASED FUNCTION")
print("-"*100)

velocity_numpy = central_difference_numpy(t, d)
print(f"\nResult: velocity_numpy = {velocity_numpy.tolist()}")

print("\n" + "-"*100)
print("COMPARISON: Expected vs Loop vs NumPy")
print("-"*100)
print(f"{'Index':<8} {'t[i]':<8} {'Expected':<15} {'Loop':<15} {'NumPy':<15} {'Match?':<10}")
print("-"*100)

all_match = True
for i in range(len(expected_velocity)):
    loop_val = velocity_loop[i]
    numpy_val = velocity_numpy[i]
    expected_val = expected_velocity[i]
    
    match_loop = abs(loop_val - expected_val) < 1e-10
    match_numpy = abs(numpy_val - expected_val) < 1e-10
    match_all = match_loop and match_numpy
    
    if not match_all:
        all_match = False
    
    match_str = "✓" if match_all else "✗"
    print(f"{i:<8} {t[i]:<8} {expected_val:<15.4f} {loop_val:<15.4f} {numpy_val:<15.4f} {match_str:<10}")

print("-"*100)
if all_match:
    print("✓ SUCCESS: All values match perfectly!")
else:
    print("✗ ERROR: Values do not match. Logic needs to be fixed.")

print("\n" + "="*100)
print("SUMMARY:")
print("="*100)
print(f"Velocity Array (Loop):    {[f'{v:.4f}' for v in velocity_loop]}")
print(f"Velocity Array (NumPy):   {[f'{v:.4f}' for v in velocity_numpy]}")
print(f"Expected Velocity Array:  {[f'{v:.4f}' for v in expected_velocity]}")
print("="*100 + "\n")


# ============ VISUALIZATION ============

print("Generating visualization graphs...")

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))

# ============ GRAPH 1: Displacement vs Time with Secant Lines ============
ax1.set_title('Displacement vs Time - Central Differences (Secant Lines)', fontsize=14, fontweight='bold')
ax1.set_xlabel('Time (s)', fontsize=12)
ax1.set_ylabel('Displacement (m)', fontsize=12)
ax1.grid(True, alpha=0.3)

# Plot displacement points
ax1.plot(t, d, 'o-', color='darkblue', linewidth=2, markersize=10, label='Displacement Data', zorder=3)

# Draw secant lines and mark slopes
colors = ['red', 'green', 'orange', 'purple']

for i in range(len(t)):
    if i == 0:
        # Forward Difference: line from point 0 to point 1
        t1, t2 = t[0], t[1]
        d1, d2 = d[0], d[1]
        ax1.plot([t1, t2], [d1, d2], '--', color=colors[i], linewidth=2, alpha=0.7, label=f'Forward Diff (i=0)')
        # Mark slope at point 0
        ax1.annotate(f'v[0]={velocity_loop[0]:.2f}', xy=(t1, d1), xytext=(t1-0.5, d1-1.5),
                    fontsize=10, fontweight='bold', color=colors[i],
                    bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.7))
    
    elif i == len(t) - 1:
        # Backward Difference: line from point n-2 to point n-1
        t1, t2 = t[i-1], t[i]
        d1, d2 = d[i-1], d[i]
        ax1.plot([t1, t2], [d1, d2], '--', color=colors[i], linewidth=2, alpha=0.7, label=f'Backward Diff (i={i})')
        # Mark slope at last point
        ax1.annotate(f'v[{i}]={velocity_loop[i]:.2f}', xy=(t2, d2), xytext=(t2-0.5, d2+1.5),
                    fontsize=10, fontweight='bold', color=colors[i],
                    bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.7))
    
    else:
        # Central Difference: line from point i-1 to point i+1
        t1, t2 = t[i-1], t[i+1]
        d1, d2 = d[i-1], d[i+1]
        ax1.plot([t1, t2], [d1, d2], '--', color=colors[i], linewidth=2, alpha=0.7, label=f'Central Diff (i={i})')
        # Mark slope at point i
        ax1.annotate(f'v[{i}]={velocity_loop[i]:.2f}', xy=(t[i], d[i]), xytext=(t[i]-0.5, d[i]+1.5),
                    fontsize=10, fontweight='bold', color=colors[i],
                    bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.7))

ax1.legend(loc='upper left', fontsize=10)
ax1.set_xlim(-1, 11)
ax1.set_ylim(-2, 15)

# ============ GRAPH 2: Velocity vs Time ============
ax2.set_title('Velocity vs Time - Numerical Differentiation Results', fontsize=14, fontweight='bold')
ax2.set_xlabel('Time (s)', fontsize=12)
ax2.set_ylabel('Velocity (m/s)', fontsize=12)
ax2.grid(True, alpha=0.3)
ax2.axhline(y=0, color='k', linewidth=0.5)

# Plot velocity from loop function
ax2.plot(t, velocity_loop, 'o-', color='darkgreen', linewidth=2, markersize=10, label='Velocity (Loop Function)')

# Add value labels on each point
for ti, vi in zip(t, velocity_loop):
    ax2.text(ti, vi + 0.2, f'{vi:.2f}', ha='center', va='bottom', fontsize=10, fontweight='bold')

# Mark the methods used
ax2.plot(t[0], velocity_loop[0], 's', color='red', markersize=12, label='Forward Diff (First Point)', markerfacecolor='none', markeredgewidth=2)
ax2.plot(t[1:-1], velocity_loop[1:-1], '^', color='orange', markersize=12, label='Central Diff (Interior Points)', markerfacecolor='none', markeredgewidth=2)
ax2.plot(t[-1], velocity_loop[-1], 'd', color='purple', markersize=12, label='Backward Diff (Last Point)', markerfacecolor='none', markeredgewidth=2)

ax2.legend(loc='upper right', fontsize=10)
ax2.set_xlim(-1, 11)
ax2.set_ylim(-4, 3)

plt.tight_layout()
plt.savefig('task_b_central_differences_visualization.png', dpi=300, bbox_inches='tight')
print("Graph saved as 'task_b_central_differences_visualization.png'")
plt.show()
