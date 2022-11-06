import pdb
import time
#from lxml import etree
from pprint import pprint
from jnpr.junos import Device
import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS
from pykeepass import PyKeePass

### CONFIGURATION ###

DEBUG = False

sleep_time_secs = 60

### CREDENTIALS #####

kp = PyKeePass('db.kdbx')

entry = kp.find_entries_by_title('juniper_device', first=True)
jnpr_host = entry.custom_properties['ip_address']
jnpr_user = entry.username
jnpr_pass = entry.password

entry = kp.find_entries_by_title('influxdb', first=True)
influxdb_url = entry.url
influxdb_bucket = entry.custom_properties['bucket']
influxdb_org = entry.custom_properties['org']
influxdb_token = entry.custom_properties['token']

####################

client = influxdb_client.InfluxDBClient(
    url=influxdb_url,
    token=influxdb_token,
    org=influxdb_org
)

write_api = client.write_api(write_options=SYNCHRONOUS)

while True:

    with Device(host=jnpr_host, user=jnpr_user, password=jnpr_pass) as dev:
        res=dev.rpc.get_environment_information()

    #print(etree.tostring(res, encoding='unicode', pretty_print=True))

    ts = time.strftime("%Y-%m-%d %H:%M:%S")
    for t in res.findall("environment-item/temperature"):
        p_name = t.getparent().findtext("name")
        p_temp = t.get("celsius")
        if DEBUG:        
            print(ts + " | " + p_name + ': ' + p_temp)

        p = influxdb_client.Point("juniper_temps").tag("name", p_name).field("temperature", float(p_temp))
        write_api.write(bucket=influxdb_bucket, org=influxdb_org, record=p)

    time.sleep(sleep_time_secs)


