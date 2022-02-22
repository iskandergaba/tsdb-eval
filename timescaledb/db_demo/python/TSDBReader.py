import psycopg2
import pandas as pd

CONNECTION = "postgres://postgres:root@localhost:5432/metrics"

def main():  
    conn = psycopg2.connect(CONNECTION)

    # Get the first 10 data results
    print('\nsys_load')
    query = """SELECT *
                FROM sys_load
                ORDER BY time ASC
                LIMIT 10"""
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    sys_load_df = pd.DataFrame(results, columns=['time', 'cpu_load', 'memory_usage', 'network_usage'])
    sys_load_df.set_index('time', inplace=True)
    print(sys_load_df.head(10))

    # Get the first 24 hours of aggregations
    print('\nsys_load_hourly')
    query = """SELECT *
                FROM sys_load_hourly
                ORDER BY bucket ASC"""
    cursor.execute(query)
    results = cursor.fetchall()
    sys_load_hourly_df = pd.DataFrame(results, columns=['time', 'cpu_load', 'memory_usage', 'network_usage'])
    sys_load_hourly_df.set_index('time', inplace=True)
    print(sys_load_hourly_df.head(24))

    cursor.close()

if __name__ == "__main__":
    main()