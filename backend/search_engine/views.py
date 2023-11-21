from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from rest_framework.response import Response
from search_engine.forms import People, ProfileUpdateForm, UserUpdateForm
from search_engine.models import CrawlingQueue, Item
from crawling.crawling.items import CrawlingItem
from .serializers import UserSerializer, ItemSerializer
from .documents import ItemDocument
from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework import permissions

# Create your views here.

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer

class ItemViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

def accountRecovery(request):
    return render(request, 'search_engine/recoveryPass.html', {'title': 'accountRecovery'})


def signup(request):
    if request.method == 'POST':
        form = People(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Your account has been created! You can now log in.')
            return redirect('search_engine-login')
    else:
        form = People()
    return render(request, 'search_engine/signup.html', {'form': form})

def log_in(request):
    return render(request, 'search_engine/login.html', {'title': 'login'})

@login_required
def dashboard(request):
    return render(request, 'search_engine/dashboard.html', {'title': 'dashboard'})

@login_required
def search(request):
    if request.method == 'POST':
        urltext = request.POST.get('urlsText')    # getting list of urls input by user
        clusterID = request.POST.get('cluster')   # getting cluster name from user
        username = request.user                   # requesting current user
        depth = request.POST.get('depth')
        strategy = request.POST.get('contentType')

        crawl_item = CrawlingQueue(userName=username, clusterName=clusterID, url=urltext, depth = depth, strategy = strategy)
        crawl_item.save()  # the entries are passed to CrawlingQueue model and saved to Database
        messages.success(request, f'Cluster created successfully!')
        return render(request, 'search_engine/search.html', {'title': 'search'})


    return render(request, 'search_engine/search.html', {'title': 'search'})

@login_required
def searchClusters(request):
    clusters = CrawlingQueue.objects.all().values_list('clusterName').filter(
        userName=request.user.username).distinct()  # get all clusters for current logged in user as tuples

    clusters = [x[0] for x in clusters]  # convert tuples to values of a list

    #CrawlingQueue.objects.filter(clusterName = 'PDFs').delete()
    #CrawlingQueue.objects.filter(clusterName = 'Unis').delete()
    #CrawlingQueue.objects.filter(clusterName = 'DSDSD').delete()

    print("deleted")

    if request.method == 'POST':
        clusterID = request.POST.get('cluster')
        keyword = request.POST.get('keyword')

        relevant_links = ItemDocument.search().filter("match", username = request.user.username).filter("match", clustername = clusterID).filter("term", content = keyword)

        print("Links: ")

        for x in relevant_links:
            print(x.link)

        return render(request, 'search_engine/result.html', {'mylist': relevant_links, 'keyword': keyword})

    return render(request, 'search_engine/searchClusters.html',
                  {'clusters': clusters})  # render the clusters to html template using clusters

@login_required
def result(request):
    return render(request, 'search_engine/result.html')

@login_required
def about(request):
    return render(request, 'search_engine/about.html', {'title': 'about'})

@login_required
def user(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('search_engine-user')
    
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'search_engine/user.html', context)
