# [Prometheus](https://prometheus.io)
## Requirements

## Install Prometheus via Docker
1. Get the latest image of TimeScaleDB
```
docker pull prom/prometheus
```

2. Spin a container instance that will monitor itself.
```
cd prometheus
docker run -d \
    --name prometheus \
    --add-host=hostname:$(hostname -I) \
    -p 9090:9090 \
    -v ./prometheus.yml:/etc/prometheus/prometheus.yml \
    prom/prometheus
```

3. Give it a couple of minutes so that some data is collected, then head to [http://localhost:9090](http://localhost:9090), select a time series like `scrape_duration_seconds` for instance and take a look at its graph.
## Set the Database

## Run the Code
### Java

### Python

[Return to parent](../README.md)