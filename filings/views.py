from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from filings.models import Filing
from filings.template_models import FilingTemplateModel

def index(request):
    filings = Filing.objects.all().order_by('date_submitted')
    filings_list = []
    for filing in filings:
        filing_template_model = FilingTemplateModel(filing)
        filings_list.append(filing_template_model)

    filings_count = len(filings)

    paginator = Paginator(filings_list, 25)

    page = request.GET.get('page')
    try:
        paginated_filings_list = paginator.page(page)
    except PageNotAnInteger:
        paginated_filings_list = paginator.page(1)
    except EmptyPage:
        paginated_filings_list = paginator.page(paginator.num_pages)

    context = {
        'filings': paginated_filings_list,
        'filings_count': filings_count
    }
    return render(request, 'filings/index.html', context)

def detail(request, filing_id):
    filing_model = get_object_or_404(Filing, pk=int(filing_id))
    filing = FilingTemplateModel(filing_model)
    context = {
        'filing': filing
    }
    return render(request, 'filings/detail.html', context)
