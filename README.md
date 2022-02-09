# TSDB Evaluation
This is a short report comparing the most popular TSDBs to one another along with a demo and quick setup guides. This is not a comprehensive list of all TSDBs available, but only of the most popular and mature ones.

## Summary

|| TimescaleDB | InfluxDB | QuestDB | Prometheus |
|--------------------------|---|---|---|---|
| Licensing | [MIT](https://github.com/influxdata/influxdb/blob/master/LICENSE) | [Apache 2.0](https://github.com/timescale/timescaledb/blob/master/LICENSE) | [Apache 2.0](https://github.com/questdb/questdb/blob/master/LICENSE.txt) | [Apache 2.0](https://github.com/prometheus/prometheus/blob/main/LICENSE)|
| Data model 			    | SQL ([PostgreSQL](https://docs.timescale.com/timescaledb/latest/overview)) | NoSQL (Custom<sup>[1](https://medium.com/dataseries/analysis-of-the-storage-mechanism-in-influxdb-b84d686f3697), [2](https://docs.influxdata.com/influxdb/v2.1/reference/internals/storage-engine)</sup>) | NoSQL ([Column-based](https://questdb.io/docs/concept/storage-model)) | NoSQL ([TSDB format](https://prometheus.io/docs/prometheus/latest/storage)) |
| Data Retention Settings 	| 🟢 [Auto](https://docs.timescale.com/timescaledb/latest/getting-started/data-retention) | 🟢 [Auto](https://docs.influxdata.com/influxdb/v2.1/organizations/buckets) | 🟡 [Manual](https://questdb.io/docs/operations/data-retention) | 🟡 [Limited](https://stackoverflow.com/questions/69630832/how-to-store-data-in-prometheus-with-different-retention-time-per-job-or-targets) |
| Continuous Aggregation			| 🟢 [Auto](https://docs.timescale.com/timescaledb/latest/getting-started/create-cagg/) | 🟢 [Auto](https://docs.influxdata.com/influxdb/v2.1/process-data/get-started) | 🟡 [Manual](https://questdb.io/docs/reference/sql/sample-by) | 🟢 [Auto](https://prometheus.io/docs/prometheus/latest/configuration/recording_rules) |
| Data Compression			| 3 ⭐ | 4 ⭐ | 4 ⭐ | 4 ⭐ |
| Performance				| 3 ⭐ | 3 ⭐ | 4 ⭐ | 4 ⭐ |
| Scalability				| 4 ⭐ | 3 ⭐ | ? ⭐ | ? ⭐ |
| Maturity					| 5 ⭐ | 3 ⭐ | 2 ⭐ | 4 ⭐ |
| Learning curve			| 🟢 | 🟡 | 🔴 | 🔴 |
| Java support				| 🟢 | 🟢 | 🟢 | 🟢 |
| Python support			| 🟢 | 🟢 | 🟢 | 🟢 |
| C/C++ support				| 🟢 | ? | ? | ? |
| C# support				| 🟢 | ? | ? | ? |
| Apache Kafka support		| ? | ? | ? | ? |
| Grafana support			| 🟢 | ? | ? | ? |

## Benchmarks
### [influxdb-comparisons (by InfluxData)](https://github.com/influxdata/influxdb-comparisons)
In 2016, InfluxData created started this repository that benchmarks InfluxDB against other TSDBs. Currently, the benchmark supports **Elasticsearch**, **Cassandra**, **MongoDB**, **OpenTSDB**, **TimescaleDB**, **Graphite** and **Splunk**. While they boast having beaten ElasticSearch, Cassandra, and MongoDB (which are not designed with time-series specifically in mind), they weirdly leave it to the user to run their benchmark and determine performance levels of InfluxDB against other databases. The benchmark tests data generation, data loading, query generation, query execution and query validation.

### [Time Series Benchmark Suite (by TimescaleDB)](https://github.com/timescale/tsbs)
In response Timescale created Time Series Benchmark Suite (TSBS). It currently supports **Akumuli**, **Cassandra**, **ClickHouse**, **CrateDB**, **InfluxDB**, **MongoDB**, **QuestDB**, **SiriDB**, **TimescaleDB**, **Timestream** and **VictoriaMetrics**. Using TSBS for benchmarking involves 3 phases: data and query generation, data loading/insertion, and query execution. TSBS is more widely adopted by the comunity as a reliable benchmark for comparisons, some of which are listed in the section below.


## Comparisons
### [InfluxDB ⚔️ TimescaleDB ⚔️ QuestDB (by QuestDB)](https://questdb.io/tutorial/2021/07/05/comparing-questdb-timescaledb-influxdb)
In this article, QuestDB makers used [TSBS](https://github.com/timescale/tsbs) to evaluate performance against InfluxDB and TimescaleDB. This benchmark served to show that QuestDB superior ingestion rates in both low and high cardinality settings. The authors acknowledge that "As a newer entrant in this space, the most apparent downside to QuestDB is the lack of features such as replication."

### [TimescaleDB ⚔️ InfluxDB (by TimescaleDB)](https://blog.timescale.com/blog/timescaledb-vs-influxdb-for-time-series-data-timescale-influx-sql-nosql-36489299877)
Timescale also made their contribution to this TSDB arms race to showcase the superiority of their product over the leading TSDB, InfuxDB.

- **Data model:** The article concludes that the tagset data model in InfluxDB is more limiting and thus might be easier to get started with for some. However, the relational model in TimescaleDB is more versatile and offers more functionality, flexibility, and control. This is especially important as the application evolves.


- **Reliability:** Timescale argues that InfluxDB had to design and implement all recovery, reliability and durability functionality from scratch which is a notoriously hard problem in databases that typically takes many years or even decades to get correct. They claim that every database goes through a period when it sometimes loses data because it's really, really hard to get all the corner cases right. And eventually, all those corner cases come to haunt some operator. But, PostgreSQL went through this period in the 1990s, while InfluxDB is still figuring these things out today.

- **Performance:** The insert performance analysis concluded that as cardinality increases, InfluxDB performance drops dramatically due to its reliance on time-structured merge trees (which, similar to the log-structured merge trees it is modeled after, suffers with higher-cardinality datasets). As far as read latency goes, their analysis concluded that TimescaleDB outperforms InfluxDB on both simple and complex queries for the vast majority of cases.

- **Resource consumption:**
	- ***Disk usage:*** Even though TimescaleDB offers native compression, InfluxDB is able achieve better compression ratios overall thanks to its column-oriented structure.
	- ***CPU usage:*** TimescaleDB has 10x better resource utilization (even with 30% higher requests) when compared to InfluxDB according to this analysis.

### [TimescaleDB ⚔️ InfluxDB (by Severalnines)](https://severalnines.com/database-blog/which-time-series-database-better-timescaledb-vs-influxdb)
- Severalnines also made their own comparison of TimescaleDB and InfluxDB. They highlighted that although InfluxDB is easier to get started with as users do not need to worry about creating schemas, it is not a schemaless database as an underlying schema is automatically generated from the input data. They also note that InfluxDB had to implement several tools from scratch to ensure fault-tolerance, replication, reliability, high availability, backup/restore, etc. and many of those features are only available in the enterprise version. They also pointed out that InfluxDB offers a significantly better on-disk compression than TimescaleDB.

- On the other hand, they appreciated that TimescaleDB, being a PostgreSQL extension in nature, offers a short learning curve for new users and fully benefits from the well tested and proven backup and high availability tools that come with PostgreSQL like `pg_dump` and `pg_backup`. Basically, TimescaleDB inerits all the functionality and schema flexibility of PostgreSQL, and provides more capabilities on the top of them.

- As far as insert rates go, Severalnine's analysis concluded that for workloads with low cardinality (i.e. small number of devices), InfluxDB outperforms. But as cardinality increases, InfluxDB performance drops off faster and eventually TimescaleDB outperforms it.

- As far as read query performance goes, both databases perform comparably for simple queries. However, TimescaleDB vastly outperforms InfluxDB for complex queries and supports a broader range of query types.

- Finally, they also noted that InfluxDB has stability and performance issues at high (100K+) cardinalities.

### [TimescaleDB ⚔️ InfluxDB (by United Manufacturing Hub)](https://docs.umh.app/docs/concepts/timescaledb-vs-influxdb)
In this analysis, United Manufacturing Hub ruled that TimescaleDB is better suited for the Industrial IoT than InfluxDB thanks to its stability, maturity, and failure resistance. Below is the summary of the arguments they presented:

1. **Reliability and scalability:** TimescaleDB is built on PostgreSQL which is continuously being developed for more than 25 years. A proven database technology that can scale horizontally across many servers. InfluxDB is a relatively new startup. Despite its massive funding and being it the leader in TSDB field, it still lacks stability. In fact, InfluxData has completely rewritten its database at least two times in the past (actually more, see this [article](https://medium.com/dataseries/analysis-of-the-storage-mechanism-in-influxdb-b84d686f3697) for a complete history of InfluxDB storage engine re-writings.)

2. **SQL is better known than flux:** TimescaleDB, like PostgreSQL, relies on SQL (it is 100% SQL compliant in fact), the de facto standard language for relational databases that has been established for more than 45 years. This makes for a smooth learning curve for developers and a massive comunity support. InfluxDB, on the other hand, relies on the homegrown flux, a flow-based language that is supposed to simplify time-series data queries. The problem with it it is that it forces the developer to think differently (not using good old relational algebra) and makes for a steep learning curve for the development team.

    - **Iskander'a note:** *From the point of view of readbility, it is an abomination.*

3. **Relational data**
United Manufacturing Hub concludes its reasoning with the argument that production data is often relational, and chances are that your product will need a relational database anyway, so better stick to PostgreSQL/timescaleDB and reduce the complexity rather than run two completely different datbases.

## Demos
- **[TimescaleDB](./timescaledb/README.md)**
- **[InfluxDB](./influxdb/README.md)**
- **[QuestDB](./questdb/README.md)**
- **[Prometheus](./prometheus/README.md)**
