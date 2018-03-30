from django.shortcuts import render
from .models import Artist, Genre, Language, Song, Group, WaitList, Actions, Blocus
import requests #needs pip install
import json
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.http import JsonResponse
import random
import os
from django.contrib.auth.decorators import login_required
from .forms import AddCatalogForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

def index(request):
    if(Blocus.objects.all().exists() and not request.user.is_authenticated):
        return render(
            request,
            'closed.html',
        )

    num_artist = Artist.objects.all().count()
    num_genre = Genre.objects.all().count()
    num_song = Song.objects.all().count()
    num_group = Group.objects.all().count()

    return render(
        request,
        'index.html',
        context={'num_artist':num_artist,'num_genre':num_genre,'num_song':num_song,'num_group':num_group},
    )


def search(request):
    if(Blocus.objects.all().exists() and not request.user.is_authenticated):
        return render(
            request,
            'closed.html',
        )
    return render(
        request,
        'search.html',
    )

@login_required
def manager(request):
    action = request.GET.get('action','')
    if(not action == ''):
        order = Actions(
                    name=action
                    )
        order.save()

    if( WaitList.objects.all().exists()):
        data = []
        waitlist = WaitList.objects.all()
        for item in waitlist:
            data.append(item.duration)
    else:
        data = []

    gate = request.GET.get('blocus','')
    if (not gate == ''):
        if (gate == 'open'):
            temp = Blocus.objects.all()
            temp.delete()
        else:
            temp = Blocus(
                        name='closed'
                        )
            temp.save()


    if(Blocus.objects.all().exists()):
        blocus = 'closed'
    else:
        blocus = 'open'

    return render(
        request,
        'manager.html',
        context={'data':data,'blocus':blocus},
    )


def update(request):
    if(Blocus.objects.all().exists() and not request.user.is_authenticated):
        return render(
            request,
            'closed.html',
        )

    if(Actions.objects.all().exists()):
        order = Actions.objects.latest('time')
        name = order.name
        order.delete()
        return JsonResponse({'string':name})
    else: return JsonResponse({'string':""})




def query(request,pk):
    if(Blocus.objects.all().exists() and not request.user.is_authenticated):
        return render(
            request,
            'closed.html',
        )
    pk = pk.strip()
    url = 'https://www.googleapis.com/youtube/v3/search'
    api_key = os.environ.get('YTPARTY_API_KEY','')
    call_param = {
        'key':api_key,
        'part':'snippet',
        'maxResults':'20',
        'q':pk,
        'type':'video',
        'videoEmbeddable':'true'
    }

    response = requests.get(url, params=call_param)
    data = response.json()
    return render(
        request,
        'query.html',
        context={'query':pk,'data':data},
    )



def display(request):
    action = request.GET.get('action','')
    if( not WaitList.objects.all().exists()):
            random_idx = random.randint(0, Song.objects.count() -1)
            random_obj = Song.objects.all()[random_idx]
            record = WaitList(
                        title="no_request",
                        img=random_obj.img,
                        ytid=random_obj.ytid,
                        duration=random_obj.duration
                        )
            record.save()


    if(action == 'next'):
            previous = WaitList.objects.earliest('time')
            previous.delete()
            if( not WaitList.objects.all().exists()):
                return render(
                    request,
                    'next.html',
                    context={'content':'no_request'},
                )

            else:
                song = WaitList.objects.earliest('time')
                return render(
                    request,
                    'next.html',
                    context={'content':song},
                )



    song = WaitList.objects.earliest('time')
    wait = WaitList.objects.all()[1:4]
    return render(
        request,
        'display.html',
        context={'song':song,'wait':wait},
    )


def choice(request):
    if(Blocus.objects.all().exists() and not request.user.is_authenticated):
        return render(
            request,
            'closed.html',
        )

    title = request.GET.get('title','')
    img = request.GET.get('img','')
    id = request.GET.get('id','')
    previous = request.GET.get('previous','')

    if (previous == 'query'):
        url = 'https://www.googleapis.com/youtube/v3/videos'
        api_key = os.environ.get('YTPARTY_API_KEY','')


        call_param = {
            'key':api_key,
            'part':'contentDetails',
            'id': id,
            }

        response = requests.get(url, params=call_param)
        data = response.json()
    else:
        data = request.GET.get('duration','')
    return render(
        request,
        'choice.html',
        context = {'title':title,'img':img,'id':id,'previous': previous,'data':data},
    )

