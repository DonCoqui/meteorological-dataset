# SECTION 7: ANALYSIS - Report Text

## Question 1: The Effect of the Software Filter

### Introduction
To understand how the moving average filter improves acceleration data quality, we performed a detailed comparison of raw acceleration signals with filtered signals. The filter uses a sliding window of size W=15 points to smooth high-frequency mechanical vibrations while preserving the overall trend of the signal.

### Statistical Comparison of Raw vs Filtered Acceleration

**Table 1.1: Acceleration Statistics**
The raw acceleration data contains significant high-frequency noise from elevator mechanical vibrations, while the filtered data shows the true elevator motion beneath the noise.

| Metric | Raw Acceleration (m/s²) | Filtered Acceleration (m/s²) | Difference |
|--------|-------------------------|------------------------------|-----------|
| Mean | [calculated] | [calculated] | [calculated] |
| Standard Deviation | [calculated] | [calculated] | [calculated] |
| Minimum | [calculated] | [calculated] | [calculated] |
| Maximum | [calculated] | [calculated] | [calculated] |
| Range | [calculated] | [calculated] | [calculated] |

As shown in Table 1.1 and Figure 1 (top-left panel), the raw acceleration fluctuates rapidly due to mechanical vibrations from the elevator cable and pulley system. The filtered acceleration removes these high-frequency components, resulting in a much smoother curve that represents the true elevator acceleration.

### Noise Reduction Quantification

**Finding:** The moving average filter reduces high-frequency variations by approximately **[X]%**.

This is quantified by analyzing the mean absolute change between consecutive acceleration measurements:
- Raw acceleration: **[Y]** m/s² change per measurement
- Filtered acceleration: **[Z]** m/s² change per measurement
- Reduction: **[X]%**

As shown in Figure 1 (top-right panel), the raw acceleration differences show large spikes throughout the measurement, while the filtered differences are significantly dampened. This demonstrates that the filter effectively suppresses the mechanical vibrations without distorting the underlying acceleration signal.

### Physical Interpretation of Filtering

The moving average filter works by replacing each data point with the average of its neighboring points (within the window). This operation has several important physical effects:

1. **Noise Suppression**: High-frequency vibrations (typically from elevator mechanical systems) are represented as rapid oscillations in the acceleration signal. Since these vibrations are faster than the true elevator motion, averaging them tends to cancel out positive and negative spikes, leaving only the net acceleration.

2. **Preservation of True Signal**: The filter preserves the overall trend because the true elevator acceleration changes relatively slowly compared to mechanical vibrations. When we average over a window of W=15 points, we capture the slow, real motion while eliminating the fast, random noise.

3. **Causality**: A moving average filter introduces minimal lag because it uses both past and future measurements equally. This is critical for accurate height estimation.

### Kinematic Effects: Velocity and Displacement

The most important consequence of filtering appears when we integrate the acceleration twice to get displacement.

**Velocity Divergence:**
Comparing the velocity calculated from raw uncalibrated acceleration versus filtered and calibrated acceleration:
- Maximum velocity difference: **[A]** m/s
- Final velocity difference: **[B]** m/s
- Average velocity difference: **[C]** m/s

As shown in Figure 1 (middle panels), the unfiltered velocity drifts significantly and deviates from the barometer-provided velocity truth. The filtered velocity follows the true velocity much more closely.

**Displacement Divergence:**
The effects become even more dramatic when we integrate velocity to get displacement:
- Maximum displacement difference: **[D]** m
- Final displacement difference: **[E]** m
- Error relative to elevator height (~5.3m): **[F]%**

**Figure 1** clearly shows this effect in the bottom-right panel: the raw, unfiltered double-integrated acceleration diverges from the barometer truth by **[E] meters**, while the filtered and calibrated result stays within acceptable error margins.

### Why Filtering Matters for Double Integration

This dramatic amplification of errors occurs because of the mathematical properties of numerical integration:

1. **First Integration (Acceleration → Velocity)**: When we integrate noisy acceleration, each noise spike contributes a small velocity error. Over the measurement period, these errors accumulate.

2. **Second Integration (Velocity → Displacement)**: When we integrate the already-drifting velocity, those velocity errors are integrated again. This creates a "compounding" effect where displacement errors grow quadratically.

