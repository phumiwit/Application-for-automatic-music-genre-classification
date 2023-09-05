

from django.core.files.storage import default_storage
from django.shortcuts import render,redirect
from django.http import JsonResponse, HttpResponse
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from key import Keyword_Spotting_Service
from django import forms
from django.conf import settings
from musicgenreapp.settings import BASE_DIR, MEDIA_ROOT
from myapp.models import User,Userdata,Valueforchart
from django.contrib.auth.models import User
from django.contrib import messages
from myapp.models import Audio,Collection,File
from django.contrib.auth.decorators import login_required
import os
import json
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import requests
from pylast import LastFMNetwork
import pylast
from pydub import AudioSegment
import ast
import subprocess
import time
from dotenv import load_dotenv

load_dotenv()



class MultipleFileUploadForm(forms.Form):
    audios  = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))



@login_required(login_url="userlogin")
def choosefile(request):
    if not request.user.is_authenticated:
        return redirect("userlogin")
    if request.method == 'POST':
        allowed_extensions = [".mp4", ".wav"]
        path_list = []
        for uploaded_file in request.FILES.getlist('audios'):
            filename = uploaded_file.name
            file_extension = os.path.splitext(filename)[1].lower()
            if file_extension not in allowed_extensions:
                messages.error(request, "Error: Only .mp4 and .wav files are allowed.")
                return redirect('/choosefile')
            save_path = default_storage.save(filename, uploaded_file)
            file_url = default_storage.url(save_path)
            path_list.append(save_path)
            user = User.objects.get(username=request.user)
            file = File.objects.create(UserName=user, FileName=filename, FileUrl=file_url)
            file.save()

        request.session['path_list'] = path_list
        return redirect('/predictfile')
    else:
        return render(request, 'choosefile.html', {'form': MultipleFileUploadForm()})


def showchoosefile(request):
    path_list = request.session.get('path_list')
    return render(request, 'showchoosefile.html', {"path_list":path_list})



def convert_to_wav(file_path):
    # if file_path.endswith(".mp4"):
    #     audio = AudioSegment.from_file(file_path, format="mp4")
    #     audio.export(file_path + "output.wav", format="wav")
    #     file_path = os.path.abspath(file_path + "output.wav")
    #     return file_path
    # else:
    return file_path

@login_required(login_url="userlogin")
def predictfile(request):
    path_list = request.session.get('path_list')
    predictgenre = []
    top3_predictgenre = []
    
    filename = []
    value = []
    audio_ids = []
    Fullpath = []
    user = User.objects.get(username=request.user)
    user1 = Userdata.objects.filter(UserName = request.user).first()
    for i in path_list:
        path = os.path.join(MEDIA_ROOT, i)
        file = File.objects.filter(UserName=user, FileUrl=path).first()
        Fullpath.append(file)
        converted_path = convert_to_wav(path)
        if os.path.exists(converted_path):
            kss = Keyword_Spotting_Service()
            keyword1, keyword2,keyword3 = kss.prediction(converted_path)
            predictgenre.append(keyword1)
            top3_predictgenre.append(keyword3)
            
            value.append(keyword2)
            filename.append(i)
            os.remove(converted_path)
        else:
            print(f"File not found at path: {converted_path}")
    
    for o, j, k,u in zip(predictgenre, filename, value,top3_predictgenre):
        value_json = json.dumps(k)
        audio = Audio.objects.create(UserName=user, FileName=j, Genre=o, Top3_Genre = u,Value=value_json)
        valueforchart = Valueforchart.objects.create(Genre=o,Age=user1.age)
        audio.save()
        valueforchart.save()
        audio_ids.append(audio.id)

    context = list(zip(filename, predictgenre, audio_ids, top3_predictgenre,Fullpath))
    
    return render(request, 'predict.html', {'context':context})



