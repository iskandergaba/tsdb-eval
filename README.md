# TSDB Evaluation
This repository is a short report comparing popular TSDBs to one another.

## Summary



|| TimescaleDB | InfluxDB | QuestDB | Prometheus |
|--------------------------|---|---|---|---|
| Data model 			    | SQL ([PostgreSQL](https://docs.timescale.com/timescaledb/latest/overview)) | NoSQL (Custom<sup>[1](https://medium.com/dataseries/analysis-of-the-storage-mechanism-in-influxdb-b84d686f3697), [2](https://docs.influxdata.com/influxdb/v2.1/reference/internals/storage-engine)</sup>) | NoSQL ([Column-based](https://questdb.io/docs/concept/storage-model)) | NoSQL ([TSDB format](https://prometheus.io/docs/prometheus/latest/storage)) |
| Data Retention Settings 	| ✅ [Auto](https://docs.timescale.com/timescaledb/latest/getting-started/data-retention) | ✅ [Auto](https://docs.influxdata.com/influxdb/v2.1/organizations/buckets) | ☑️ [Manual](https://questdb.io/docs/operations/data-retention) | ✅ [Auto](https://prometheus.io/docs/prometheus/latest/storage/#operational-aspects) |
| Continuous Aggregation			| ✅ [Auto](https://docs.timescale.com/timescaledb/latest/getting-started/create-cagg/) | ✅ [Auto](https://docs.influxdata.com/influxdb/v2.1/process-data/get-started) | ❌ No | ✅ [Auto](https://prometheus.io/docs/prometheus/latest/configuration/recording_rules) |
| Data Compression			| 3 ⭐ | 4 ⭐ | 4 ⭐ | 4 ⭐ |
| Performance				| 3 ⭐ | 3 ⭐ | 4 ⭐ | ? ⭐ |
| Scalability				| 4 ⭐ | 3 ⭐ | ? ⭐ | ? ⭐ |
| Maturity					| 5 ⭐ | 3 ⭐ | 2 ⭐ | 3.5 ⭐ |
| Java client					|   |   |   |   |
| Python client					|   |   |   |   |

## Benchmarks
### [influxdb-comparisons (by InfluxData)](https://github.com/influxdata/influxdb-comparisons)
In 2016, InfluxData created started this repository that benchmarks InfluxDB against other TSDBs. Currently, the benchmark supports **Elasticsearch**, **Cassandra**, **MongoDB**, **OpenTSDB**, **TimescaleDB**, **Graphite** and **Splunk**. While they boast having beaten ElasticSearch, Cassandra, and MongoDB (which are not designed with time-series specifically in mind), they weirdly leave it to the user to run their benchmark and determine performance levels of InfluxDB against other databases. The benchmark tests data generation, data loading, query generation, query execution and query validation.

### [Time Series Benchmark Suite (by TimescaleDB)](https://github.com/timescale/tsbs)
In response Timescale created Time Series Benchmark Suite (TSBS). It currently supports **Akumuli**, **Cassandra**, **ClickHouse**, **CrateDB**, **InfluxDB**, **MongoDB**, **QuestDB**, **SiriDB**, **TimescaleDB**, **Timestream** and **VictoriaMetrics**. Using TSBS for benchmarking involves 3 phases: data and query generation, data loading/insertion, and query execution. TSBS is more widely adopted by the comunity as a reliable benchmark for comparisons, some of which are listed in the section below.


## Comparisons
### [InfluxDB ⚔️ TimescaleDB ⚔️ QuestDB (by QuestDB)](https://questdb.io/tutorial/2021/07/05/comparing-questdb-timescaledb-influxdb)
TODO

### [TimescaleDB ⚔️ InfluxDB (by TimescaleDB)](https://blog.timescale.com/blog/timescaledb-vs-influxdb-for-time-series-data-timescale-influx-sql-nosql-36489299877)
TDOD

### [TimescaleDB ⚔️ InfluxDB (by Severalnines)](https://severalnines.com/database-blog/which-time-series-database-better-timescaledb-vs-influxdb)
TDOD

### [TimescaleDB ⚔️ InfluxDB (by United Manufacturing Hub)](https://docs.umh.app/docs/concepts/timescaledb-vs-influxdb)
TDOD

## Demos
- **[TimescaleDB](./timescaledb/README.md)**
- **[InfluxDB](./influxdb/README.md)**
- **[QuestDB](./questdb/README.md)**
- **[Prometheus](./prometheus/README.md)**

## References