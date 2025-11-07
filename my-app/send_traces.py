import time
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.resources import Resource
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter

# --- Configuration ---
# Set the service name for your application
resource = Resource(attributes={
    "service.name": "demo-service"
})

# Set up the OTLP exporter to send traces to Tempo
otlp_exporter = OTLPSpanExporter(endpoint="localhost:4317", insecure=True)

# Set up the trace provider and processor
provider = TracerProvider(resource=resource)
processor = BatchSpanProcessor(otlp_exporter)
provider.add_span_processor(processor)
trace.set_tracer_provider(provider)

# Get a tracer for your application
tracer = trace.get_tracer("demo_app_tracer")

# --- Create and Send a Trace ---
print("Sending a trace to Tempo...")
with tracer.start_as_current_span("main-operation") as parent_span:
    parent_span.set_attribute("app.version", "1.0")
    print(f"Trace ID: {parent_span.get_span_context().trace_id}")

    with tracer.start_as_current_span("child-task") as child_span:
        time.sleep(0.1)
        child_span.set_attribute("task.status", "complete")

print("Trace sent successfully!")

# Wait for the exporter to send the data
time.sleep(2) 
