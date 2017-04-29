from django.shortcuts import render, get_object_or_404

from filings.models import Filing
from filings.template_models import FilingTemplateModel

def index(request):
    filings = Filing.objects.all()
    filings_list = []
    for filing in filings:
        filing_template_model = FilingTemplateModel(filing)
        filings_list.append(filing_template_model)
    context = {
        'filings': filings_list
    }
    return render(request, 'filings/index.html', context)

def detail(request, filing_id):
    filing = get_object_or_404(Filing, pk=int(filing_id))
    context = {
        'filing': filing
    }
    return render(request, 'filings/detail.html', context)
