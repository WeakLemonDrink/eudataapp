'''
Mapping urls for `tenders` Django web app.
'''


from django.urls import path

from tenders import views


app_name = 'tenders'
urlpatterns = [
    path('', views.index, name='index'),
    path('sign-s3/', views.sign_s3, name='sign-s3'),
    path('lot/', views.LotListView.as_view(), name='lot-list'),
    path('contractawardnotice/', views.ContractAwardNoticeListView.as_view(),
         name='contractawardnotice-list'),
    path('contractnotice/', views.ContractNoticeListView.as_view(), name='contractnotice-list'),
    path('contractnotice/<int:contractnotice_id>/edit-lot-units/',
         views.ContractNoticeEditLotUnitsView.as_view(), name='contractnotice-edit-lot-units'),
    path('tender/add/', views.TenderSingleCreateView.as_view(), name='tender-create'),
    path('tender/bulk-add/', views.TenderBulkCreateView.as_view(), name='tender-bulk-create')
]
