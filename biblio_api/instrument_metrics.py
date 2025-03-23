from prometheus_client import make_asgi_app
import re
from starlette.routing import Mount
from prometheus_client import REGISTRY, Counter, Gauge, Histogram, Summary
from prometheus_client.openmetrics.exposition import (CONTENT_TYPE_LATEST,
                                                      generate_latest)

def MetricsInstrumentor(app, service_name='myproject'):
    metrics_app = make_asgi_app()
    route = Mount("/metrics", make_asgi_app())
    route.path_regex = re.compile('^/metrics(?P<path>.*)$')
    app.routes.append(route)