@login_required(login_url="userlogin")
def collection(request):
    if not request.user.is_authenticated:
        return redirect("userlogin")
    if request.method == 'POST':
        user = request.user
        collectionname = request.POST.get('collectionname')
        filenames = request.POST.getlist('filename')
        genres = request.POST.getlist('genre')
        all_genre = request.POST.getlist('all_genre')
        audio_ids = request.POST.getlist('audio_id')
        # Check if collection with the same name already exists for the user
        existing_collections = Collection.objects.filter(UserName=user, CollectionName=collectionname)
        if collectionname == '':
            messages.error(request, 'Add Collection uncomplete')
            return redirect('/choosefile')
        if existing_collections.exists():
            messages.error(request, 'A collection with the same name already exists.')
            return redirect('/choosefile')
        else:
            for filename, genre, audio_id, all_genre in zip(filenames, genres, audio_ids, all_genre):
                genre_names = [t[0] for t in ast.literal_eval(all_genre)]
                collection = Collection.objects.create(UserName=user,FileName=filename, Genre=genre, Top3_Genre=genre_names, Audio_Id=audio_id, CollectionName=collectionname)
                collection.save()
            return redirect('/choosefile')
    else:
        return redirect('/predictfile')
        
@login_required(login_url="userlogin")
def stackbar(request,audio_id):
    audio = Audio.objects.get(pk=audio_id)
    value = json.loads(audio.Value)
    keys = list(value.keys())
    print(keys)
    values = list(map(float,value.values()))
    labels = []
    second = 0
    for i in range(int(len(values)/10)):
        labels.append('second at ' + str(second))
        second += 30 
    genre = ['classical', 'country', 'jazz', 'metal', 'disco', 'pop', 'hiphop', 'reggae', 'blues', 'rock']
    rock = []
    metal = []
    pop = []
    disco = []
    blues = []
    classical = []
    jazz = []
    raggae = []
    country = []
    hiphop = []
     
    for i in range(0,len(values),10):
        classical.append(values[i])
    for i in range(1,len(values),10):
        country.append(values[i])
    for i in range(2,len(values),10):
        jazz.append(values[i])
    for i in range(3,len(values),10):
        metal.append(values[i])
    for i in range(4,len(values),10):
        disco.append(values[i])
    for i in range(5,len(values),10):
        pop.append(values[i])
    for i in range(6,len(values),10):
       hiphop.append(values[i])
    for i in range(7,len(values),10):
        raggae.append(values[i])
    for i in range(8,len(values),10):
        blues.append(values[i])
    for i in range(9,len(values),10):
        rock.append(values[i])
        
        
    labels1 = ['blue','classical','country','disco','hiphop','jazz','metal','pop','raggae','rock']
    result_blue = sum(blues)*10/len(value)
    result_classical = sum(classical)*10/len(value)
    result_country = sum(country)*10/len(value)
    result_disco = sum(disco)*10/len(value)
    result_hiphop = sum(hiphop)*10/len(value)
    result_jazz = sum(jazz)*10/len(value)
    result_metal = sum(metal)*10/len(value)
    result_pop = sum(pop)*10/len(value)
    result_raggae = sum(raggae)*10/len(value)
    result_rock = sum(rock)*10/len(value)
    print(result_blue+result_classical+result_country+result_disco+result_hiphop+result_jazz+result_metal+result_pop+result_raggae+result_rock)
    
    
    data = {
        'labels': labels,
        'blue': blues,
        'classical': classical,
        'country': country,
        'disco': disco,
        'hiphop':hiphop,
        'jazz':jazz,
        'metal':metal,
        'pop':pop,
        'raggae':raggae,
        'rock':rock
    }
    
    datadata = {
        'labels': labels1,
        'result_blue': result_blue,
        'result_classical': result_classical,
        'result_country': result_country,
        'result_disco': result_disco,
        'result_hiphop':result_hiphop,
        'result_jazz':result_jazz,
        'result_metal':result_metal,
        'result_pop':result_pop,
        'result_raggae':result_raggae,
        'result_rock':result_rock
    }
    return render(request, 'chart.html', {'data':data,'datadata':datadata})
    


