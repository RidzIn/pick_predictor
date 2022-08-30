def winrate_format(value):
    value *= 100
    value = round(value, 0)
    return str(value) + '%'


def duration_in_sec_to_duration_in_minutes(value):
    minutes = int(value // 60)
    seconds = int(value % 60)
    return str(minutes) + ':' + str(seconds)


def duration_in_minutes_to_duration_in_seconds(value):
    index_to_slice = value.find(':')
    minutes = int(value[:index_to_slice])
    sec = int(value[-2:])
    return minutes * 60 + sec
