import socket
import struct
from dataclasses import dataclass
from typing import Final

BUFFER_SIZE: Final[int] = 1024
DEFAULT_IP_LOCALHOST: Final[str] = "127.0.0.1"
DEFAULT_GRAPH_PORT: Final[int] = 3232


@dataclass
class GraphData:
    label: str
    x_value: float
    y_value: float

    def encode_data(self):
        encoded_data = self.label.encode("utf-8") + b"\0"
        encoded_data += struct.pack("ff", self.x_value, self.y_value)
        return encoded_data


def decode_graph_data(encoded_data) -> GraphData:
    label_bytes, float_bytes = encoded_data.split(b"\0", 1)
    label = label_bytes.decode("utf-8")
    x_value, y_value = struct.unpack("ff", float_bytes)
    return GraphData(label=label, x_value=x_value, y_value=y_value)


class GraphClient:
    def __init__(self, ip: str = DEFAULT_IP_LOCALHOST, port: int = DEFAULT_GRAPH_PORT):
        self.ip = ip
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def send_data(self, graph_data: GraphData):
        self.sock.sendto(graph_data.encode_data(), (self.ip, self.port))


class GraphServer:
    def __init__(self, ip: str = DEFAULT_IP_LOCALHOST, port: int = DEFAULT_GRAPH_PORT):
        self.ip = ip
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((self.ip, self.port))

    def fetch_data(self) -> GraphData | None:
        encoded_data, addr = self.sock.recvfrom(BUFFER_SIZE)
        if encoded_data:
            graph_data = decode_graph_data(encoded_data)
            return graph_data
        return None
