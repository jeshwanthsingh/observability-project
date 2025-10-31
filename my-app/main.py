import logging
from fastapi import FastAPI, Request, HTTPException, Response
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST

# --- OpenTelemetry (Tracing Only) ---
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- Prometheus Metrics Setup ---
REQUESTS = Counter("app_requests_total", "Total requests", ["endpoint"])
ERRORS = Counter("app_errors_total", "Total errors", ["endpoint"])

# --- Tracing Setup ---
resource = Resource.create(attributes={"service.name": "my-fastapi-app"})
tracer_provider = TracerProvider(resource=resource)
otlp_exporter = OTLPSpanExporter()
tracer_provider.add_span_processor(BatchSpanProcessor(otlp_exporter))
trace.set_tracer_provider(tracer_provider)
    
# --- FastAPI Application ---
app = FastAPI()
FastAPIInstrumentor.instrument_app(app) # Instrument for traces

@app.get("/")
async def root():
    REQUESTS.labels(endpoint="/").inc()
    logger.info("Root endpoint was called")
    return {"message": "Hello World"}

@app.get("/error")
async def error_endpoint():
    ERRORS.labels(endpoint="/error").inc()
    REQUESTS.labels(endpoint="/error").inc()
    logger.error("A simulated error occurred!")
    raise HTTPException(status_code=500, detail="Internal Server Error")

@app.get("/metrics")
async def metrics():
    return Response(media_type=CONTENT_TYPE_LATEST, content=generate_latest())
