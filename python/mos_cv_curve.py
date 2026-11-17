import numpy as np
import matplotlib.pyplot as plt
# --- 1. Physical Constants & Parameters ---
q = 1.602e-19         # Electron charge (C)
eps0 = 8.854e-14      # Permittivity of vacuum (F/cm)
eps_si = 11.7 * eps0  # Permittivity of Silicon
eps_ox = 3.9 * eps0   # Permittivity of SiO2
k = 1.38e-23          # Boltzmann constant (J/K)
T = 300               # Temperature (K)
ni = 1.5e10           # Intrinsic carrier conc. (cm^-3)
Vt = (k * T) / q      # Thermal voltage (approx 0.0259V)
# --- 2. User Specified Inputs ---
rho = 0.32            # Resistivity (ohm-cm)
mu_p = 400            # Specified Hole Mobility (cm^2/V-s)
tox = 50e-7           # Oxide thickness ~50nm from 1000C/60min (cm)
Vfb = -0.9            # Typical Flatband voltage for Al-gate/p-Si (V)
# --- 3. Derived Parameters ---
# Doping concentration Na from resistivity and specified mobility
Na = 1 / (rho * q * mu_p)
phi_f = Vt * np.log(Na / ni)  # Fermi potential
Cox = eps_ox / tox            # Oxide capacitance (F/cm^2)
# --- 4. C-V Curve Simulation ---
V_gate = np.linspace(-2.5, 2.5, 500)
C_total = []
for Vg in V_gate:
    V_eff = Vg - Vfb  # Effective voltage relative to Flatband
    if V_eff <= 0:
        # Accumulation Region
        C = Cox
    else:
        # Depletion and Inversion (High Frequency)
        # Using the standard depletion approximation
        # Solving for surface potential (psi_s)
        # V_eff = psi_s + sqrt(2 * q * eps_si * Na * psi_s) / Cox
        gamma = np.sqrt(2 * q * eps_si * Na) / Cox
        psi_s = ((-gamma + np.sqrt(gamma**2 + 4 * V_eff)) / 2)**2
        # Limit psi_s to 2*phi_f for High Frequency Inversion
        if psi_s > 2 * phi_f:
            psi_s = 2 * phi_f
        W = np.sqrt((2 * eps_si * psi_s) / (q * Na))
        Cs = eps_si / W if W > 0 else 1e6
        C = (Cox * Cs) / (Cox + Cs)
    C_total.append(C * 1e9)  # Convert to nF/cm^2
# --- 5. Visualization ---
plt.figure(figsize=(9, 6))
plt.plot(V_gate, C_total, color='teal', linewidth=2.5, label='HF C-V Curve')
plt.axvline(x=Vfb, color='red', linestyle='--', label=f'Flatband ($V_{{fb}}$={Vfb}V)')
plt.title(f"MOS C-V Characteristic ($N_a$ = {Na:.2e} $cm^{{-3}}$)")
plt.xlabel("Gate Voltage ($V_g$) [V]")
plt.ylabel("Capacitance [nF/cm²]")
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()
print(f"Calculated Doping (Na): {Na:.2e} cm^-3")
print(f"Oxide Capacitance (Cox): {Cox*1e9:.4f} nF/cm^2")
