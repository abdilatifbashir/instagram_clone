from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
# from .forms import NewStatusForm
from .models import Image, Profile

# Create your views here.
@login_required(login_url='/accounts/login/')
def timelines(request):
    current_user = request.user
    images = Image.objects.order_by('-date_uploaded')
    profiles = Profile.objects.order_by('-last_update')
    user_profile = Profile.objects.get(id = current_user.id)
    return render(request, 'timelines.html', {'images':images, 'profiles':profiles, 'user_profile':user_profile})

@login_required(login_url='/accounts/login/')
def profile(request):
    current_user = request.user
    profile = Profile.objects.get(id = current_user.id)
    images = Image.objects.all().filter(id=current_user.id)
    return render(request, 'profile.html', {'profile':profile, 'images':images})

@login_required(login_url='/accounts/login/')
def new_status(request):
    current_user = request.user
    if request.method == 'POST':
        form = NewStatusForm(request.POST, request.FILES)
        if form.is_valid():
            status = form.save()
            status.user = current_user
            status.save()
        HttpResponseRedirect('timelines')
    else:
        form = NewStatusForm()
    return render(request, 'new_status.html', {"form": form})

@login_required(login_url='/accounts/login')
def user_profile(request, user_id):
    profile = Profile.objects.get(id=user_id)
    images = Image.objects.all().filter(id=user_id)
    print(images)
    return render(request, 'profile.html', {'profile':profile, 'images':images})

@login_required(login_url='/accounts/login')
def single_image(request, photo_id):
    image = Image.objects.get(id = photo_id)
    return render(request, 'single_image.html', {'image':image})

def find_profile(request):
    if 'images' in request.GET and request.GET['images']:
        search_term = request.GET.get('images')
        searched_image = Image.search_by_user(search_term)
        return render(request, 'user_profile.html', {'images':searched_image})
    else:
        message = 'You haven\'t searched for anything'
        return render(request, 'single_image.html')
