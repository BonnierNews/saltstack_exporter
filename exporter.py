import argparse
import logging
import sys
from salt import client
from tornado import web, ioloop
from prometheus_client import generate_latest
from prometheus_client import CONTENT_TYPE_LATEST
from prometheus_client.core import GaugeMetricFamily
from prometheus_client.core import CounterMetricFamily
from prometheus_client.core import REGISTRY


parser = argparse.ArgumentParser()
parser.add_argument(
    '--listen-addr',
    help='address to bind to (default: 0.0.0.0)',
    default=''
)
parser.add_argument(
    '--listen-port',
    type=int,
    help='port to bind to (default: 9175)',
    default='9175'
)
parser.add_argument(
    '--log-level',
    help='log level (default: WARN)',
    default=logging.WARN
)
args = parser.parse_args()


class SaltHighstateCollector(object):
    def __init__(self, caller):
        self.caller = caller
        self.states_total = lambda sample: GaugeMetricFamily(
            'saltstack_states_total',
            'Number of states which apply to the minion in highstate',
            value=sample
        )
        self.states_nonhigh = lambda sample: GaugeMetricFamily(
            'saltstack_nonhigh_states',
            'Number of states which would change on state.highstate',
            value=sample
        )
        self.states_error = lambda sample: GaugeMetricFamily(
            'saltstack_error_states',
            'Number of states which returns an error on highstate dry-run',
            value=sample
        )

    def describe(self):
        # Running highstate on startup can be slow, so we describe instead
        yield self.states_total(None)
        yield self.states_nonhigh(None)
        yield self.states_error(None)

    def collect(self):
        statedata = self.caller.cmd('state.highstate', test=True)
        success = isinstance(statedata, dict)

        if not success:
            return

        yield self.states_total(len(statedata))

        nonhigh = filter(
            lambda (id, state): state['result'] is None,
            statedata.iteritems()
        )
        yield self.states_nonhigh(len(nonhigh))

        error = filter(
            lambda (id, state): state['result'] is False,
            statedata.iteritems()
        )
        yield self.states_error(len(error))


class RootHandler(web.RequestHandler):
    def get(self):
        self.set_status(200)
        self.write(
            '<h1>Saltstack Collector</h1>'
            '<a href="/metrics">Metrics</a>'
        )


class HealthcheckHandler(web.RequestHandler):
    def get(self):
        self.write('OK')

    def head(self):
        self.set_status(200)


# This is a tornado-adapted handled from prometheus_client.MetricsHandler
class MetricsHandler(web.RequestHandler):
    def get(self):
        try:
            output = generate_latest(REGISTRY)
        except:
            self.set_status(500, 'error generating metric output')
            raise
        self.set_status(200)
        self.set_header('Content-Type', CONTENT_TYPE_LATEST)
        self.write(output)


def init_logging():
    loggers = ['tornado.access', 'tornado.application', 'tornado.general']
    for logger_name in loggers:
        logger = logging.getLogger(logger_name)
        logger.propagate = False
        logger.setLevel(args.log_level)
        stdout_handler = logging.StreamHandler(sys.stdout)
        logger.addHandler(stdout_handler)

if __name__ == '__main__':
    caller = client.Caller()
    REGISTRY.register(SaltHighstateCollector(caller))

    init_logging()

    app = web.Application([
        (r'/', RootHandler),
        (r'/healthcheck', HealthcheckHandler),
        (r'/metrics', MetricsHandler)
    ])
    app.listen(args.listen_port, args.listen_addr)

    print 'Serving metrics on {}:{}'.format(args.listen_addr, args.listen_port)
    ioloop.IOLoop.current().start()
