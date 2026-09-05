import time
import logging

logger = logging.getLogger('reports.request_logger')


class RequestLogMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.time()

        response = self.get_response(request)

        duration = time.time() - start_time
        user = request.user if request.user.is_authenticated else 'Anonymous'

        log_message = (
            f"User: {user} | Method: {request.method} | "
            f"Path: {request.path} | Time: {duration:.2f}s"
        )

        # Print to terminal (console) 
        print(log_message)
        logger.info(log_message)

        return response