@login_required(login_url="userlogin")
def topsongspotify(request):
    
    if not request.user.is_authenticated:
        return redirect("userlogin")
        
    client_id =    os.getenv("client_id")
    client_secret = os.getenv("client_secret")

    
    auth_url = 'https://accounts.spotify.com/api/token'
    try:
        auth_response = requests.post(auth_url, {
            'grant_type': 'client_credentials',
            'client_id': client_id,
            'client_secret': client_secret
        })
    except requests.exceptions.RequestException as e:
        return render(request, 'error.html', {'error_message': 'หน้าเว็บไม่พร้อมใช้งานโปรดลองอีกครั้งในภายหลัง'})
    
    if auth_response.status_code != 200:
        return render(request, 'error.html', {'error_message': 'หน้าเว็บไม่พร้อมใช้งานโปรดลองอีกครั้งในภายหลัง'})
    access_token = auth_response.json()['access_token']
    
    
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    
    
    playlist_id = '37i9dQZEVXbMDoHDwVN2tF' 
    try:
        response = requests.get(f'https://api.spotify.com/v1/playlists/{playlist_id}/tracks', headers=headers)
    except requests.exceptions.RequestException as e:
        return render(request, 'error.html', {'error_message': 'หน้าเว็บไม่พร้อมใช้งานโปรดลองอีกครั้งในภายหลัง'})
    
    if response.status_code != 200:
        return render(request, 'error.html', {'error_message': 'หน้าเว็บไม่พร้อมใช้งานโปรดลองอีกครั้งในภายหลัง'})

    
    top_songs = response.json()['items']
    song_data = []
    for i,song in enumerate(top_songs[:10]):
        try:
            artist_id = song["track"]["artists"][0]["id"]
            artist_response = requests.get(f'https://api.spotify.com/v1/artists/{artist_id}', headers=headers)
            if artist_response.status_code != 200:
                return render(request, 'error.html', {'error_message': 'หน้าเว็บไม่พร้อมใช้งานโปรดลองอีกครั้งในภายหลัง'})
            artist_name = artist_response.json()['name']
            genres = artist_response.json
            genres = artist_response.json()['genres']
            song_name = song["track"]["name"]
            artist_name =song["track"]["artists"][0]["name"]
            album_id =song["track"]["album"]["id"]
            album_response = requests.get(f'https://api.spotify.com/v1/albums/{album_id}', headers=headers)
            album_image_url =album_response.json()['images'][0]['url']
        except IndexError:
            artist_id = song["track"]["artists"][0]["id"]
            artist_response = requests.get(f'https://api.spotify.com/v1/artists/{artist_id}', headers=headers)
            if artist_response.status_code != 200:
                return render(request, 'error.html', {'error_message': 'หน้าเว็บไม่พร้อมใช้งานโปรดลองอีกครั้งในภายหลัง'})
            artist_response.json()['name']
            genres = None
            song_name = None
            artist_name = None
            album_id = None
            album_response = requests.get(f'https://api.spotify.com/v1/albums/{album_id}', headers=headers)
            album_image_url = None
            
        song_data.append({'song_name':song_name,'artist_name':artist_name,'album_image_url':album_image_url,'genres':genres})
    return render(request, 'topsong.html', {'song_data':song_data})


def error(request, error_message):
    return render(request, 'error.html', {'error_message': error_message})

@login_required(login_url="userlogin")
def mainpage(request):
    if request.user.is_authenticated:
        collections = Collection.objects.filter(UserName=request.user)
        collection_name = set(collections.values_list('collectionname', flat=True))
        collections = [{'collectionname': name} for name in collection_name]
        song_data = topsongspotify(request)
    else:
        return redirect("userlogin")
    return render(request, 'mainpage.html', {'song_data': song_data,'collections':collections})


