import json
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, reverse, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView, DeleteView
from accounts.models import User
from .forms import RepAddForm, SessionForm
from .models import Rep, Exercice, Session


# Create your views here.

from django.utils.decorators import method_decorator


@method_decorator(login_required, name='dispatch')
class SessionCreateView(CreateView):
    form_class = SessionForm
    template_name = 'create_rep.html'

    def form_valid(self, form):
        """ pre populating the user field to thee loggedin user"""
        newform = form.save(commit=False)
        newform.user = self.request.user
        newform.save()
        return HttpResponseRedirect(reverse_lazy('volume:session-list'))


@method_decorator(login_required, name='dispatch')
class SessionDetail(DetailView):
    model = Session
    template_name = 'session_detail.html'

    def get_context_data(self, **kwargs):
        context = super(SessionDetail, self).get_context_data(**kwargs)
        """ adding initial form data (prepopulating the session field"""
        set_form_data = {"session": self.object.id}
        exercices = Rep.objects.filter(session=self.object.id)
        context['set_form'] = RepAddForm(self.object.user, initial=set_form_data)
        context['exercices'] = serializers.serialize("json", exercices, indent=4,relations={'rep':{'relations':('exercice',)}})
        return context

    def get_musclegroup(self, mg):
        # musclegroup = Session.objects.get(id=self.request.id).rep_set.filter(exercice__primarymg__id=mg)
        self.object.rep_set.filter(exercice__primarymg__id=mg)
        return musclegroup

    def get_volume_by_musclegroup(get_musclegroup):
        volume = 0
        for rep in get_musclegroup:
            volume += (rep.weight * rep.repition)
        return volume

    # def get_total_volume(self, request, *args, **kwargs):
    #     session = request.session
    #     total_volume = []
    #     for item in session.rep_set.all():
    #         print(item)
    #         total_volume.append(item)
    #     return total_volume


@method_decorator(login_required, name='dispatch')
class SessionList(ListView):
    model = Session
    template_name = 'session_list.html'

    def get_queryset(self):
        """ displaying session corresponding only to the current user """
        qs = Session.objects.filter(user__id=self.request.user.id)
        return qs

    def get_context_data(self, **kwargs):
        context = super(SessionList, self).get_context_data(**kwargs)
        """adding the Session Form to Context"""
        context['newform'] = SessionForm()
        return context


@login_required
def new_rep(request):
    if request.method == 'POST':
        form = RepAddForm(request.user, request.POST)
        if form.is_valid():
            x = request.POST.get("session")
            form.save()
            return HttpResponseRedirect(reverse_lazy('volume:session_detail', args=[x]))
    else:
        form = RepAddForm(request.user)
    return render(request, 'create_rep.html', {'form': form})


class RepDeleteView(DeleteView):
    model = Rep
    template_name = 'rep_delete.html'
    success_url = reverse_lazy('volume:session-list')

    def delete(self, request, *args, **kwargs):
        self.get_object().delete()
        payload = {'delete': 'ok'}
        return HttpResponse(json.dumps(payload), content_type='application/json')


@method_decorator(login_required, name='dispatch')
class ExerciceCreateView(CreateView):
    model = Exercice
    fields = ['name', 'primarymg', 'secondarymg', 'image']
    template_name = 'create_exercice.html'
    success_url = '/'


@method_decorator(login_required, name='dispatch')
class ExerciceDetail(DetailView):
    model = Exercice
    template_name = 'session_detail.html'
