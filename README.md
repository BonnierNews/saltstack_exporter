# Saltstack Exporter for Prometheus
This exporter allows scraping of data from a Saltstack minion.
The exporter must run on a minion, and have permission to execute commands locally.

To install and run:

```shell
pip install saltstack_exporter
saltstack_exporter
```

The direct invocation works since `pip` installs a wrapper executable script.
If this does not work on your platform, call python directly on `exporter.py`
in the `site_packages` directory. For example, on Linux with Python 2.7:

```shell
python /usr/lib/python2.7/site-packages/saltstack_exporter/exporter.py
```

# Configuration
Below are the available flags:

```shell
usage: exporter.py [-h] [--listen-addr LISTEN_ADDR] [--listen-port LISTEN_PORT]
                   [--highstate-interval HIGHSTATE_INTERVAL]
                   [--log-level LOG_LEVEL]

optional arguments:
  -h, --help            show this help message and exit
  --listen-addr LISTEN_ADDR
                        address to bind to (default: 0.0.0.0)
  --listen-port LISTEN_PORT
                        port to bind to (default: 9175)
  --highstate-interval HIGHSTATE_INTERVAL
                        interval between highstate test runs (default: 300)
  --log-level LOG_LEVEL
                        log level (default: WARN)
```

# Metrics
Currently, the exporter exposes metrics for highstate conformity only:

