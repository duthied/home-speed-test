import re
import subprocess
from influxdb import InfluxDBClient
import logging

# change this to be machine independent
this_host = 'm1-mbp'

FORMAT = '%(asctime)s %(clientip)-15s %(user)-8s %(message)s'
logging.basicConfig(level=logging.DEBUG)
logging.basicConfig(format=FORMAT)

logging.debug('Starting speedtest - DB')

response = subprocess.Popen('/opt/homebrew/bin/speedtest --accept-license --accept-gdpr', shell=True, stdout=subprocess.PIPE).stdout.read().decode('utf-8')

ping = re.search('Latency:\s+(.*?)\s', response, re.MULTILINE)
download = re.search('Download:\s+(.*?)\s', response, re.MULTILINE)
upload = re.search('Upload:\s+(.*?)\s', response, re.MULTILINE)
jitter = re.search('Latency:.*?jitter:\s+(.*?)ms', response, re.MULTILINE)

source = this_host
ping = ping.group(1)
download = download.group(1)
upload = upload.group(1)
jitter = jitter.group(1)

speed_data = [
    {
        "measurement" : "internet_speed",
        "tags" : {
            "host": "RaspberryPiMyLifeUp"
        },
        "fields" : {
            "download": float(download),
            "upload": float(upload),
            "ping": float(ping),
            "jitter": float(jitter),
            "source": source,
        }
    }
]

logging.debug(f'source:{source} ping:{ping} download:{download} upload:{upload} jitter:{jitter}')

client = InfluxDBClient('pi-hole', 8086, 'speedmonitor', 'Mark2me', 'internetspeed')

client.write_points(speed_data)