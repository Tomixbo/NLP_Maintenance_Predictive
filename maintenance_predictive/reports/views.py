from django.shortcuts import render, redirect, get_object_or_404
from .models import Report
from .forms import ReportForm
from .ml.ml import predict_score 

def list_reports(request):
    # Récupère les params order_by et direction
    order_by  = request.GET.get('order_by', 'created')
    direction = request.GET.get('direction', 'desc')
    # Colonnes autorisées
    if order_by not in ('created','device','score'):
        order_by = 'created'
    # Préfixe pour desc vs asc
    prefix = '' if direction == 'asc' else '-'
    ordering = f"{prefix}{order_by}"
    # Sépare incidents en deux listes, ordonnées
    to_do = Report.objects.filter(fixed=False).order_by(ordering)
    done  = Report.objects.filter(fixed=True).order_by(ordering)
    return render(request, 'reports/list_report.html', {
        'to_do': to_do,
        'done':  done,
        'order_by':  order_by,
        'direction': direction,
    })


def create_report(request):
    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.score = predict_score(report.text)
            report.save()
            return redirect('reports:list_reports')
    else:
        form = ReportForm()
    return render(request, 'reports/create_report.html', {'form': form})

def report_detail(request, pk):
    report = get_object_or_404(Report, pk=pk)

    if request.method == 'POST' and request.POST.get('fix'):
        report.fixed = True
        report.save()
        return redirect('reports:list_reports')

    return render(request, 'reports/modal_detail.html', {'report': report})
