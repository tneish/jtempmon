Log temperatures from a Juniper EX2200 switch, into influxdb.

Create bucket, and token in InfluxDB:
-------------------------------------
Login via e.g. `http://influxdb_host:8086`
Add via GUI..

Create python venv environment:
-------------------------------
```
$ git clone https://github.com/tneish/jtempmon.git
$ cd jtempmon
$ python3 -m venv venv
$ source venv/bin/activate
$ python3 -m pip install --upgrade pip
$ python3 -m pip install -r requirements.txt
```

Update Login Details
--------------------
Use your favourite [KeePass db editor](https://keepass.info) to update URLs, IP addresses, usernames, passwords, influxdb token, etc in the keepass database file, `db.kdbx`.

Copy to release dir (separate release from development version)
---------------------------------------------------------------
```
$ cp jtempmon.py db.kdbx release
```

systemd service:
------------------
To daemonize and start the script when your server starts, create a systemd service for jtempmon..

Update paths to python venv
```
$ vim jtempmon.service 
```

Copy and install service
```
$ sudo cp jtempmon.service /etc/systemd/system
$ sudo systemctl daemon-reload
$ sudo systemctl enable jtempmon.service 
```

Start service
```
$ sudo systemctl start jtempmon.service
```
