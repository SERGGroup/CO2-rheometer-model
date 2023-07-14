# %% --------------- IMPORT CLASSES                              ---------------------------------------------------- #
from main_code.rheometer import Rheometer


# %% --------------- CALCULATE DIRECTLY                           ---------------------------------------------------- #
t_in = 30   # [°C]
p_in = 55   # [bar]
t_new = 80  # [°C]

# Initialize the class
rheometer = Rheometer()

# Set the Initial Condition
rheometer.update_input_condition(t_in=t_in, p_in=p_in)

# Calculate the expected pressure for a given temperature
p_out = rheometer.calculate_current_pressure(t_new=t_new)

# Estimate the pressure uncertainties
p_unc = rheometer.calculate_pressure_uncertainties(t_new=t_new, calculate_with_derivatives=False)


# %% --------------- CALCULATE INVERSE                           ---------------------------------------------------- #
# Ask the class to set its initial state in order to reach the desired state after the heating
# (defined by pressure and temperature)
rheometer.estimate_input_condition(t_desired=t_new, p_desired=p_out, p_input=p_in)

# Read the required initial temperature
t_in_required = rheometer.t_in

# Check if the desired condition is reachable
is_rchbl = rheometer.is_condition_reachable(t_desired=t_new, p_desired=p_out)
