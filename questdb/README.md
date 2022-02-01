# [QuestDB](https://www.questdb.io)
## Requirements

## Setup

## Install QuestDB via Docker
1. Get the latest image of TimeScaleDB
```
docker pull questdb/questdb
```

2. Spin a container instance with telemetry turned off
```
docker run -d --name questdb \
 -e QDB_TELEMETRY_ENABLED=FALSE \
 -p 9000:9000 \
 -p 9009:9009 \
 -p 8812:8812 \
 -p 9003:9003 \
 questdb/questdb
```


## Run the Code
### Java

### Python

[Return to parent](../README.md)