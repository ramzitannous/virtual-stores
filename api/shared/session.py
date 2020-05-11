from urllib3.util.retry import Retry
from django.conf import settings
from requests.adapters import HTTPAdapter
from requests.sessions import Session


class StoreSession(Session):
    def request(self, method, url, **kwargs):
        kwargs["timeout"] = kwargs.get(
            "timeout") or settings.REQUEST_DEFAULT_TIMEOUT
        return super().request(method, url, **kwargs)


def get_requests_session() -> StoreSession:
    session = StoreSession()

    retries = settings.REQUEST_DEFAULT_RETRIES
    backoff = settings.REQUEST_DEFAULT_BACKOFF

    methods = ["GET", "POST", "PUT", "PATCH"]

    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff,
        method_whitelist=frozenset(methods)
    )

    adapter = HTTPAdapter(max_retries=retry)

    session.mount('http://', adapter)
    session.mount('https://', adapter)

    return session
