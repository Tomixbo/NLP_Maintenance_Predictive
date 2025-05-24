from django.contrib import admin
from .models import Report

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('id', 'created', 'author', 'device', 'fixed', 'score_display')
    list_filter = ('fixed', 'device')
    search_fields = ('author', 'device', 'text')
    ordering = ('-created',)

    @admin.display(description='Score de criticité')
    def score_display(self, obj):
        return f"{obj.score:.2f}" if obj.score is not None else "—"
