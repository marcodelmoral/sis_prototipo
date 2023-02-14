from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test


# todo poner los otros decoradores
def epidemiologo_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='geo:geo_home'):
    '''
    Decorator for views that checks that the logged in user is a student,
    redirects to the log-in page if necessary.
    '''
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.tipo_usuario == 1,
        login_url=login_url,

    )
    if function:
        return actual_decorator(function)
    return actual_decorator
