from scipy.integrate import odeint
import numpy as np
import math
import matplotlib.pyplot as plt

np.set_printoptions(legacy="1.25", precision=8, suppress=True)  # Set precision for NumPy output

# Initial concentration (mol/L) = ic
ic_a = 5
ic_b = 3
ic_c = 0
ic_d = 3
ic_e = 0
ic_f = 0

# Operating condition (temperature in K, pressure in Pa)
temp = 373.15 
press = 10 * 10**5

# Boltzmann constant (R)
r_const = 0.008314

# Molar flow = L/Mole Min
mf_a = 0.4
mf_b = 0.15
mf_c = 0.9

# Activation energy (kJ/mole)
ea_f_rx = 5
ea_s_rx = 10
ea_t_rx = 12

# Initiate equilibrium constant and rate constant
eq_const = 1.5
k1f = mf_a * math.exp(-(ea_f_rx) / (r_const * temp))
k1r = k1f / eq_const
k2f = mf_b * math.exp(-(ea_s_rx) / (r_const * temp)) 
k2r = k2f / eq_const
k3r = mf_c * math.exp(-(ea_t_rx) / (r_const * temp))
k3f = k3r * eq_const

# Initiate initial concentration array
initial_concentration = [ic_a, ic_b, ic_c, ic_d, ic_e, ic_f]

t_zero = 0 # Initial time (minute)
t_arr = np.linspace(0, 180, 101) # Time array (minute)

def concentration_over_time(concentration, time):
    A, B, C, D, E, F = concentration

    # Reaction rates
    r1 = k1f * A**2 * B - k1r * C
    r2 = k2f * C * D - k2r * E**3
    r3 = k3f * E * A - k3r * F**4

    # Differential equations
    dA_dt = -2 * r1 + r3
    dB_dt = -r1
    dC_dt = r1 - r2
    dD_dt = -r2
    dE_dt = 3 * r2 - r3
    dF_dt = r3

    return [dA_dt, dB_dt, dC_dt, dD_dt, dE_dt, dF_dt]

conc_prof = odeint(concentration_over_time, initial_concentration, t_arr)

plt.plot(t_arr, conc_prof[:, 0], label='Ca')
plt.plot(t_arr, conc_prof[:, 1], label='Cb')
plt.plot(t_arr, conc_prof[:, 2], label='Cc')
plt.plot(t_arr, conc_prof[:, 3], label='Cd')
plt.plot(t_arr, conc_prof[:, 4], label='Ce')
plt.plot(t_arr, conc_prof[:, 5], label='Cf')

plt.legend(loc='best')
plt.xlabel('t (minute)')
plt.ylabel('C (mol/L)')
plt.show()
