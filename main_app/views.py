from .models import Artist
from django.shortcuts import redirect
from django.views import View # handles requests
from django.http import HttpResponse # handles sending a type of response
from django.views.generic.base import TemplateView
# This will import the class we are extending 
from django.views.generic.edit import CreateView
from django.views.generic import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse
from .models import Artist, Song, Playlist

# Create your views here.

#here we will be creating a class called Home and extending it from the View class 
class Home(View):

    # Here we are adding a method that will be ran when we are dealing with a GET request
    def get(self, request):
        #here we are returning a generic response
        #this is similar to response.send() in express
        return HttpResponse("Spotify Home")

class About(View):

    def get(self, request):
        return HttpResponse("Spotify About")

class Home(TemplateView):
    template_name = "home.html"


class About(TemplateView):
    template_name = "about.html"


class ArtistList(TemplateView):
    template_name = "artist_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # to get the query parameter we have to acccess it in the request.GET dictionary object        
        name = self.request.GET.get("name")
        # If a query exists we will filter by name 
        if name != None:
            # .filter is the sql WHERE statement and name__icontains is doing a search for any name that contains the query param
            context["artists"] = Artist.objects.filter(name__icontains=name)
              # We add a header context that includes the search param
            context["header"] = f"Searching for '{name}'"
        else:
            context["artists"] = Artist.objects.all()# this is where we add the key into our context object for the view to use
             # default header for not searching 
            context["header"] = "Trending Artists"
        return context


class ArtistCreate(CreateView):
    model = Artist
    fields = ['name', 'img', 'bio', 'verified_artist']
    template_name = "artist_create.html"
    success_url = "/artists/"

class ArtistDetail(DetailView):
    model = Artist
    template_name = "artist_detail.html"

class ArtistUpdate(UpdateView):
    model = Artist
    fields = ['name', 'img', 'bio', 'verified_artist']
    template_name = "artist_update.html"
    success_url = "/artists/"

    def get_success_url(self):
        return reverse('artist_detail', kwargs={'pk': self.object.pk})#returns to artist page

class ArtistDelete(DeleteView):
    model = Artist
    template_name = "artist_delete_confirmation.html"
    success_url = "/artists/"

class SongCreate(View):
    def post(self, request, pk):
        title = request.POST.get("title")
        length = request.POST.get("length")
        artist = Artist.objects.get(pk=pk)
        Song.objects.create(title=title, length=length, artist=artist)
        return redirect('artist_detail', pk=pk)

class Home(TemplateView):
    template_name = "home.html"
    # Here we have added the playlists as context
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["playlists"] = Playlist.objects.all()
        return context

class PlaylistSongAssoc(View):

    def get(self, request, pk, song_pk):
        # get the query param from the url
        assoc = request.GET.get("assoc")
        if assoc == "remove":
            # get the playlist by the id and
            # remove from the join table the given song_id
            Playlist.objects.get(pk=pk).songs.remove(song_pk)
        if assoc == "add":
            # get the playlist by the id and
            # add to the join table the given song_id
            Playlist.objects.get(pk=pk).songs.add(song_pk)
        return redirect('home')

class ArtistDetail(DetailView):
    model = Artist
    template_name = "artist_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["playlists"] = Playlist.objects.all()
        return context
