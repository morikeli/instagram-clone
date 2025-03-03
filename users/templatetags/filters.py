from django.utils.timesince import timesince
from django import template


register = template.Library()


@register.filter(name='post_timesince')
def custom_timesince_filter(value):
    """ 
        This is function returns the value of time elapsed since a post was uploaded on his/her News Feed. If the time elsapsed is in: 
            - minutes, return 'm',
            - hours, return 'h', 
            - days, return 'd',
            - weeks, return 'w',
        
        If all the above conditions are false, i.e. time past is less than a minute, then return 'Just now'.
    """
    
    time_diff = timesince(value)   # time difference
    (time_diff := time_diff.split(',')[0])  # split time and access the first value.
    
    if 'minute' in time_diff:
        if int(time_diff[:1]) == 0:
            time_elapsed = f"Just now"
            return time_elapsed
        
        elif int(time_diff[:2]) > 1:
            time_elapsed = f"{time_diff[:2]}mins"     # get the first 2 items in the str. value
        
        else:
            time_elapsed = f"{time_diff[:2]}min"
        
        return time_elapsed
    
    elif 'hour' in time_diff:
        time_elapsed = f"{time_diff[:2]}h"     # return e.g. 2 h, 3 h -> 2hours, 3 hours
        return time_elapsed
    
    elif 'day' in time_diff:
        time_elapsed = f"{time_diff[:2]}d"
        return time_elapsed
    
    elif 'week' in time_diff:
        time_elapsed = f"{time_diff[:2]}w"
        return time_elapsed
    
    elif 'month' in time_diff:
        time_elapsed = f"{time_diff[:2]}mos"
        return time_elapsed
    
    elif 'year' in time_diff:
        time_elapsed = f"{time_diff[:2]}y"
        return time_elapsed


@register.filter(name='totalcount')
def get_total_count(value):
    """
        This filter is used to shorten the number of likes of a post or followers a user has. For example:
        - a post with `1,000,000`, `10,000,000`, `100,000,000` likes will be shortened to 1M, 10M or 100M
        - a user with `1,000,000` or `10,000,000` followers will be shortened to 1M or 10M
    """

    total_count = int(value)

    if total_count >= 1_000_000:
        views = round((total_count) / 1_000_000, 1)
        return f'{views}M'
    
    elif total_count >= 10_000_000:
        views = round((total_count) / 1_000_000, 1)
        return f'{views}M'
    
    elif total_count >= 100_000_000:
        views = round((total_count) / 100_000_000, 1)
    
    else:
        return total_count

