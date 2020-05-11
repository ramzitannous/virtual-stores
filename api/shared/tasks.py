from celery import Task, states
from celery.result import EagerResult
from shared.helpers import *
from requests.exceptions import Timeout, ConnectionError

class OnceTask(Task):

    @staticmethod
    def get_lock(name):
        return bool(int(get_value(name, 0)))

    @staticmethod
    def unlock(name):
        remove_value(name)

    @staticmethod
    def lock(timeout, name):
        put_value(name, 1, timeout)

    def apply_async(self, args=None, kwargs=None, task_id=None, producer=None, link=None, link_error=None, shadow=None,
                    **options):
        name = f"{self.name} - {str(tuple(args))} - {str(kwargs)}"
        if OnceTask.get_lock(name):
            print(f'{self.name} is already running')
            return EagerResult(None, None, states.REJECTED)

        else:
            timeout = self._get_app().conf.get('lock_timeout', 60 * 60)
            OnceTask.lock(timeout, name)
            print(f'{self.name} locked with timeout {timeout}')
            return super().apply_async(args, kwargs, task_id, producer, link, link_error, shadow, **options)

    def after_return(self, status, retval, task_id, args, kwargs, einfo):
        name = f"{self.name} - {str(tuple(args))} - {str(kwargs)}"
        OnceTask.unlock(name)
        print(f'{self.name} is unlocked')
        super().after_return(status, retval, task_id, args, kwargs, einfo)


class AutoRetryTask(Task):
    autoretry_for = (BrokenPipeError, ConnectionError, Timeout)
    retry_kwargs = {'max_retries': 5}
    default_retry_delay = 1 * 60

