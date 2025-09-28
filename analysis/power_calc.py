"""
analysis/power_calc.py
Back-of-envelope power calculation for PLV effect sizes.
"""
import math

def required_n(effect_size=0.15, alpha=0.05, power=0.8):
    # Very rough: one-sample equivalence to Cohen's d→n using normal approx.
    # Replace with proper PLV variance model as data accumulates.
    from scipy.stats import norm
    z1 = norm.ppf(1-alpha/2)
    z2 = norm.ppf(power)
    n = 2*((z1+z2)/effect_size)**2
    return math.ceil(n)

if __name__ == "__main__":
    print("Rough n for PLV Δ=0.15:", required_n())
