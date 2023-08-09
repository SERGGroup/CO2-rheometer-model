# %% --------------- IMPORT CLASSES                              ---------------------------------------------------- #
from main_code.rheometer import Rheometer
from matplotlib import pyplot as plt
from scipy.stats import linregress
import numpy as np


# %% --------------- CALCULATE DIRECTLY                           ---------------------------------------------------- #
t_in = -10         # [°C]
rho_in = 850      # [kg/m^3]
t_new_max = 60    # [°C]
t_new_list = np.linspace(t_in, t_new_max, num=1000)

# Initialize the class
rheometer = Rheometer()

# Set the Initial Condition
rheometer.update_input_condition(t_in=t_in, rho_in=rho_in)

# Calculate the expected pressure for a given temperature
p_new_list = np.array(rheometer.calculate_current_pressure(t_new_value=t_new_list))

dt = t_new_list[1:] - t_new_list[:-1]
dpdt = (p_new_list[1:] - p_new_list[:-1]) / dt
ddpddt = abs((dpdt[1:] - dpdt[:-1]) / dt[:-1])

max_ddp = max(ddpddt)
t_trans = t_new_list[list(ddpddt).index(max_ddp) - 1]


# %% --------------- SIMULATE NOISE                               ---------------------------------------------------- #
sigma_t = 0.1   # [°C] (PT100 uncertainty)
sigma_p = 1     # [bar]

noisy_t = t_new_list + np.random.normal(0, sigma_t, len(t_new_list))
noisy_p = p_new_list + np.random.normal(0, sigma_p, len(p_new_list))

noisy_dt = noisy_t[1:] - noisy_t[:-1]
noisy_dpdt = (noisy_p[1:] - noisy_p[:-1]) / noisy_dt
noisy_ddpddt = abs((noisy_dpdt[1:] - noisy_dpdt[:-1]) / noisy_dt[:-1])


# %% --------------- EXTRACT DP/DT TROUGH LINEAR INTERPOLATION    ---------------------------------------------------- #
half_wind_size = 50
wind_size = 2 * half_wind_size

int_dpdt = np.zeros(len(noisy_t) - wind_size)
int_t = np.zeros(len(noisy_t) - wind_size)

for i in range(len(noisy_t) - wind_size):

    k_str = i + half_wind_size
    k_end = i + wind_size
    result = linregress(noisy_t[k_str: k_end], noisy_p[k_str: k_end])

    int_dpdt[i] = result.slope
    int_t[i] = np.mean(noisy_t[k_str: k_end])


# %% --------------- PLOT RESULTS                                 ---------------------------------------------------- #
fig, (ax_1) = plt.subplots(1, 1, dpi=300)
fig.set_size_inches(10, 5)
show_clear_data = True

ax_2 = ax_1.twinx()
ax_3 = ax_1.twinx()
ax_3.get_yaxis().set_visible(False)

ax_2.set_ylabel("$dp/dt\ [bar/^{\circ}C]$")
ax_1.set_xlabel("$T\ [^{\circ}C]$")
ax_1.set_ylabel("$p\ [bar]$")

if show_clear_data:

    lns = ax_1.plot(t_new_list, p_new_list, label="p", color="tab:blue", alpha=0.3, linewidth=8)
    lns += ax_2.plot(t_new_list[:-1], dpdt, label="dp/dt", color="tab:orange", alpha=0.3, linewidth=8)
    lns += ax_1.plot(noisy_t, noisy_p, label="p noisy", color="tab:blue")

else:

    lns = ax_1.plot(noisy_t, noisy_p, label="p noisy", color="tab:blue")

lns += ax_2.plot(int_t, int_dpdt, color="tab:orange", label="dp/dt smooted")
lns += ax_3.plot(noisy_t[:-1], noisy_dpdt, label="dp/dt noisy", color="tab:orange", alpha=0.3)

labs = [l.get_label() for l in lns]
ax_1.legend(lns, labs)
plt.tight_layout(pad=3)
plt.show()
