import logging
import uuid
import sys

def get_logger(name: str):
    """
    Creates a centralized logger with standard formatting.
    """
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        
        # Standard console handler
        handler = logging.StreamHandler(sys.stdout)
        
        # Format include request_id (tracing)
        formatter = logging.Formatter(
            '[%(asctime)s] [%(levelname)s] [%(name)s] [TraceID: %(request_id)s] %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    
    return logger

class RequestTracingAdapter(logging.LoggerAdapter):
    """
    Logger adapter that injects a request_id into every log message.
    """
    def process(self, msg, kwargs):
        request_id = kwargs.pop('request_id', self.extra.get('request_id', 'N/A'))
        return f"{msg}", {**kwargs, 'extra': {'request_id': request_id}}

def get_tracing_logger(name: str, request_id: str = None):
    """
    Returns a logger adapter that includes a unique request_id for tracing.
    """
    base_logger = get_logger(name)
    rid = request_id or str(uuid.uuid4())[:8]
    return RequestTracingAdapter(base_logger, {'request_id': rid})
