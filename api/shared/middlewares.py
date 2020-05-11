import uuid
import time

TRANSACTION_NAME = "X-TRANSACTION-ID"
PROCESSING_TIME = "X-PROCESSING-TIME"


class HeaderMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        init_time = time.time()
        response = self.get_response(request)
        trans_id = request.META.get(TRANSACTION_NAME)
        if trans_id is None:
            trans_id = uuid.uuid4().hex
        response[TRANSACTION_NAME] = trans_id
        response[PROCESSING_TIME] = time.time() - init_time
        return response
