'''
Mapping urls for `profiles` Django web app.
'''


from django.urls import path

from profiles import views


app_name = 'profiles'
urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('tedsearchterm/', views.TedSearchTermListView.as_view(), name='tedsearchterm-list'),
    path('tedsearchterm/add/', views.TedSearchTermCreateView.as_view(),
         name='tedsearchterm-create'),
    path('tedsearchterm/<int:pk>/delete/', views.TedSearchTermDeleteView.as_view(),
         name='tedsearchterm-delete'),
    path('tedsearchterm/<int:pk>/update/', views.ted_search_term_update,
         name='ted_search_term_update')
]
