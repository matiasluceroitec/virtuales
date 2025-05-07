from datetime import date, datetime

def get_time_data(request):
    return {
        'current_year': date.today().year,
        'current_date': date.today()
    }

