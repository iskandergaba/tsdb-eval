import os
import time
import psycopg2
import pandas as pd
import matplotlib.pyplot as plt
from pylab import rcParams
plt.style.use('fivethirtyeight')
rcParams['figure.figsize'] = 18, 8

DB_NAME = "sys_load"

def main():
    # Initialize the database
    connection = psycopg2.connect(user="postgres",
                                password="root",
                                host="localhost",
                                port="5432",
                                database=DB_NAME)
    connection.autocommit = True
    count = 0
    while True:
        df_24h = read_data(connection, "cpu_load_24h", "24 hours")
        df_7d = read_data(connection, "cpu_load_7d", "7 days")
        df_30d = read_data(connection, "cpu_load_30d", "30 days")
        plot(df_24h, figname='cpu_load_24h-{}.png'.format(count), title='CPU Load in The Last 24 Hours')
        plot(df_7d, figname='cpu_load_7d-{}.png'.format(count), title='CPU Load in The Last 7 days')
        plot(df_30d, figname='cpu_load_30d-{}.png'.format(count), title='CPU Load in The Last 30 days')
        count = (count + 1) % 5
        time.sleep(60)

def read_data(connection, table, interval):
    cursor = connection.cursor()

    sql = """SELECT *
                FROM {}
                WHERE ts_bucket > NOW() - INTERVAL '{}'
                ORDER BY ts_bucket ASC""".format(table, interval)
    cursor.execute(sql)
    results = cursor.fetchall()
    df = pd.DataFrame(results, columns=['ts', 'cpu_load_min', 'cpu_load_avg', 'cpu_load_max'])
    df.set_index('ts', inplace=True)

    cursor.close()
    return df

def plot(df, save_dir='../plots', figname='plot.png', title='CPU Load'):
    save_path = '../plots/{}'.format(figname)

    # Create save directory if it does not exist
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    ax = df['cpu_load_min'].plot(label="Minimum", marker='v')
    df['cpu_load_max'].plot(ax=ax, label='Maximum', marker='^')
    df['cpu_load_avg'].plot(ax=ax, label='Average', marker='o')
    ax.set_xlabel('Time')
    ax.set_ylabel('CPU Load')
    ax.text(df.index[-1], df['cpu_load_avg'].iloc[-1], '{:.2f}'.format(df['cpu_load_avg'].iloc[-1]))
    plt.title(title)
    plt.legend()
    plt.savefig(save_path, bbox_inches='tight', pad_inches=0.5, transparent=True)
    plt.close()

if __name__ == "__main__":
    main()