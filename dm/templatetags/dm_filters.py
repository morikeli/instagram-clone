from django.utils.timesince import timesince
from django import template


register = template.Library()


@register.filter(name='last_seen')
def last_login_timesince_filter(value):
    """ 
        This is function returns the value of time elapsed since a user was last seen on the website. If the time past is in: 
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
            time_elapsed = "Last seen recently"
            return time_elapsed
        
        elif int(time_diff[:2]) > 1:
            time_elapsed = f"Active {time_diff[:2]}mins ago"     # get the first 2 items in the str. value
        
        else:
            time_elapsed = f"Active"
        
        return time_elapsed
    
    elif 'hour' in time_diff:
        time_elapsed = f"Active {time_diff[:2]}h ago"     # return e.g. 2 h, 3 h -> 2hours, 3 hours
        return time_elapsed
    
    elif 'day' in time_diff:
        time_elapsed = f"Active {time_diff[:2]}d ago"
        return time_elapsed
    
    elif 'week' in time_diff:
        time_elapsed = f"Active {time_diff[:2]}w ago"
        return time_elapsed
    
    elif 'month' in time_diff:
        time_elapsed = f"Active {time_diff[:2]}m ago"
        return time_elapsed
    
    elif 'year' in time_diff:
        time_elapsed = f"Active {time_diff[:2]}y ago"
        return time_elapsed
