from django.utils import timezone
from django.utils.crypto import get_random_string


def upload_to(instance, filename):
    ext = str(filename).split(".")[-1]
    date_now = timezone.now().strftime("%Y-%m-%d")
    filename = "{0}.{1}".format(get_random_string(64), ext)
    return '{0}/{1}'.format(date_now, filename)


def now():
    return timezone.now()
