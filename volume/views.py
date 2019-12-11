from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, reverse, redirect
from django.views.generic import ListView, CreateView, DetailView, DeleteView
from accounts.models import User
from .models import Rep, Exercice, Session
from .forms import RepAddForm, SessionForm
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
# Create your views here.
from django.contrib.auth.decorators import login_required
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
        context['set_form'] = RepAddForm(self.object.user, initial=set_form_data)
        return context

    # def get_total_volume(self, request, *args, **kwargs):
    #     session = request.session
    #     total_volume = []
    #     for item in session.rep_set.all():
    #         print(item)
    #         total_volume.append(item)
    #     return total_volume


@method_decorator(login_required, name='dispatch')
class SessionList(LoginRequiredMixin, ListView):
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
