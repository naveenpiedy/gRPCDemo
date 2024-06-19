# Created by NaveenPiedy at 6/19/2024 6:40 AM
import grpc
import logging


class LoggingInterceptor(grpc.ServerInterceptor):
    def intercept_service(self, continuation, handler_call_details):
        method_name = handler_call_details.method
        metadata = dict(handler_call_details.invocation_metadata)
        trace_id = metadata.get('trace-id', 'unknown')
        logging.info(f"Trace ID: {trace_id} - Invoking method: {method_name}")

        # Call the actual RPC method
        response = continuation(handler_call_details)

        logging.info(f"Trace ID: {trace_id} - Completed method: {method_name}")
        return response