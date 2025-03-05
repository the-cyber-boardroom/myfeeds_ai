from datetime import datetime, timezone


def path_to__date_time(path):
    try:
        date_format = '%Y/%m/%d/%H'                         # Format corresponding to yyyy/mm/dd/hh
        date_time   = datetime.strptime(path, date_format)  # Convert to datetime object
        date_time   = date_time.replace(tzinfo=timezone.utc)
        return date_time
    except Exception:
        return None