import prometheus_client
import time
import psutil

UPDATE_PERIOD = 1
SYSTEM_USAGE = prometheus_client.Gauge('sys_load',
                                       'Hold current system resource usage',
                                       ['resource_type'])

if __name__ == '__main__':
  prometheus_client.start_http_server(8000)
  
while True:
  SYSTEM_USAGE.labels('CPU').set(psutil.cpu_percent())
  SYSTEM_USAGE.labels('Memory').set(psutil.virtual_memory()[2])
  time.sleep(UPDATE_PERIOD)