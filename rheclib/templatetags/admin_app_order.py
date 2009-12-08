from django.conf import settings
from django import template

register = template.Library()

def reorder_admin_apps(app_list):
    """
    This will reorder the apps in the admin using weights defined in the RHEC_ADMIN_APP_WEIGHTS dict.
    The names, unfortunately, must be the verbose names displayed in the admin, not the actual app name, 
    because that is what is in the admin app_list var.
    The app_list argument object is modified, it does not return a value.
    Usage: Define your app weights in settings.py like so:
    RHEC_ADMIN_APP_WEIGHTS = {'Sites': 1,
                              'Auth' : 2}
    Override the default admin index.html template and insert the following before the app_list is rendered:
    {% load admin_app_order %}{% reorder_admin_apps app_list %}
    """
    weights = getattr(settings, 'RHEC_ADMIN_APP_WEIGHTS', {})
    for app_dict in app_list:
        app_dict['rhec_sort_weight'] = weights.get(app_dict['name'], 999)
    app_list.sort(lambda x, y: cmp(x['rhec_sort_weight'], y['rhec_sort_weight']))
    return ''
    
register.simple_tag(reorder_admin_apps)