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
    url(r'^catalog/artists',views.ArtistListView.as_view(), name='artists'),
    url(r'^catalog/groups',views.GroupListView.as_view(), name='groups'),
    url(r'^catalog/songs',views.SongListView.as_view(), name='songs'),
    url(r'^catalog/artist/(?P<pk>\d+)$', views.ArtistDetailView.as_view(), name='artist-detail'),
    url(r'^catalog/group/(?P<pk>\d+)$', views.GroupDetailView.as_view(), name='group-detail'),
    url(r'^catalog/song/(?P<pk>\d+)$', views.SongDetailView.as_view(), name='song-detail'),
    url(r'^addcatalog/$', views.addcatalog, name='addcatalog'),
    url(r'^create/artist/', views.ArtistCreate.as_view(), name='artist-create'),
    url(r'^create/group/', views.GroupCreate.as_view(), name='group-create'),
    url(r'^create/song/', views.SongCreate.as_view(), name='song-create'),
    url(r'^update/artist/(?P<pk>\d+)$', views.ArtistUpdate.as_view(), name='artist-update'),
    url(r'^update/group/(?P<pk>\d+)$', views.GroupUpdate.as_view(), name='group-update'),
    url(r'^update/song/(?P<pk>\d+)$', views.SongUpdate.as_view(), name='song-update'),
    url(r'^delete/artist/(?P<pk>\d+)$', views.ArtistDelete.as_view(), name='artist-delete'),
    url(r'^delete/group/(?P<pk>\d+)$', views.GroupDelete.as_view(), name='group-delete'),
    url(r'^delete/song/(?P<pk>\d+)$', views.SongDelete.as_view(), name='song-delete'),
]
