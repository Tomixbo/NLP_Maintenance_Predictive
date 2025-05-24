from django import forms
from .models import Report

class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['author', 'device', 'component', 'text', 'fixed']
        labels = {
            'author': 'Nom du rédacteur',
            'device': 'Nom du dispositif (ex. Éolienne Nord #2)',
            'component': 'Élément ou pièce concerné(e)',
            'text': 'Rapport d\'incident ou de maintenance',
            'fixed': 'Les pannes ont-elles été corrigées ?',
        }
