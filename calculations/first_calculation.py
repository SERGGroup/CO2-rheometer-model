# %% --------------- IMPORT CLASSES                              ---------------------------------------------------- #
from main_code.rheometer_state import RheometerState


# %% --------------- CALCULATE                                    ---------------------------------------------------- #
state = RheometerState(25, p_in=6)
p_out = state.get_output_state(80, state_var="P")
p_unc = state.get_uncertainties(80, state_var="P")
