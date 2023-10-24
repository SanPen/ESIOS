def time_diff_in_group(start_date, end_date, timegroup):
    """
    Calculate the difference between two datetime objects based on the specified time group.

    :param start_date: The start datetime object.
    :type start_date: datetime.datetime
    :param end_date: The end datetime object.
    :type end_date: datetime.datetime
    :param timegroup: The time group to calculate the difference in.
    :type timegroup: str
    :return: The difference between the two dates in the specified time group.
    :rtype: float
    """
    # Calculate the difference between the two dates
    diff = end_date - start_date

    # Convert the timedelta to the desired time group
    if timegroup == "minutes5":
        return diff.total_seconds() / 300
    elif timegroup == "minutes10":
        return diff.total_seconds() / 600
    elif timegroup == "minutes15":
        return diff.total_seconds() / 900
    elif timegroup == "hour":
        return diff.total_seconds() / 3600
    elif timegroup == "day":
        return diff.total_seconds() / 86400
    elif timegroup == "month":
        return diff.days / 30
    elif timegroup == "year":
        return diff.days / 365
    else:
        raise ValueError("Invalid time group")
