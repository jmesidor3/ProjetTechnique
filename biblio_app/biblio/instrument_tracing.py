from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry import trace
from opentelemetry.sdk.resources import Resource


def TracesInstrumentor(app, service_name, otlp_endpoint="localhost:4317", excluded_urls=""):
    resource = Resource.create(attributes={"service.name": service_name})
    tracer = TracerProvider(resource=resource)
    trace.set_tracer_provider(tracer)

    # trace_processor = BatchSpanProcessor(ConsoleSpanExporter())
    trace_processor = BatchSpanProcessor(
        OTLPSpanExporter(endpoint=otlp_endpoint, insecure=True)
    )
    tracer.add_span_processor(trace_processor)

     # instrument
    FlaskInstrumentor().instrument( tracer_provider=tracer, enable_commenter=True, commenter_options={})
    return tracer