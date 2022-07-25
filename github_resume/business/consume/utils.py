from datetime import datetime

from github_resume.business.consume.const import DATE_FIELDS


def _normalize_datetime_fields(data: dict):
    for k, v in data.items():
        if k in DATE_FIELDS:
            data[k] = datetime.strftime(
                datetime.strptime(v, '%Y-%m-%dT%H:%M:%SZ'), '%Y/%m/%d'
            )


def normalize_response_datetime(response: list or dict):
    if isinstance(response, list):
        for each in response:
            _normalize_datetime_fields(each)
    else:
        _normalize_datetime_fields(response)
    return response
