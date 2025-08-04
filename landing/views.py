from django.shortcuts import render

# Create your views here.

from django.shortcuts import render, redirect
from .forms import FormulaireForm

def home(request):
    if request.method == 'POST':
        form = FormulaireForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')  # back to the landing page (or a “thank you” page)
    else:
        form = FormulaireForm()

    return render(request, 'landing/home.html', {'form': form})