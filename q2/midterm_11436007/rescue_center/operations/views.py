from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.db.models import Q, Count
from django.shortcuts import render

from .models import Incident, ResourceRequest, ActionLog

User = get_user_model()

GUIDE_DATA = {
    '火災應變': {
        '初期通報': ['確認火源位置', '通知指揮中心', '開啟避難廣播'],
        '人員疏散': ['引導至安全出口', '協助行動不便者', '清點人數'],
    },
    '水災應變': {
        '預警階段': ['備妥沙袋', '轉移低窪住戶', '聯繫避難所'],
        '撤離階段': ['確認人員名單', '安排交通接送', '關閉電源'],
    },
    '醫療緊急': {
        '現場處置': ['評估傷患狀況', '施行急救', '呼叫救護車'],
        '後送流程': ['通報醫院', '填寫傷患資料', '跟進送醫結果'],
    },
}


class IncidentListView(ListView):
    model = Incident
    template_name = 'home.html'
    context_object_name = 'incidents'
    ordering = ['-created_at']


class IncidentDetailView(DetailView):
    model = Incident
    template_name = 'incident_detail.html'
    context_object_name = 'incident'


class IncidentCreateView(CreateView):
    model = Incident
    template_name = 'incident_new.html'
    fields = ['title', 'category', 'priority', 'location', 'description', 'reporter', 'is_active']


class IncidentUpdateView(UpdateView):
    model = Incident
    template_name = 'incident_edit.html'
    fields = ['category', 'priority', 'location', 'description', 'is_active']


class IncidentDeleteView(DeleteView):
    model = Incident
    template_name = 'incident_delete.html'
    success_url = reverse_lazy('home')


class GuideView(TemplateView):
    template_name = 'guide.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['guide_data'] = GUIDE_DATA
        return context


def responders_view(request):
    users = User.objects.filter(is_staff=False, is_superuser=False, is_active=True)
    return render(request, 'responders.html', {'users': users, 'total': users.count()})


def stats_view(request):
    incidents = Incident.objects.all()
    incident_stats = incidents.annotate(
        rr_count=Count('resource_requests', distinct=True),
        al_count=Count('action_logs', distinct=True),
    )
    context = {
        'incident_total': incidents.count(),
        'incident_active': incidents.filter(is_active=True).count(),
        'incident_closed': incidents.filter(is_active=False).count(),
        'resource_total': ResourceRequest.objects.count(),
        'resource_urgent': ResourceRequest.objects.filter(is_urgent=True).count(),
        'actionlog_total': ActionLog.objects.count(),
        'user_total': User.objects.filter(is_staff=False, is_superuser=False).count(),
        'incident_stats': incident_stats,
    }
    return render(request, 'stats.html', context)


def incident_search_view(request):
    qs = Incident.objects.all()
    q = request.GET.get('q', '').strip()
    category = request.GET.get('category', '')
    priority = request.GET.get('priority', '')
    is_active = request.GET.get('is_active', '')
    reporter = request.GET.get('reporter', '').strip()
    rr_status = request.GET.get('rr_status', '')
    rr_urgent = request.GET.get('rr_urgent', '')
    al_note = request.GET.get('al_note', '').strip()

    if q:
        qs = qs.filter(
            Q(title__icontains=q) |
            Q(location__icontains=q) |
            Q(description__icontains=q)
        )
    if category:
        qs = qs.filter(category=category)
    if priority:
        qs = qs.filter(priority=priority)
    if is_active != '':
        qs = qs.filter(is_active=(is_active == 'true'))
    if reporter:
        qs = qs.filter(
            Q(reporter__id=reporter) if reporter.isdigit() else Q(reporter__username__icontains=reporter)
        )
    if rr_status:
        qs = qs.filter(resource_requests__status=rr_status).distinct()
    if rr_urgent:
        qs = qs.filter(resource_requests__is_urgent=(rr_urgent == 'true')).distinct()
    if al_note:
        qs = qs.filter(action_logs__note__icontains=al_note).distinct()

    qs = qs.distinct()

    context = {
        'incidents': qs,
        'count': qs.count(),
        'q': q,
        'category': category,
        'priority': priority,
        'is_active': is_active,
        'reporter': reporter,
        'rr_status': rr_status,
        'rr_urgent': rr_urgent,
        'al_note': al_note,
    }
    return render(request, 'incident_search.html', context)
