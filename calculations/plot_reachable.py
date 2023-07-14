# %% --------------- IMPORT CLASSES                              ---------------------------------------------------- #
from main_code.support.plot_reachable_condition import ReachableConditionPlotter
from REFPROPConnector import DiagramPlotterOptions
from main_code.rheometer import Rheometer
from matplotlib import pyplot as plt
import matplotlib.ticker as ticker


# %% --------------- INITIALIZE RHEOMETER                         ---------------------------------------------------- #
rheometer = Rheometer(rho_measured=False)


# %% --------------- PLOT REACHABLE RANGE P-rho                   ---------------------------------------------------- #
options = DiagramPlotterOptions(

    x_variable="rho", x_var_range=(100, 1000), x_var_log=True,
    y_variable="P", y_var_range=(6, 15), y_var_log=True

)

plotter = ReachableConditionPlotter(rheometer, options=options, n_points=250)
plotter.calculate()

fig, (ax_1) = plt.subplots(1, 1, dpi=200)
fig.set_size_inches(10, 5)
plotter.plot(ax_1)

ax_1.xaxis.set_major_formatter(ticker.FormatStrFormatter('%0.0f'))
ax_1.xaxis.set_minor_formatter(ticker.FormatStrFormatter('%0.0f'))
ax_1.yaxis.set_major_formatter(ticker.FormatStrFormatter('%0.0f'))
ax_1.yaxis.set_minor_formatter(ticker.FormatStrFormatter('%0.0f'))

plt.show()


# %% --------------- PLOT REACHABLE RANGE T-P                     ---------------------------------------------------- #
options = DiagramPlotterOptions(

    x_variable="T", x_var_range=(5, 150), x_var_log=False,
    y_variable="P", y_var_range=(6, 15), y_var_log=True,
    isoline_ranges={

        "rho": (100, 1000, 20)

    }

)


plotter = ReachableConditionPlotter(rheometer, options=options, n_points=350)
plotter.calculate()

fig, (ax_1) = plt.subplots(1, 1, dpi=200)
fig.set_size_inches(10, 5)
plotter.plot(ax_1)

ax_1.yaxis.set_major_formatter(ticker.FormatStrFormatter('%0.0f'))
ax_1.yaxis.set_minor_formatter(ticker.FormatStrFormatter('%0.0f'))

plt.show()