@login_required(login_url="userlogin")
def topsonglastfm(request):
    if not request.user.is_authenticated:
        return redirect("userlogin")
        
   
    API_KEY = os.getenv("API_KEY")
    API_SECRET = os.getenv("API_SECRET")
    username = os.getenv("USER_NAME")
    password_hash = pylast.md5(os.getenv("password_hash"))

    
    try:
        network = pylast.LastFMNetwork(api_key=API_KEY, api_secret=API_SECRET,
                                    username=username, password_hash=password_hash)
    except pylast.NetworkError:
        time.sleep(30) # wait for 30 seconds
        return render(request, 'error.html', {'error_message': 'หน้าเว็บไม่พร้อมใช้งานโปรดลองอีกครั้งในภายหลัง:' })
    except Exception as e:
        return render(request, 'error.html', {'error_message': 'หน้าเว็บไม่พร้อมใช้งานโปรดลองอีกครั้งในภายหลัง:' })    
   

   
    try:
        top_tracks_of_week = network.get_top_tracks(limit=10)
    except pylast.NetworkError:
        time.sleep(30) # wait for 30 seconds
        return render(request, 'error.html', {'error_message': 'หน้าเว็บไม่พร้อมใช้งานโปรดลองอีกครั้งในภายหลัง' })
    except Exception as e:
        return render(request, 'error.html', {'error_message': 'หน้าเว็บไม่พร้อมใช้งานโปรดลองอีกครั้งในภายหลัง' })

    
    song_data = []
    genre = ['blue','classical','country','disco','hiphop','jazz','metal','pop','raggae','rock']
    for i,track in enumerate(top_tracks_of_week):
        try:
            song_name = track.item.get_name()
            artist_name = track.item.get_artist().get_name()
            album_image_url = track.item.get_cover_image()
        except IndexError:
            album_image_url = None
            song_name = None
            artist_name = None
        genres = [tag.item.get_name() for tag in track.item.get_top_tags()]
        new_list = []
        for element in genres:
            if element in genre:
                new_list.append(element)
        
        song_data.append({'song_name':song_name,'artist_name':artist_name,'album_image_url':album_image_url, 'genres': new_list})

    return render(request, 'topsong1.html', {'song_data':song_data})

            

   


    

@login_required(login_url="userlogin")
def download_json(request):
    if request.method == 'POST':
        filenames = request.POST.getlist('filename')
        genres = request.POST.getlist('genre')
        all_genres = request.POST.getlist('all_genre')
        data = {'filenames': filenames, 'genres': genres , 'all_genres':all_genres}
        json_data = json.dumps(data)
        response = HttpResponse(json_data, content_type='application/json')
        response['Content-Disposition'] = 'attachment; filename="data.json"'
        return response
    
@login_required(login_url="userlogin")
def collection_detail(request, collectionname):
    collection = Collection.objects.filter(UserName=request.user, CollectionName=collectionname)
    if len(collection) == 0:
        return redirect('/mainpage')
    else:
        return render(request, 'collectiondetail.html', {'collection': collection})



    
@login_required(login_url="userlogin")
def collections(request):
    if request.user.is_authenticated:
        collections = Collection.objects.filter(UserName=request.user)
        collection_name = set(collections.values_list('collectionname', flat=True))
        collections = [{'collectionname': name} for name in collection_name]
        return render(request, 'collections.html', {'collections': collections})
    else:
        return redirect('userlogin')

    
@login_required(login_url="userlogin")
def collection_delete(request, audio_id):
    try:
        collection = Collection.objects.get(UserName=request.user,Audio_Id=audio_id)
        collection.delete()
        collectionname = collection.collectionname
        collection = Collection.objects.filter(UserName=request.user,CollectionName=collectionname)
        if collection:
            return render(request, 'collectiondetail.html', {'collection':collection})
        else:
            return redirect('mainpage')
    except Collection.DoesNotExist:
        return render(request, 'error.html', {'error_message': 'Collection completed delete.'})

    

@login_required(login_url="userlogin")
def delete_collection(request):
    if request.method == 'POST':
        collectionname = request.POST.get('entries')
        try:
            entries = Collection.objects.filter(UserName=request.user,CollectionName=collectionname)
        except Collection.DoesNotExist:
            return render(request, 'error.html', {'error_message': 'Collection completed delete.'})
        entries.delete()
        return redirect('/mainpage')

@login_required(login_url="userlogin")
def confirm_delete(request, audio_id):
    try:
        collection = Collection.objects.get(UserName=request.user,Audio_Id=audio_id)
        collectionname = collection.collectionname
        collection = Collection.objects.filter(UserName=request.user,CollectionName=collectionname)
        return render(request, 'confirm_delete.html', {'collection': collection,'collectionname':collectionname})
    except Collection.DoesNotExist:
        return render(request, 'error.html', {'error_message': 'Collection completed delete.'})

@login_required(login_url="userlogin")
def confirm_delete_collection(request):
    if request.method == 'POST':
        collectionname = request.POST.get('collectionname')
        try:
            entries = Collection.objects.filter(UserName=request.user,CollectionName=collectionname)
        except Collection.DoesNotExist:
            return render(request, 'error.html', {'error_message': "Collection completed delete."})

        return render(request, 'confirm_delete_collection.html', {'entries':entries})
    else:
        return redirect('/mainpage')



            





