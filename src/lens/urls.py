from django.urls import re_path
from .views import (
    TypeListView,
    TypeCreateView,
    StockListView,
    SearchStockListView,
    EntryListView,
    EntryCreateView,
    ExitListView,
    ExitCreateView,
    ProductListView,
    ProductCreateView,

)

app_name = 'lens'

urlpatterns = [
    re_path(r'^stock/$', StockListView.as_view(), name='stock'),
    re_path(r'^search/(?P<slug>\w+)/$', SearchStockListView.as_view(), name='search'),
    re_path(r'^types/$', TypeListView.as_view(), name='types-list'),
    re_path(r'^types/create/$', TypeCreateView.as_view(), name='types-create'),
    re_path(r'^entries/$', EntryListView.as_view(), name='entry-list'),
    re_path(r'^entries/create/$', EntryCreateView.as_view(), name='entry-create'),
    re_path(r'^exits/$', ExitListView.as_view(), name='exit-list'),
    re_path(r'^exits/create/$', ExitCreateView.as_view(), name='exit-create'),
    re_path(r'^products/$', ProductListView.as_view(), name='product-list'),
    re_path(r'^products/create/$', ProductCreateView.as_view(), name='product-create'),
]
