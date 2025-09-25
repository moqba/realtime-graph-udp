# realtime-graph-udp
This is a tool to perform, non-blocking, fast live plotting in python sending data via UDP. This is an integration of PyQtGraph leveraging the optimization for smooth, real-time updates packaged for simple use.  
This tool initially was created to allow live graphing in python tests without impacting testing time or performance. By sending data via UDP, the test performance is not impacted. The graph process can be launched in a different python process to avoid impacting the test.

![til](./doc/plot_demo.gif)

## Current features
- Axis range can be predefined or will be automatically scaling according to data added.
- Modular graph allowing user to add as many labels necessary.
- Data can be sent from a station to another using UDP

## Implementation
Refer to the test example [`test_real_time_graph.py`](./realtime_graph_udp/tests/test_real_time_graph.py) to view the implementation.
