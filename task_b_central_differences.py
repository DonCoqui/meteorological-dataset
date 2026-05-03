import matplotlib.pyplot as plt
import numpy as np

print("\n" + "="*80)
print("TASK B: CENTRAL DIFFERENCES - NUMERICAL DIFFERENTIATION")
print("="*80)

# ============ PART 1: PRELIMINARY HAND CALCULATIONS ============

print("\n" + "="*80)
print("PART 1: PRELIMINARY HAND CALCULATIONS")
print("="*80)

time = [0, 2, 6, 10]
displacement = [0, 2, 12, 6]

print("\nInput Data:")
print(f"Time (s):         {time}")
print(f"Displacement (m): {displacement}")

print("\n" + "-"*80)
print("HAND CALCULATIONS:")
print("-"*80)

print("\n1. FORWARD DIFFERENCE at t=0 (index 0)")
print("   Formula: v[0] = (d[1] - d[0]) / (t[1] - t[0])")
fd_0 = (displacement[1] - displacement[0]) / (time[1] - time[0])
print(f"   v[0] = ({displacement[1]} - {displacement[0]}) / ({time[1]} - {time[0]})")
print(f"   v[0] = {displacement[1] - displacement[0]} / {time[1] - time[0]}")
print(f"   v[0] = {fd_0} m/s")

print("\n2. CENTRAL DIFFERENCE at t=2 (index 1)")
print("   Formula: v[1] = (d[2] - d[0]) / (t[2] - t[0])")
cd_1 = (displacement[2] - displacement[0]) / (time[2] - time[0])
print(f"   v[1] = ({displacement[2]} - {displacement[0]}) / ({time[2]} - {time[0]})")
print(f"   v[1] = {displacement[2] - displacement[0]} / {time[2] - time[0]}")
print(f"   v[1] = {cd_1} m/s")

print("\n3. CENTRAL DIFFERENCE at t=6 (index 2)")
print("   Formula: v[2] = (d[3] - d[1]) / (t[3] - t[1])")
cd_2 = (displacement[3] - displacement[1]) / (time[3] - time[1])
print(f"   v[2] = ({displacement[3]} - {displacement[1]}) / ({time[3]} - {time[1]})")
print(f"   v[2] = {displacement[3] - displacement[1]} / {time[3] - time[1]}")
print(f"   v[2] = {cd_2} m/s (or {cd_2} = -3/2)")

print("\n4. BACKWARD DIFFERENCE at t=10 (index 3)")
print("   Formula: v[3] = (d[3] - d[2]) / (t[3] - t[2])")
bd_3 = (displacement[3] - displacement[2]) / (time[3] - time[2])
print(f"   v[3] = ({displacement[3]} - {displacement[2]}) / ({time[3]} - {time[2]})")
print(f"   v[3] = {displacement[3] - displacement[2]} / {time[3] - time[2]}")
print(f"   v[3] = {bd_3} m/s")

expected_velocity = [fd_0, cd_1, cd_2, bd_3]
print("\n" + "-"*80)
print(f"EXPECTED VELOCITY ARRAY: {expected_velocity}")
print(f"Expected (as fractions): [1, 2, -3/2, -3/2]")
print("-"*80)


# ============ PART 2: PYTHON FUNCTIONS ============

print("\n" + "="*80)
print("PART 2: PYTHON FUNCTIONS")
print("="*80)

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

print("\n" + "="*80)
print("PART 3: DESK CHECK VALIDATION")
print("="*80)

print("\n" + "-"*80)
print("TESTING LOOP-BASED FUNCTION: central_difference_loop()")
print("-"*80)

velocity_loop = central_difference_loop(time, displacement)
print(f"\nResult: {velocity_loop}")

print("\nDetailed Trace Table (Loop Function):")
print(f"{'i':<4} {'Type':<12} {'Formula':<40} {'Velocity':<10}")
print("-"*80)

for i in range(len(time)):
    if i == 0:
        dtype = "Forward"
        formula = f"(d[1]-d[0])/(t[1]-t[0]) = ({displacement[1]}-{displacement[0]})/({time[1]}-{time[0]})"
    elif i == len(time) - 1:
        dtype = "Backward"
        formula = f"(d[{i}]-d[{i-1}])/(t[{i}]-t[{i-1}]) = ({displacement[i]}-{displacement[i-1]})/({time[i]}-{time[i-1]})"
    else:
        dtype = "Central"
        formula = f"(d[{i+1}]-d[{i-1}])/(t[{i+1}]-t[{i-1}]) = ({displacement[i+1]}-{displacement[i-1]})/({time[i+1]}-{time[i-1]})"
    
    print(f"{i:<4} {dtype:<12} {formula:<40} {velocity_loop[i]:<10.4f}")

print("\n" + "-"*80)
print("TESTING NUMPY-BASED FUNCTION: central_difference_numpy()")
print("-"*80)

velocity_numpy = central_difference_numpy(time, displacement)
print(f"\nResult: {velocity_numpy.tolist()}")

print("\nDetailed Trace Table (NumPy Function):")
print(f"{'i':<4} {'Type':<12} {'Formula':<40} {'Velocity':<10}")
print("-"*80)

