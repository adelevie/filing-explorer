from django.shortcuts import render, get_object_or_404

from filings.models import Filing

def index(request):
    filings = Filing.objects.all()
    context = {
        'filings': filings
    }
    return render(request, 'filings/index.html', context)

def detail(request, filing_id):
    filing = get_object_or_404(Filing, pk=int(filing_id))
    context = {
        'filing': filing
    }
    return render(request, 'filings/detail.html', context)
