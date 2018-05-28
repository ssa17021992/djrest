from base64 import urlsafe_b64encode as b64encode
from uuid import uuid4

from requests import request as _request
from django.conf import settings


def get_object_or_none(model, *args, **kwargs):
    """Get object or none"""
    try:
        obj = model.objects.get(*args, **kwargs)
    except model.DoesNotExist:
        obj = None
    return obj


def unique_id():
    """Generate unique id"""
    return b64encode(uuid4().bytes).decode()[:-2]


def to_object(data):
    """Data to object"""
    iterable = (list, tuple, set)
    if isinstance(data, iterable):
        return [to_object(i) for i in data]

    if not isinstance(data, dict):
        return data

    obj = type('Obj', (), {})()
    for k, v in data.items():
        setattr(obj, k, to_object(v))
    return obj


def request(method, url, **kwargs):
    """Make http request"""
    try:
        response = _request(method, url, **kwargs)
        response.status = response.status_code
    except Exception:
        response = to_object({})
        response.status = 500  # Internal server error
    return response


def send_notification(title, body, icon, data, to):
    """Send firebase push notification"""
    if not to: return

    return requests.post(settings.FCM_URL, headers={
        'Content-Type': 'application/json',
        'Authorization': 'Key=%s' % settings.FCM_TOKEN
    }, json={
        'registration_ids': to,
        'notification': {  # Max. 2KB.
            'title': title,
            'body': body,
            'icon': icon or settings.FCM_DEFAULT_ICON
        },
        'data': data  # Max. 4KB.
    })
