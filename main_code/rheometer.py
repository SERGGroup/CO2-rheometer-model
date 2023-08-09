from REFPROPConnector import ThermodynamicPoint
from collections.abc import Iterable


DEFAULT_UNC = {

    "T": 0.1,
    "P": 0.01,
    "rho": 15

}


class Rheometer:

    def __init__(

            self, p_max_cell=150, p_max_cylinder=60, t_min_cell=5,
            p_measured=False, rho_measured=False

    ):

        self.t_min_cell = t_min_cell
        self.p_max_cell = p_max_cell
        self.p_max_cyl = p_max_cylinder

        self.p_measured = p_measured
        self.rho_measured = rho_measured

        self.initial_state = ThermodynamicPoint(["Carbon Dioxide"], [1])
        self.__tmp_state = self.initial_state.duplicate()
        self.__density_calculation = False

    def update_input_condition(self, t_in, p_in=None, rho_in=None):

        self.initial_state.set_variable("T", t_in)

        if rho_in is not None:

            self.__density_calculation = True
            self.initial_state.set_variable("rho", rho_in)

        else:

            self.__density_calculation = False
            self.initial_state.set_variable("P", p_in / 10)

    def estimate_input_condition(self, t_desired, p_desired, p_input=None):

        if p_input is None:
            p_input = self.p_max_cyl

        self.__tmp_state.set_variable("T", t_desired)
        self.__tmp_state.set_variable("P", p_desired / 10)

        self.initial_state.set_variable("rho", self.__tmp_state.get_variable("rho"))
        self.initial_state.set_variable("P", p_input / 10)

    def calculate_current_pressure(self, t_new_value):

        if issubclass(type(t_new_value), Iterable):

            result_list = list()

            for t_new in t_new_value:

                result_list.append(self.__get_output_state(t_new=t_new).get_variable("P") * 10)

            return result_list

        return self.__get_output_state(t_new=t_new_value).get_variable("P") * 10

    def calculate_pressure_uncertainties(self, t_new, calculate_with_derivatives=False):

        return_dict = self.__get_uncertainties(t_new, state_var="P", calculate_with_derivatives=calculate_with_derivatives)
        return {

            "dvar": return_dict["dvar"] * 10,
            "range": [return_dict["range"][0] * 10, return_dict["range"][1] * 10]

        }

    def is_condition_reachable(self, t_desired, p_desired):

        if p_desired > self.p_max_cell:

            return False

        self.estimate_input_condition(t_desired, p_desired)

        if self.t_in < self.t_min_cell:

            return False

        if self.input_is_bifase:

            return self.rho_measured

        return self.p_in <= self.p_max_cyl

    @property
    def t_in(self):

        return self.initial_state.get_variable("T")

    @property
    def rho_in(self):

        return self.initial_state.get_variable("rho")

    @property
    def p_in(self):

        return self.initial_state.get_variable("P") * 10

    @property
    def input_is_bifase(self):

        input_q = self.initial_state.get_variable("Q")

        if type(input_q) is float:

            return 0 < input_q < 1

        else:

            return False

    def __get_output_state(self, t_new, input_point=None):

        if input_point is None:

            input_point = self.initial_state

        new_state = input_point.duplicate()
        new_state.set_variable("rho", input_point.get_variable("rho"))
        new_state.set_variable("T", t_new)

        return new_state

    def __get_uncertainties(self, t_new, state_var="P", calculate_with_derivatives=False):

        if not calculate_with_derivatives:

            return self.__get_uncertainties_std(t_new=t_new, state_var=state_var)

        else:

            return self.__get_uncertainties_der(t_new=t_new, state_var=state_var)

    def __get_uncertainties_std(self, t_new, state_var="P"):

        std_new = self.__get_output_state(t_new)

        dt = DEFAULT_UNC["T"]
        t_in = self.initial_state.get_variable("T")

        if self.__density_calculation:

            var_in_name = "rho"

        else:

            var_in_name = "P"

        var_in = self.initial_state.get_variable(var_in_name)
        dvar_in = DEFAULT_UNC[var_in_name]

        max_value = std_new.get_variable(state_var)
        min_value = std_new.get_variable(state_var)

        for i in [-1, 0, 1]:

            for j in [-1, 0, 1]:

                self.__tmp_state.set_variable(var_in_name, var_in + i * dvar_in)
                self.__tmp_state.set_variable("T", t_in + j * dt)

                for k in [-1, 0, 1]:

                    t_out_curr = t_new + k * dt
                    curr_new = self.__get_output_state(t_out_curr, input_point=self.__tmp_state)
                    curr_value = curr_new.get_variable(state_var)

                    if max_value < curr_value:
                        max_value = curr_value

                    elif min_value > curr_value:
                        min_value = curr_value

        return {

            "dvar": (max_value - min_value) / 2,
            "range": [min_value, max_value]

        }

    def __get_uncertainties_der(self, t_new, state_var="P"):

        std_out = self.__get_output_state(t_new)

        dt = DEFAULT_UNC["T"]

        if self.__density_calculation:

            drho = DEFAULT_UNC["rho"]

        else:

            dp = DEFAULT_UNC["P"]
            drhodt_in = self.initial_state.get_derivative("rho", "T", "P")
            drhodp_in = self.initial_state.get_derivative("rho", "P", "T")

            drho = abs(drhodt_in * dt) + abs(drhodp_in * dp)

        dvardt = std_out.get_derivative(state_var, "T", "rho")
        dvardrho = std_out.get_derivative(state_var, "rho", "T")

        std_var = std_out.get_variable(state_var)
        dvar = abs(dvardt * dt) + abs(dvardrho * drho)

        return {

            "dvar": dvar,
            "range": [std_var - dvar, std_var + dvar]

        }
