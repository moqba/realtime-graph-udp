import multiprocessing
from time import sleep
from typing import Final

from realtime_graph_udp.graph_server import GraphClient, GraphData
from realtime_graph_udp.real_time_plot import GraphSettings, PlotLabel, run_live_plot

PROCESS_START_DELAY: Final[int] = 3
SAMPLING_RATE: Final[float] = 0.5


def test_real_time_plot():
    hp_to_happyiness_ratio = 0.1
    maximum_horse_power = 400
    samples = 25
    graph_settings = GraphSettings(graph_title="Horse power in my motorcycle", x_label="HP", y_label="my happiness factor", x_range=(0,maximum_horse_power))
    plot_labels = [PlotLabel(label="Me"), PlotLabel(label="My wallet")]

    graph_process = multiprocessing.Process(target=run_live_plot, args=(graph_settings, plot_labels))
    graph_process.start()
    sleep(PROCESS_START_DELAY)
    graph_client = GraphClient()
    for i in range(samples):
        horse_power = (maximum_horse_power/samples)*i
        graph_client.send_data(graph_data=GraphData("Me", x_value=horse_power, y_value=horse_power*hp_to_happyiness_ratio))
        graph_client.send_data(graph_data=GraphData("My wallet", x_value=horse_power, y_value=(maximum_horse_power*hp_to_happyiness_ratio)-horse_power*hp_to_happyiness_ratio))
        sleep(SAMPLING_RATE)
    if graph_process is not None:
        graph_process.terminate()
        graph_process.join()
