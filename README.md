# Saltstack Exporter for Prometheus
This exporter allows scraping of data from a Saltstack minion.
The exporter must run on a minion, and have permission to execute commands locally.

To install and run:

```shell
pip install prometheus_client
python exporter.py
```

# Configuration
Below are the available flags:

```shell
usage: exporter.py [-h] [--listen-addr LISTEN_ADDR]
                   [--listen-port LISTEN_PORT] [--log-level LOG_LEVEL]

optional arguments:
  -h, --help            show this help message and exit
  --listen-addr LISTEN_ADDR
                        address to bind to (default: 0.0.0.0)
  --listen-port LISTEN_PORT
                        port to bind to (default: 9175)
  --log-level LOG_LEVEL
                        log level (default: WARN)
```

