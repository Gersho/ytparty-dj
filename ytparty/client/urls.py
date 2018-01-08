from django.conf.urls import url
from . import views




urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^search/$', views.search, name='search'),
    url(r'^search/(?P<pk>.+)$', views.query, name='query'),
    url(r'^request/$', views.request, name='request'),
    url(r'^choice/$', views.choice, name='choice'),
    url(r'^manager/$', views.manager, name='manager'),
    url(r'^display/$', views.display, name='display'),
    url(r'^update/$', views.update, name='display-update'),
    url(r'^playlist/$', views.playlist, name='playlist'),
    # url(r'^catalog/genre',views.BookListView.as_view(), name='books'),
    url(r'^catalog/artists',views.ArtistListView.as_view(), name='artists'),
    url(r'^catalog/groups',views.GroupListView.as_view(), name='groups'),
    url(r'^catalog/songs',views.SongListView.as_view(), name='songs'),
    url(r'^catalog/artist/(?P<pk>\d+)$', views.ArtistDetailView.as_view(), name='artist-detail'),
    url(r'^catalog/group/(?P<pk>\d+)$', views.GroupDetailView.as_view(), name='group-detail'),
    url(r'^catalog/song/(?P<pk>\d+)$', views.SongDetailView.as_view(), name='song-detail'),
]
