import matplotlib.pyplot as plt
import numpy as np

# Toy data from the Trapezoidal Rule project
time = [0, 2, 4, 8, 12, 16]
velocity = [0, 4, 3, 0, -4, -2]
displacement = [3, 7, 14, 20, 12, 0]

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
ax2.plot(time, displacement, 'o-', color='darkgreen', linewidth=2, markersize=8, label='Displacement')

# Fill area under displacement curve
ax2.fill_between(time, 0, displacement, color='lightgreen', alpha=0.5, label='Accumulated Displacement')

# Add value labels on each point
for t, d in zip(time, displacement):
    ax2.text(t, d + 0.8, f'{d}m', ha='center', va='bottom', fontsize=10, fontweight='bold')

# Mark the maximum displacement
max_idx = displacement.index(max(displacement))
ax2.plot(time[max_idx], displacement[max_idx], 'r*', markersize=20, label=f'Maximum: {max(displacement)}m')

ax2.legend(loc='upper right', fontsize=11)
ax2.set_xlim(-1, 17)
ax2.set_ylim(-2, 24)

# Adjust layout and display
plt.tight_layout()
plt.savefig('trapezoidal_rule_visualization.png', dpi=300, bbox_inches='tight')
print("Graph saved as 'trapezoidal_rule_visualization.png'")
plt.show()

# Print summary
print("\n" + "="*60)
print("TRAPEZOIDAL RULE INTEGRATION SUMMARY")
print("="*60)
print(f"Initial Displacement: {displacement[0]} m")
print(f"Final Displacement: {displacement[-1]} m")
print(f"Maximum Displacement: {max(displacement)} m at t = {time[displacement.index(max(displacement))]} s")
print(f"\nDisplacement Array: {displacement}")
print("="*60)
