# [Prometheus](https://prometheus.io)
## Requirements
- Python 3
	- [prometheus-client](https://pypi.org/project/prometheus-client)
        - `pip install prometheus-client`

## Install Prometheus via Docker
1. Get the latest image of TimeScaleDB
```
docker pull prom/prometheus
```

2. Spin a container instance that will monitor [http://localhost:8000](http://localhost:8000).
```
cd prometheus
docker run -d \
    --name prometheus \
    --add-host=hostname:$(hostname -I) \
    -p 9090:9090 \
    -v ./prometheus.yml:/etc/prometheus/prometheus.yml \
    -v ./prometheus.rules:/etc/prometheus/prometheus.rules \
    prom/prometheus
```

3. You should now be able to access the dashboard through [http://localhost:9090](http://localhost:9090). If you go to `Status -> Targets`, you should see that a target under the name `http://hostname:8000` that is down. That is because we are yet to start a server at [http://localhost:8000](http://localhost:8000) that emits system load metrics. `hostname` is set inside the container's `/etc/hosts` to the machine IP address so that Prometheus in the container can access the localhost of the hosting machine where the metrics server is running.

## Run the Code
### Python
- To start the metrics server, run the code in `server.py`. This will start a server that will expose the machines CPU and Memory usage values every second.
```bash
python server.py 
```

- If you go back to the dashboard on [http://localhost:9090](http://localhost:9090) and navigate to `Status -> Targets`, you will see that the target  `http://hostname:8000`. You can now query `sys_load` and plot the machine's CPU and memory usaage over time. Provided that enough time has elapsed for the aggregation to occur, you can also query `sys_load:CPU:rate1m`, `sys_load:CPU:rate10m`, `sys_load:CPU:rate1h`, `sys_load:CPU:rate6h`, `sys_load:CPU:rate12h`, and `sys_load:CPU:rate24h` which are CPU load aggregation continuously computed over the intervals of one minute, ten minutes, one hour, six hours, twelve hours and one day, respectively. The same goes for `sys_load:Memory:rate1m`, `sys_load:Memory:rate10m`, `sys_load:Memory:rate1h`, `sys_load:Memory:rate6h`, `sys_load:Memory:rate12h`, and `sys_load:Memory:rate24h` for memory usage.

[Return to parent](../README.md)