from dataclasses import dataclass
import itertools

from PyQt6.QtCore import QThread, pyqtSignal, QObject, QTimer
from PyQt6.QtWidgets import QApplication, QMainWindow, QGridLayout, QWidget
import pyqtgraph as pg
import numpy as np
import signal

from pyqtgraph import PlotDataItem
from realtime_graph_udp.graph_server import GraphServer, DEFAULT_GRAPH_PORT, \
    DEFAULT_IP_LOCALHOST


@dataclass
class GraphSettings:
    graph_title: str
    x_label: str = ""
    y_label: str = ""
    x_range: tuple[float, float] | None = None
    y_range: tuple[float, float] | None = None


@dataclass
class PlotLabel:
    label: str
    color: str | None = None


class GraphWorker(QObject):
    def __init__(self, ip: str = DEFAULT_IP_LOCALHOST, port: int = DEFAULT_GRAPH_PORT):
        super().__init__()
        self.graph_server = GraphServer(ip=ip, port=port)
        self.plot_data = tuple()

    plot_update = pyqtSignal(tuple)
    end_of_run = pyqtSignal()

    def run(self):
        self.plot_data = self.graph_server.fetch_data()
        if self.plot_data:
            self.plot_update.emit((self.plot_data.label, self.plot_data.x_value, self.plot_data.y_value))
            self.plot_data = tuple()
        self.end_of_run.emit()


class MainGraphWindow(QMainWindow):
    def __init__(self, graph_settings: GraphSettings, plot_labels: list[PlotLabel], ip: str = DEFAULT_IP_LOCALHOST,
                 port: int = DEFAULT_GRAPH_PORT):
        super().__init__()

        layout = QGridLayout()  # overall layout

        self.setWindowTitle(graph_settings.graph_title)
        self.graph_thread = QThread()
        self.graph_thread.setObjectName(f"{graph_settings.graph_title}_thread")
        worker = GraphWorker(ip=ip, port=port)
        worker.moveToThread(self.graph_thread)

        plot_widget = self._setup_plot_widget(graph_settings)
        default_colors = itertools.cycle(["b", "c", "g", "m", "r", "y"])

        self.plot_curves: dict[str, PlotDataItem] = dict()
        self.plots_x_axis: dict[str, np.ndarray] = dict()
        self.plots_y_axis: dict[str, np.ndarray] = dict()
        for plot_label in plot_labels:
            self.plots_x_axis[plot_label.label] = np.array([])
            self.plots_y_axis[plot_label.label] = np.array([])
            if plot_label.color is None:
                pen_color = next(default_colors)
            else:
                pen_color = plot_label.color
            self.plot_curves[plot_label.label] = plot_widget.plot(self.plots_x_axis[plot_label.label],
                                                                  self.plots_y_axis[plot_label.label],
                                                                  name=plot_label.label, pen=pen_color)

        layout.addWidget(plot_widget, 1, 0)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        def update_curve_callback(data: tuple[str, float, float]):
            label, x, y = data
            self.plots_x_axis[label] = np.append(self.plots_x_axis[label], x)
            self.plots_y_axis[label] = np.append(self.plots_y_axis[label], y)
            self.plot_curves[label].setData(self.plots_x_axis[label], self.plots_y_axis[label])

        def end_of_run_callback():
            QTimer.singleShot(3, worker.run)  # Run worker again immediately

        worker.plot_update.connect(update_curve_callback)
        worker.end_of_run.connect(end_of_run_callback)

        self.graph_thread.started.connect(worker.run)  # kicks off the worker when the thread starts
        self.graph_thread.start()

    def _setup_plot_widget(self, graph_settings: GraphSettings) -> pg.PlotWidget:
        plot_widget = pg.PlotWidget(labels={'left': graph_settings.y_label, 'bottom': graph_settings.x_label, 'top': graph_settings.graph_title})
        plot_widget.setMouseEnabled(x=False, y=True)
        plot_widget.addLegend()
        if graph_settings.x_range is not None:
            plot_widget.setXRange(graph_settings.x_range[0], graph_settings.x_range[1])
        if graph_settings.y_range is not None:
            plot_widget.setYRange(graph_settings.y_range[0], graph_settings.y_range[1])
        return plot_widget


def run_live_plot(graph_settings: GraphSettings, plot_labels: list[PlotLabel], ip: str = DEFAULT_IP_LOCALHOST,
                  port: int = DEFAULT_GRAPH_PORT):
    app = QApplication([])
    window = MainGraphWindow(graph_settings, plot_labels, ip, port)
    window.show()
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    app.exec()