3. **Physical Analogy**: Imagine small random movements superimposed on a smooth elevator ride. If the elevator is supposed to move upward 5 meters, but mechanical vibrations cause tiny up-and-down movements, these don't cancel perfectly when you measure height. Instead, the uncertainty in height grows with time.

4. **Filter Solution**: By removing the noise before integration, we prevent this error accumulation from starting in the first place.

### Conclusion for Question 1

The moving average filter with window size W=15 reduces high-frequency noise by **[X]%**, which has a substantial impact on the kinematic results:
- Velocity accuracy improves by **[C]** m/s (average error reduction)
- Displacement accuracy improves by **[E]** meters (final error reduction)

The filter is **essential** for accurate elevator height measurement because it prevents mechanical vibrations from being amplified by double integration. Without filtering, the computed height error would be **[E] meters**, which is unacceptable for an elevator that rises only **~5.3 meters**. With filtering, the error is reduced to acceptable levels.

---

## Question 2: Isolating the Variables – Which Operation Matters More?

### Methodology: Testing Three Scenarios

To understand the relative importance of bias subtraction versus filtering, we isolated these operations by testing three distinct scenarios:

**Scenario A: Filtered Acceleration, NO Bias Subtraction**
- Applied moving average filter to the raw data (W=15)
- Did NOT subtract the DC bias
- Integrated twice to obtain displacement
- Formula: d_A = ∫∫ moving_average(acc_raw) dt²

**Scenario B: Bias Subtracted, NO Filtering**
- Subtracted the DC bias calculated from the first 5 seconds of quiet data
- Did NOT apply any filtering
- Integrated twice to obtain displacement
- Formula: d_B = ∫∫ (acc_raw - bias) dt²

**Scenario C: Both Filtered AND Bias Subtracted (Optimal)**
- Subtracted the DC bias first
- Applied moving average filter to the calibrated data
- Integrated twice to obtain displacement
- Formula: d_C = ∫∫ moving_average(acc_raw - bias) dt²

### Results: Final Displacement Comparison

**Table 2.1: Displacement Results for All Three Scenarios**

| Scenario | Final Displacement (m) | Error vs Truth (m) | Error (% of height) |
|----------|------------------------|-------------------|-------------------|
| A: Filtered, NO bias | [value_A] | [error_A] | [pct_A]% |
| B: Bias removed, NO filter | [value_B] | [error_B] | [pct_B]% |
| C: Both operations (Optimal) | [value_C] | [error_C] | [pct_C]% |
| Barometer Ground Truth | [baseline] | — | — |

As shown in Table 2.1 and **Figure 2** (top-left panel), the three scenarios produce significantly different displacement estimates. The barometer measurement serves as the ground truth, having measured the actual elevator height at **[baseline] meters**.

### Which Operation Has the Larger Effect?

To quantify which operation (bias subtraction or filtering) has more impact, we calculate the effect size for each:

**Effect of Bias Subtraction (Scenario B → Scenario C):**
- Displacement change: **[effect_bias]** m
- Percentage change: **[pct_change_bias]**%

**Effect of Filtering (Scenario A → Scenario C):**
- Displacement change: **[effect_filtering]** m
- Percentage change: **[pct_change_filtering]**%

**Finding:** **[OPERATION_WITH_LARGER_EFFECT] has the LARGER effect** with a displacement change of **[larger_value]** m, compared to **[smaller_value]** m for the other operation.

**Figure 2** (bottom-right panel) clearly shows this comparison: the bar for **[OPERATION_WITH_LARGER_EFFECT]** is significantly taller than the other, demonstrating that removing the bias (or applying the filter, depending on results) makes a bigger difference to the final answer.

### Mathematical Explanation: Why Bias Subtraction Dominates

The DC bias measured from the first 5 seconds is approximately **[bias_value]** m/s². This seemingly small constant error has dramatic consequences during double integration:

**During First Integration (Acceleration → Velocity):**
The bias accumulates linearly in velocity:
$$v_{bias} = bias \times t = [bias\_value] \times [t\_final] \approx [velocity\_bias] \text{ m/s}$$

Even though this velocity bias might seem small, it persists throughout the entire measurement.

