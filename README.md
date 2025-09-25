# realtime-graph-udp
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

This tool provides non-blocking, high-performance live plotting in Python using UDP for data transmission. It integrates PyQtGraph to deliver smooth, real-time updates while remaining lightweight and simple to use.

Originally developed to enable live visualization in Python test environments without slowing down execution, it offloads plotting to a separate process. By streaming data over UDP, test performance remains unaffected, and the graphing process can run independently to ensure seamless, real-time monitoring.

![til](./doc/plot_demo.gif)

## Current features
- Modular graphing – add multiple labels to a graph and send data to all of them through the same UDP socket. 
- UDP support – send and receive data across stations for remote visualization.
- Flexible axis control – ranges can be predefined or automatically scale to incoming data; X axis, Y axis, and graph title can all be customized.
## Implementation
Refer to the test example [`test_real_time_graph.py`](./realtime_graph_udp/tests/test_real_time_graph.py) to view the implementation.
