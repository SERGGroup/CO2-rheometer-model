from REFPROPConnector import ThermodynamicPoint


DEFAULT_UNC = {

    "T": 0.1,
    "P": 0.01,
    "rho": 15

}


class RheometerState:

    def __init__(self, t_in, p_in=None, rho_in=None):

        self.initial_state = ThermodynamicPoint(["Carbon Dioxide"], [1])
        self.__tmp_state = self.initial_state.duplicate()

        self.initial_state.set_variable("T", t_in)

        if rho_in is not None:

            self.__density_calculation = True
            self.initial_state.set_variable("rho", rho_in)

        else:

            self.__density_calculation = False
            self.initial_state.set_variable("P", p_in)

    def get_output_state(self, t_out, input_point=None):

        if input_point is None:

            input_point = self.initial_state

        new_state = input_point.duplicate()
        new_state.set_variable("rho", input_point.get_variable("rho"))
        new_state.set_variable("T", t_out)

        return new_state

    def get_uncertainties(self, t_out, state_var="P", calculate_with_drivatives=False):

        if not calculate_with_drivatives:

            return self.__get_uncertainties_std(t_out=t_out, state_var=state_var)

        else:

            return self.__get_uncertainties_der(t_out=t_out, state_var=state_var)

    def __get_uncertainties_std(self, t_out, state_var="P"):

        std_out = self.get_output_state(t_out)

        dt = DEFAULT_UNC["T"]
        t_in = self.initial_state.get_variable("T")

        if self.__density_calculation:

            var_in = self.initial_state.get_variable("rho")
            dvar_in = DEFAULT_UNC["rho"]

        else:

            var_in = self.initial_state.get_variable("P")
            dvar_in = DEFAULT_UNC["P"]

        max_value = std_out.get_variable(state_var)
        min_value = std_out.get_variable(state_var)

        min_state = [0, 0, 0]
        max_state = [0, 0, 0]

        for i in [-1, 0, 1]:

            for j in [-1, 0, 1]:

                self.__tmp_state.set_variable("rho", var_in + i * dvar_in)
                self.__tmp_state.set_variable("T", t_in + j * dt)

                for k in [-1, 0, 1]:

                    t_out_curr = t_out + k * dt
                    curr_out = self.get_output_state(t_out_curr, input_point=self.__tmp_state)
                    curr_value = curr_out.get_variable(state_var)

                    if max_value < curr_value:

                        max_value = curr_value
                        max_state = [i, j, k]

                    elif min_value > curr_value:

                        min_value = curr_value
                        min_state = [i, j, k]

        return {

            "dvar": max_value - min_value,
            "range": [min_value, max_value],
            "states": [min_state, max_state]

        }

    def __get_uncertainties_der(self, t_out, state_var="P"):

        std_out = self.get_output_state(t_out)

        dt = DEFAULT_UNC["T"]
        t_in = self.initial_state.get_variable("T")

        if self.__density_calculation:

            drho = DEFAULT_UNC["rho"]

        else:

            dp = DEFAULT_UNC["P"]
            drhodt_in = self.initial_state.get_derivative("rho", "T", "P")
            drhodp_in = self.initial_state.get_derivative("rho", "P", "T")

            drho = drhodt_in * dt + drhodp_in * dp

        dvardt = self.initial_state.get_derivative(state_var, "T", "rho")
        dvardrho = self.initial_state.get_derivative(state_var, "rho", "T")

        std_var = std_out.get_variable(state_var)
        dvar = dvardt * dt + dvardrho * drho

        return {

            "dvar": dvar,
            "range": [std_var - dvar / 2, std_var + dvar / 2],
            "states": [None, None]

        }