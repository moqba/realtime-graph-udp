import random

from realtime_graph_udp.graph_server import GraphData, decode_graph_data


def test_encode_decode_graph_data():
    data_to_encode = GraphData(label="mock data to encode", x_value=random.randint(1, 100),
                               y_value=random.randint(1, 100))
    encoded_data = data_to_encode.encode_data()
    decoded_data = decode_graph_data(encoded_data)
    assert data_to_encode == decoded_data
