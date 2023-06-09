import os
import re
import subprocess
import time
import logging

# change this to be machine independent
this_host = 'pi-hole'

FORMAT = '%(asctime)s %(clientip)-15s %(user)-8s %(message)s'
logging.basicConfig(level=logging.DEBUG)
logging.basicConfig(format=FORMAT)

logging.debug('Starting speedtest')

response = subprocess.Popen('/usr/bin/speedtest --accept-license --accept-gdpr', shell=True, stdout=subprocess.PIPE).stdout.read().decode('utf-8')

ping = re.search('Latency:\s+(.*?)\s', response, re.MULTILINE)
download = re.search('Download:\s+(.*?)\s', response, re.MULTILINE)
upload = re.search('Upload:\s+(.*?)\s', response, re.MULTILINE)
jitter = re.search('Latency:.*?jitter:\s+(.*?)ms', response, re.MULTILINE)

source = this_host
ping = ping.group(1)
download = download.group(1)
upload = upload.group(1)
jitter = jitter.group(1)

logging.debug(f'source:{source} ping:{ping} download:{download} upload:{upload} jitter:{jitter}')

try:

  logging.debug('attempting to open /home/pi/src/speedtest/speedtest.csv')
  f = open('/home/pi/src/speedtest/speedtest.csv', 'a+')
  if os.stat('/home/pi/src/speedtest/speedtest.csv').st_size == 0:
    f.write('Date,Time,Ping (ms),Jitter (ms),Download (Mbps),Upload (Mbps)\r\n')
except Exception as err:
  logging.exception(str(err))

f.write('{},{},{},{},{},{}\r\n'.format(time.strftime('%m/%d/%y'), time.strftime('%H:%M'), ping, jitter, download, upload))
