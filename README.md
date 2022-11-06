Log temperatures from Juniper EX2200 switch.

create bucket, and token in InfluxDB:
-------------------------------------
login via e.g. http://influxdb_host:8086
add via GUI

create python venv environment:
-------------------------------
$ git clone <<url>>
$ cd jtempmon
$ python3 -m venv venv
$ source venv/bin/activate
$ python3 -m pip install --upgrade pip
$ python3 -m pip install -r requirements.txt

Update config to juniper device, and influxdb:
$ vim jtempmon.py

Copy to release dir (separate release from development version)
$ cp jtempmon.py release

systemd service:
------------------
Update paths to python venv
$ vim jtempmon.service 

Copy and install service
$ sudo cp jtempmon.service /etc/systemd/system
$ sudo systemctl daemon-reload
$ sudo systemctl enable jtempmon.service 

Start service
$ sudo systemctl start jtempmon.service
