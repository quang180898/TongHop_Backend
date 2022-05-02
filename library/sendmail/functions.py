from concurrent.futures.thread import ThreadPoolExecutor
from django.core.mail import EmailMessage
from config.settings import EMAIL_HOST_STRING


class PoolHandle(object):
    class __PoolHandle:
        def __init__(self):
            self.val = None
            self.pool = ThreadPoolExecutor(15)

        def _submit(self, fn, par=None):
            if par is None:
                self.pool.submit(fn)
            else:
                self.pool.submit(fn, par)

        def submit(self, fn, par=None):
            try:
                self._submit(fn, par)
            except:
                pass

        def __str__(self):
            return self + self.val

    instance = None

    def __new__(cls):
        if not PoolHandle.instance:
            PoolHandle.instance = PoolHandle.__PoolHandle()
        return PoolHandle.instance

    def __getattr__(self, name):
        return getattr(self.instance, name)

    def __setattr__(self, name):
        return setattr(self.instance, name)


def send_mail(subject, msg_html, to_mail, cc_mail=None):
    msg = EmailMessage(subject=subject, body=msg_html, from_email=EMAIL_HOST_STRING, to=to_mail, cc=cc_mail)
    msg.content_subtype = "html"
    PoolHandle().submit(msg.send)
