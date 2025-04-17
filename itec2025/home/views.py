from django.shortcuts import render

# Create your views here.
def register_view(request):
    return render(
        request=request,
        template_name='accounts/register.html'
    )