def request(request):
    if(Blocus.objects.all().exists() and not request.user.is_authenticated):
        return render(
            request,
            'closed.html',
        )

    title = request.GET.get('title','')
    img = request.GET.get('img','')
    id = request.GET.get('id','')
    duration = request.GET.get('duration','')

    #user requests song change
    tag = request.GET.get('tag','')
    if (tag == "change"):
        oldrequest = WaitList.objects.get(requestid__exact=request.session['requestid'])
        oldrequest.title = title
        oldrequest.img = img
        oldrequest.ytid = id
        oldrequest.duration = duration
        oldrequest.save()
        return render(
            request,
            'request.html',
            context = {'title':title,'img':img,'id':id,'duration':duration},
        )

    #check if user has song in list already

    if(WaitList.objects.filter(requestid__exact=request.session.get('requestid','9ed5aaee-a7cd-4533-8ba3-2ff9d8e17b83')).exists() and not request.user.is_authenticated):
        oldrequest = WaitList.objects.get(requestid__exact=request.session['requestid'])
        return render(
            request,
            'change.html',
            context = {'title':title,'img':img,'id':id,'duration':duration,'oldrequest':oldrequest},
        )

    record = WaitList(
                title=title,
                img=img,
                ytid=id,
                duration=duration
                )
    request.session['requestid'] = record.requestid.hex
    record.save()
    return render(
        request,
        'request.html',
        context = {'title':title,'img':img,'id':id,'duration':duration},
    )


def playlist(request):
    if( WaitList.objects.all().exists()):
        data = WaitList.objects.all()
    else:
        data = ""

    deletion = request.GET.get('deletion','')
    if(not deletion == ''):
        remove = WaitList.objects.get(requestid__exact=deletion)
        remove.delete()

    return render(
        request,
        'playlist.html',
        context={'data':data},
    )

@login_required
def addcatalog(request):
    if request.method == 'POST':
        form = AddCatalogForm(request.POST)
        if form.is_valid():
            newsong = Song(
                        title=form.cleaned_data['title'],
                        ytid=form.cleaned_data['ytid'],
                        #artist=form.cleaned_data['artist'],
                        #group=form.cleaned_data['group'],
                        duration=form.cleaned_data['duration'],
                        img=form.cleaned_data['img'],
                        )
            newsong.save()

            return HttpResponseRedirect(reverse('songs') )

    else:
        title = request.GET.get('title','')
        img = request.GET.get('img','')
        ytid = request.GET.get('ytid','')
        duration = request.GET.get('duration','')

        form = AddCatalogForm(initial={'title': title,'img':img,'ytid':ytid,'duration':duration})

    return render(
        request,
        'addcatalog.html',
        {'form': form},
    )




class ArtistCreate(CreateView):
    model = Artist
    fields = '__all__'
    success_url = reverse_lazy('artists')

class ArtistUpdate(UpdateView):
    model = Artist
    fields = '__all__'
    success_url = reverse_lazy('artists')

class ArtistDelete(DeleteView):
    model = Artist
    success_url = reverse_lazy('artists')

class GroupCreate(CreateView):
    model = Group
    fields = '__all__'
    success_url = reverse_lazy('groups')

class GroupUpdate(UpdateView):
    model = Group
    fields = '__all__'
    success_url = reverse_lazy('groups')

class GroupDelete(DeleteView):
    model = Group
    success_url = reverse_lazy('groups')

class SongCreate(CreateView):
    model = Song
    exclude = ['genre','language']
    success_url = reverse_lazy('songs')

class SongUpdate(UpdateView):
    model = Song
    fields = ['title','ytid','artist','group','duration','img']
    success_url = reverse_lazy('songs')

class SongDelete(DeleteView):
    model = Song
    success_url = reverse_lazy('songs')

class ArtistListView(generic.ListView):
    model = Artist

class GroupListView(generic.ListView):
    model = Group

class SongListView(generic.ListView):
    model = Song

class ArtistDetailView(generic.DetailView):
    model = Artist

class GroupDetailView(generic.DetailView):
    model = Group

class SongDetailView(generic.DetailView):
    model = Song
