import logging
from fluent import handler

def LogsInstrumentor(service_name, fluent_endpoint="24224"):
    custom_format = {
    'host': '%(hostname)s',
    'where': '%(module)s.%(funcName)s',
    'type': '%(levelname)s',
    'stack_trace': '%(exc_text)s'
    }

    logging.basicConfig(level=logging.INFO)   
    h = handler.FluentHandler(service_name, host='host', port=fluent_endpoint)
    formatter = handler.FluentRecordFormatter(custom_format)
    h.setFormatter(formatter)
    return  h