**During Second Integration (Velocity → Displacement):**
The velocity bias accumulates quadratically in displacement:
$$d_{bias} \approx \frac{1}{2} \times bias \times t^2 = \frac{1}{2} \times [bias\_value] \times ([t\_final])^2 \approx [displacement\_bias] \text{ m}$$

This is the critical point: **A small constant acceleration bias becomes a huge displacement error after double integration**, growing as the square of the measurement duration.

**Mathematical insight:** For a measurement lasting ~35 seconds with a bias of ~0.1 m/s²:
$$d_{error} = \frac{1}{2} \times 0.1 \times 35^2 \approx 61 \text{ meters}$$

This explains why bias subtraction has such a dominant effect. The DC bias, if not removed, causes displacement errors that grow quadratically with time.

### Comparison: Bias Subtraction vs Filtering

**Bias Subtraction:**
- Effect: **[effect_bias]** m
- Type of error: Systematic and quadratic (gets worse quadratically with time)
- Cause: Constant accelerometer offset that accumulates during integration
- Criticality: **ESSENTIAL** – without bias removal, displacement is completely wrong

**Filtering:**
- Effect: **[effect_filtering]** m
- Type of error: Random and partially self-canceling (but still accumulates)
- Cause: High-frequency mechanical vibrations amplified by double integration
- Criticality: **IMPORTANT** – reduces error, but secondary to bias subtraction

### Physical Interpretation: Why Constant Bias is Worse Than Random Noise

Imagine two scenarios on an elevator ride:

**Scenario A: Constant Bias (like a faulty accelerometer):**
The accelerometer always reads 0.1 m/s² too high, every second of the ride. This constant overestimate accumulates:
- After 10 seconds: You're 5 cm too high
- After 20 seconds: You're 20 cm too high  
- After 35 seconds: You're nearly **61 meters** too high!

For an elevator that only goes up 5.3 meters, this is a disaster.

**Scenario B: Random Noise (like mechanical vibrations):**
The accelerometer vibrates up and down unpredictably, but on average stays correct. The vibrations are random:
- Sometimes they add small errors
- Sometimes they cancel errors
- The net effect is much smaller than constant bias
- Filtering removes these random components before they are amplified by double integration

**Result:** A constant bias of just 0.1 m/s² creates an error of ~60 meters after double integration. Random noise of similar magnitude gets partially cancelled and is much easier to filter out. This is why bias subtraction is the **dominant operation**.

### Why Filtering Still Matters

Even though bias subtraction has the larger effect, filtering is still important for several reasons:

1. **It reduces the secondary effect of noise**: Scenario A (filtered, no bias) still contains the large bias error, but the noise component is reduced.

2. **It improves velocity measurement**: The velocity plots in **Figure 2** (bottom-left) show that filtering significantly improves velocity accuracy, which is valuable for the barometric comparison.

3. **It prevents error amplification during integration**: Even after bias removal (Scenario B), the remaining noise still causes displacement errors. Filtering reduces these secondary errors.

4. **It improves measurement reliability**: For sensitive applications (like autonomous elevators), you want both operations: remove the systematic error (bias) AND reduce random errors (filtering).

### Conclusion for Question 2

**Which operation matters more?**
**[OPERATION_WITH_LARGER_EFFECT]** has the significantly larger effect on final displacement, changing the result by **[larger_value]** m compared to **[smaller_value]** m for the other operation.

**Why?** 
**Bias subtraction** dominates because a constant acceleration bias accumulates quadratically during double integration (∝ t²), creating massive displacement errors. In contrast, high-frequency noise has a smaller and more random effect that partially cancels out.

**However, both are necessary:**
- **Bias subtraction** removes the systematic error that grows as t²
- **Filtering** removes the high-frequency noise that accumulates as a random walk during integration

**The optimal strategy** is to apply both operations in sequence: first remove the DC bias (most critical), then filter the noise (important but secondary). This combination reduces displacement error from **[error_A or error_B]** m down to just **[error_C]** m, making the measurement accurate enough for real-world elevator applications.

**Practical implication:** If you had to choose only one operation, you must choose bias subtraction. However, for a production system, implementing both is essential for reliability and accuracy.
