from datetime import date


def get_current_year(request):
    return {
        'current_year' : date.today().year
    }


def get_user_info(request):
    if request.user.is_authenticated:
        return {
            'username': request.user.username or None,
            'email': request.user.email or None
        }
    return {}
