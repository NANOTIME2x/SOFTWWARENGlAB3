from django.shortcuts import render
from django.utils import timezone
from datetime import timedelta

def index(request):
    now = timezone.now()
    past_date = now - timedelta(days=3)
    future_date = now + timedelta(days=2)
    return render(request, 'myapp/index.html', {
        'now': now,
        'past_date': past_date,
        'future_date': future_date,
    })
