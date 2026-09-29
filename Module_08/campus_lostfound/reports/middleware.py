## Step 9 — Write `reports/middleware.py` (new file)

# Create 'middleware.py' inside the `reports/` folder:

import time
import logging

logger = logging.getLogger('reports.request_logger')


class RequestLogMiddleware:
    """
    Custom middleware that logs, for every request:
      - User (username or 'Anonymous')
      - Request Method (GET, POST, etc.)
      - URL/Path
      - Time taken to process the request (seconds)

    Example terminal output:
      User: Rahim | Method: POST | Path: /reports/create/ | Time: 0.08s
    """

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

        # Print to terminal (console) as requested, and also log it properly.
        print(log_message)
        logger.info(log_message)

        return response


"""
How middleware actually works:
------------------------------
- Django creates *one instance* of this class when the server starts (that's `__init__`, which just stores a reference to "the next thing in the chain," `get_response`). Then, for **every single request**, Django calls `__call__(request)`.

- Anything written **before** `response = self.get_response(request)` runs *before* your view function executes.

- `self.get_response(request)` is the line that actually triggers the URL routing → view → template process.

- Anything written **after** that line runs *after* the view has produced its response, but before it's sent to the browser.

That's why we start the timer before `get_response` and read it after — we're measuring exactly how long the view took. You already registered this class in `settings.py`'s `MIDDLEWARE` list back in Step 5, so it's already wired in — you don't call it manually anywhere.


"""