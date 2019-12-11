from django.urls import path
from volume.views import ExerciceCreateView, SessionDetail, SessionList, SessionCreateView, new_rep, RepDeleteView

app_name = 'volume'

urlpatterns = [
    path('', SessionList.as_view(), name="session-list"),
    path('reps/delete/<int:pk>', RepDeleteView.as_view(), name="rep-delete"),
    # path('reps/add/', RepCreateView.as_view(), name="add-set"),
    path('reps/add/', new_rep, name="add-set"),
    path('exercice/create/', ExerciceCreateView.as_view(), name="exercice_create"),
    path('session/detail/<int:pk>', SessionDetail.as_view(), name="session_detail"),
    path('session/create/', SessionCreateView.as_view(), name="session_create"),
]
