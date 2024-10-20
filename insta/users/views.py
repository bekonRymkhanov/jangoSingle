from django.shortcuts import render, redirect,get_object_or_404
from django.contrib import messages
from .forms import UserRegisterForm,ProfileForm
from .models import Profile,Follow
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save() 
            username = form.cleaned_data.get('username')
            
            Profile.objects.create(user=user)
            
            messages.success(request, f'Account created for {username}. Your profile has been created.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    
    return render(request, 'register.html', {'form': form})


def profile_view(request, username):
    user = get_object_or_404(User, username=username)
    profile = Profile.objects.get(user=user)

    
    followers_count = Follow.objects.filter(following=user).count()
    following_count = Follow.objects.filter(follower=user).count()

    is_following = Follow.objects.filter(follower=request.user, following=user).exists()

    return render(request, 'profile.html', {
        'profile': profile,
        'followers_count': followers_count,
        'following_count': following_count,
        'is_following': is_following, 
    })
@login_required
def edit_profile(request,username):
    profile = get_object_or_404(Profile, user__username=username)
    print(f"Editing profile for user: {request.user.username}")

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile', username=request.user.username)
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'edit_profile.html', {'form': form})



def main(request):
    return render(request,template_name='mainu.html')


@login_required
def follow_user(request, username):
    user_to_follow = get_object_or_404(User, username=username)
    
    if not Follow.objects.filter(follower=request.user, following=user_to_follow).exists():
        Follow.objects.create(follower=request.user, following=user_to_follow)
        messages.success(request, f'You have successfully followed {user_to_follow.username}!')
    
    return redirect('profile', username=username)


@login_required
def unfollow_user(request, username):
    user_to_unfollow = get_object_or_404(User, username=username)

    follow_relation = Follow.objects.filter(follower=request.user, following=user_to_unfollow)
    if follow_relation.exists():
        follow_relation.delete()
        messages.success(request, f'You have successfully unfollowed {user_to_unfollow.username}.')

    return redirect('profile', username=username)