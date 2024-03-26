import time

from google.api_core.exceptions import ResourceExhausted


def safe_google_request(request_function, sleep_time=5):
    def wrapper(*args, **kwargs):
        try:
            response = request_function(*args, **kwargs)
        except ResourceExhausted:
            time.sleep(sleep_time)
            response = request_function(*args, **kwargs)

        return response

    return wrapper
