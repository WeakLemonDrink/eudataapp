'''
Mapping urls for `medicines` Django web app.
'''


from django.urls import path

from medicines import views


app_name = 'medicines'
urlpatterns = [
    path('', views.index, name='index'),
    path('bnf-presentation/', views.BNFPresentationListView.as_view(), name='bnfpresentation-list'),
    path('bnf-presentation/<str:code>/', views.BNFPresentationDetailView.as_view(),
         name='bnfpresentation-detail'),
    path('get-pricing-data/<str:code>/', views.get_pricing_data, name='get-pricing-data'),
]
