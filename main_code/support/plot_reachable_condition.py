from main_code.support.support_functions import get_np_array
from main_code.rheometer import Rheometer
import matplotlib as mpl
from tqdm import tqdm
import numpy as np

from REFPROPConnector import (

    DiagramPlotterOptions,
    DiagramPlotter

)


class ReachableConditionPlotter:

    def __init__(self, rheometer: Rheometer, options: DiagramPlotterOptions, n_points=200):

        self.options = options
        self.n_points = n_points

        self.reachable_calc_result = {}

        self.rheometer = rheometer
        self.support_point = rheometer.initial_state.duplicate()
        self.dg_plotter = DiagramPlotter(self.support_point, self.options)

    def calculate(self):

        self.__calculate_reachable()
        self.dg_plotter.calculate()

    def __calculate_reachable(self):

        pbar = tqdm(desc="Reachable Conditions Calculations", total=self.n_points * self.n_points)

        res_points = get_np_array(0, 0, self.n_points)
        x_points = self.options.get_range(n_points=self.n_points, return_x_ax=True)
        y_points = self.options.get_range(n_points=self.n_points, return_x_ax=False)

        res, b = np.meshgrid(res_points, x_points, indexing='ij')
        x_mesh, y_mesh = np.meshgrid(x_points, y_points, indexing='ij')

        for i in range(self.n_points):

            for j in range(self.n_points):

                self.support_point.set_variable(self.options.x_ax, x_mesh[i, j])
                self.support_point.set_variable(self.options.y_ax, y_mesh[i, j])

                t_desired = self.support_point.get_variable("T")
                p_desired = self.support_point.get_variable("P")
                is_reachable = self.rheometer.is_condition_reachable(t_desired=t_desired, p_desired=p_desired * 10)

                if is_reachable:
                    res[i, j] = 1

                else:
                    res[i, j] = 0

                pbar.update(1)

        self.reachable_calc_result = {

            "x": x_mesh,
            "y": y_mesh,
            "z": res

        }
        pbar.close()

    def plot(self, ax_1):

        res = self.reachable_calc_result

        if len(res.keys()) == 3:

            ax_1 = self.dg_plotter.plot(ax_1)
            ax_1.contourf(res["x"], res["y"], res["z"], self.n_points * 2, cmap=mpl.colormaps["RdYlGn"], alpha=0.5)

        return ax_1
