"""
Observability module for tracing, metrics, and LLM monitoring.
"""

import asyncio
import functools
import logging
import time
import os
import uuid
from typing import Any, Callable, Dict, List, Optional, TypeVar, cast

import httpx
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.semconv.resource import ResourceAttributes

from langchain.callbacks.base import BaseCallbackHandler

from ..config.settings import settings

# Configure logging
logger = logging.getLogger(__name__)

# Set up OpenTelemetry tracing
resource = Resource(attributes={
    ResourceAttributes.SERVICE_NAME: "likeminds-integration-agent",
    ResourceAttributes.SERVICE_VERSION: "0.1.0",
    ResourceAttributes.DEPLOYMENT_ENVIRONMENT: settings.ENVIRONMENT,
})

tracer_provider = TracerProvider(resource=resource)
tracer_provider.add_span_processor(BatchSpanProcessor(ConsoleSpanExporter()))
trace.set_tracer_provider(tracer_provider)
tracer = trace.get_tracer(__name__)


# Function decorator for tracing
F = TypeVar("F", bound=Callable[..., Any])

def trace(span_name: str) -> Callable[[F], F]:
    """
    Decorator to add OpenTelemetry tracing to a function.
    
    Args:
        span_name: Name of the span to create
        
    Returns:
        Decorated function
    """
    def decorator(func: F) -> F:
        @functools.wraps(func)
        async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
            with tracer.start_as_current_span(span_name) as span:
                start_time = time.time()
                try:
                    result = await func(*args, **kwargs)
                    span.set_attribute("status", "success")
                    return result
                except Exception as e:
                    span.set_attribute("status", "error")
                    span.set_attribute("error.type", e.__class__.__name__)
                    span.set_attribute("error.message", str(e))
                    raise
                finally:
                    span.set_attribute("duration_ms", (time.time() - start_time) * 1000)
                    
        @functools.wraps(func)
        def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
            with tracer.start_as_current_span(span_name) as span:
                start_time = time.time()
                try:
                    result = func(*args, **kwargs)
                    span.set_attribute("status", "success")
                    return result
                except Exception as e:
                    span.set_attribute("status", "error")
                    span.set_attribute("error.type", e.__class__.__name__)
                    span.set_attribute("error.message", str(e))
                    raise
                finally:
                    span.set_attribute("duration_ms", (time.time() - start_time) * 1000)
        
        if asyncio.iscoroutinefunction(func):
            return cast(F, async_wrapper)
        return cast(F, sync_wrapper)
    
    return decorator


# LLM monitoring
class HeliconeCallback(BaseCallbackHandler):
    """Callback handler for logging to Helicone."""
    
    def __init__(self, api_key: str, base_url: str):
        """Initialize with Helicone API key and base URL."""
        self.api_key = api_key
        self.base_url = base_url
        self.client = httpx.AsyncClient(
            headers={"Authorization": f"Bearer {api_key}"}
        )
        self.current_runs: Dict[str, Dict[str, Any]] = {}
    
    async def on_llm_start(self, serialized: Dict[str, Any], prompts: List[str], **kwargs) -> str:
        """Called when LLM starts generating."""
        run_id = str(uuid.uuid4())
        self.current_runs[run_id] = {
            "start_time": time.time(),
            "prompts": prompts,
            "model": serialized.get("name", "unknown")
        }
        return run_id
    
    async def on_llm_end(self, response, run_id, **kwargs):
        """Called when LLM finishes generating."""
        if run_id in self.current_runs:
            run_data = self.current_runs.pop(run_id)
            end_time = time.time()
            
            # Send data to Helicone
            await self.client.post(
                f"{self.base_url}/v1/log",
                json={
                    "model": run_data["model"],
                    "prompts": run_data["prompts"],
                    "completion": response.generations[0][0].text,
                    "latency_ms": int((end_time - run_data["start_time"]) * 1000),
                    "metadata": kwargs.get("metadata", {})
                }
            )


# Monitoring functions
class MonitoringService:
    """Service for monitoring and tracing."""
    
    def get_helicone_callback(self) -> Optional[BaseCallbackHandler]:
        """Get a configured Helicone callback instance."""
        if settings.HELICONE_API_KEY:
            return HeliconeCallback(
                api_key=settings.HELICONE_API_KEY,
                base_url=settings.HELICONE_BASE_URL
            )
        return None
    
    def record_exception(self, exception: Exception) -> None:
        """Record an exception for monitoring."""
        logger.exception(f"Exception occurred: {str(exception)}")
        # In a production system, you might send this to an error tracking service
        # like Sentry or New Relic


# Create a monitoring service instance
monitor = MonitoringService() 