for i in range(len(time)):
    if i == 0:
        dtype = "Forward"
        formula = f"(d[1]-d[0])/(t[1]-t[0]) = ({displacement[1]}-{displacement[0]})/({time[1]}-{time[0]})"
    elif i == len(time) - 1:
        dtype = "Backward"
        formula = f"(d[{i}]-d[{i-1}])/(t[{i}]-t[{i-1}]) = ({displacement[i]}-{displacement[i-1]})/({time[i]}-{time[i-1]})"
    else:
        dtype = "Central"
        formula = f"(d[{i+1}]-d[{i-1}])/(t[{i+1}]-t[{i-1}]) = ({displacement[i+1]}-{displacement[i-1]})/({time[i+1]}-{time[i-1]})"
    
    print(f"{i:<4} {dtype:<12} {formula:<40} {velocity_numpy[i]:<10.4f}")

print("\n" + "-"*80)
print("COMPARISON: Expected vs Loop vs NumPy")
print("-"*80)
print(f"{'Index':<8} {'Time (s)':<12} {'Expected':<12} {'Loop':<12} {'NumPy':<12} {'Match?':<10}")
print("-"*80)

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
    print(f"{i:<8} {time[i]:<12} {expected_val:<12.4f} {loop_val:<12.4f} {numpy_val:<12.4f} {match_str:<10}")

print("-"*80)
if all_match:
    print("✓ SUCCESS: All values match perfectly!")
else:
    print("✗ ERROR: Values do not match. Logic needs to be fixed.")

print("\n" + "="*80)
print("SUMMARY:")
print("="*80)
print(f"Velocity Array (Loop):    {[f'{v:.4f}' for v in velocity_loop]}")
print(f"Velocity Array (NumPy):   {[f'{v:.4f}' for v in velocity_numpy]}")
print(f"Expected Velocity Array:  {[f'{v:.4f}' for v in expected_velocity]}")
print("="*80 + "\n")


# ============ VISUALIZATION ============

print("Generating visualization graphs...")

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))

# ============ GRAPH 1: Displacement vs Time with Secant Lines ============
ax1.set_title('Displacement vs Time - Central Differences (Secant Lines)', fontsize=14, fontweight='bold')
ax1.set_xlabel('Time (s)', fontsize=12)
ax1.set_ylabel('Displacement (m)', fontsize=12)
ax1.grid(True, alpha=0.3)

# Plot displacement points
ax1.plot(time, displacement, 'o-', color='darkblue', linewidth=2, markersize=10, label='Displacement Data', zorder=3)

# Draw secant lines and mark slopes
colors = ['red', 'green', 'orange', 'purple']

for i in range(len(time)):
    if i == 0:
        # Forward Difference: line from point 0 to point 1
        t1, t2 = time[0], time[1]
        d1, d2 = displacement[0], displacement[1]
        ax1.plot([t1, t2], [d1, d2], '--', color=colors[i], linewidth=2, alpha=0.7, label=f'Forward Diff (i=0)')
        # Mark slope at point 0
        ax1.annotate(f'v[0]={velocity_loop[0]:.2f}', xy=(t1, d1), xytext=(t1-0.5, d1-1.5),
                    fontsize=10, fontweight='bold', color=colors[i],
                    bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.7))
    
    elif i == len(time) - 1:
        # Backward Difference: line from point n-2 to point n-1
        t1, t2 = time[i-1], time[i]
        d1, d2 = displacement[i-1], displacement[i]
        ax1.plot([t1, t2], [d1, d2], '--', color=colors[i], linewidth=2, alpha=0.7, label=f'Backward Diff (i={i})')
        # Mark slope at last point
        ax1.annotate(f'v[{i}]={velocity_loop[i]:.2f}', xy=(t2, d2), xytext=(t2-0.5, d2+1.5),
                    fontsize=10, fontweight='bold', color=colors[i],
                    bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.7))
    
    else:
        # Central Difference: line from point i-1 to point i+1
        t1, t2 = time[i-1], time[i+1]
        d1, d2 = displacement[i-1], displacement[i+1]
        ax1.plot([t1, t2], [d1, d2], '--', color=colors[i], linewidth=2, alpha=0.7, label=f'Central Diff (i={i})')
        # Mark slope at point i
        ax1.annotate(f'v[{i}]={velocity_loop[i]:.2f}', xy=(time[i], displacement[i]), xytext=(time[i]-0.5, displacement[i]+1.5),
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
ax2.plot(time, velocity_loop, 'o-', color='darkgreen', linewidth=2, markersize=10, label='Velocity (Loop Function)')

# Add value labels on each point
for t, v in zip(time, velocity_loop):
    ax2.text(t, v + 0.2, f'{v:.2f}', ha='center', va='bottom', fontsize=10, fontweight='bold')

# Mark the methods used
ax2.plot(time[0], velocity_loop[0], 's', color='red', markersize=12, label='Forward Diff (First Point)', markerfacecolor='none', markeredgewidth=2)
ax2.plot(time[1:-1], velocity_loop[1:-1], '^', color='orange', markersize=12, label='Central Diff (Interior Points)', markerfacecolor='none', markeredgewidth=2)
ax2.plot(time[-1], velocity_loop[-1], 'd', color='purple', markersize=12, label='Backward Diff (Last Point)', markerfacecolor='none', markeredgewidth=2)

ax2.legend(loc='upper right', fontsize=10)
ax2.set_xlim(-1, 11)
ax2.set_ylim(-4, 3)

plt.tight_layout()
plt.savefig('central_differences_visualization.png', dpi=300, bbox_inches='tight')
print("Graph saved as 'central_differences_visualization.png'")
plt.show()
