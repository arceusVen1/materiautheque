from django.shortcuts import render
from materiaux.models import Materiau

# Create your views here.
def home(request):
    last_matx = Materiau.objects.order_by('date')[:5]
    return render(request, 'materiautheque/homepage.html', {'last_matx': last_matx})