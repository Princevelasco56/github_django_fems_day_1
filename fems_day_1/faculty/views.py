from django.shortcuts import render

# Create your views here.
def facultyreg(request):
    return render(request, 'faculty/facultyreg.html')