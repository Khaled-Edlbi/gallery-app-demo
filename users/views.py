from django.http.response import HttpResponse
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterFrom, UserUpdateForm
from django.contrib import messages
from .models import Profile, Token
from gallery_app.models import PhotoCard, VideoCard, VoiceCard, ChatCard
from gallery_app.api import check_token, get_new_token
from django.db.models import Q
from itertools import chain
from django.core.paginator import Paginator


def register(request):

    if request.method == 'POST':
        form = UserRegisterFrom(request.POST)

        if form.is_valid():
            form.save()
            return redirect('login')

    else:
        form = UserRegisterFrom()

    return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request):

    user = request.user

    search_query = request.GET.get('q', '')
    filter_query = request.GET.get('filter', '')
    sort_order = request.GET.get('sort', '')
    order_by = request.GET.get('order-by', 'modified')

    if sort_order == 'ASC':
        ASC_icon = "fa-solid fa-arrow-up-a-z"
        ASC_DES_icon = ASC_icon
        ASC_DES = 'DES'
    else:
        DES_icon = "fa-solid fa-arrow-down-z-a"
        ASC_DES_icon = DES_icon
        ASC_DES = 'ASC'

    filtering_url = f"{reverse('profile')}?q={search_query}&order-by={order_by}"
    sorting_url = f"{reverse('profile')}?q={search_query}&filter={filter_query}&order-by={order_by}"
    ordering_url = f"{reverse('profile')}?q={search_query}&filter={filter_query}&sort={sort_order}"
    pagination_url = f"{reverse('profile')}?q={search_query}&filter={filter_query}&sort={sort_order}&order-by={order_by}"

    filtering = (
        Q(author=request.user) &
        (Q(title__icontains=search_query) | Q(body__icontains=search_query) | Q(date__icontains=search_query))
    )

    condition = order_by if sort_order == 'ASC' else '-' + order_by

    photos, videos, voices, chats, posts = [], [], [], [], []

    if filter_query == 'photos':
        photos = PhotoCard.objects.filter(filtering).order_by(condition)
        posts = photos

    elif filter_query == 'videos':
        videos = VideoCard.objects.filter(filtering).order_by(condition)
        posts = videos

    elif filter_query == 'voices':
        voices = VoiceCard.objects.filter(filtering).order_by(condition)
        posts = voices

    elif filter_query == 'chats':
        chats = ChatCard.objects.filter(filtering).order_by(condition)
        posts = chats

    else:
        photos = PhotoCard.objects.filter(filtering)
        videos = VideoCard.objects.filter(filtering)
        voices = VoiceCard.objects.filter(filtering)
        chats = ChatCard.objects.filter(filtering)

        all_posts = list(chain(photos, videos, voices, chats))
        all_posts = sorted(all_posts, key=lambda x: getattr(x, order_by), reverse=True)

        if sort_order == 'ASC': all_posts.reverse()
        posts = all_posts

    paginator = Paginator(posts, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        'user': user,
        'page_obj': page_obj,

        'ASC_DES_icon': ASC_DES_icon,
        'ASC_DES': ASC_DES,

        'filtering_url': filtering_url,
        'sorting_url': sorting_url,
        'ordering_url': ordering_url,
        'pagination_url': pagination_url,

        'posts_count': len(posts),
        'photos_count': len(photos),
        'videos_count': len(videos),
        'voices_count': len(voices),
        'chats_count': len(chats)
    }

    return render(request, 'users/profile.html', context)


@login_required
def update_profile(request):

    access_token = Token.objects.get(user=request.user).access_token
    current_profile = Profile.objects.get(user=request.user)

    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        new_profile_image = request.POST.get('image')

        if new_profile_image:
            current_profile.image = new_profile_image
            current_profile.save()

        if user_form.is_valid():
            user_form.save()
            messages.success(request, f"Your account has been updated successfully!")
            return redirect('profile')

    else:
        user_form = UserUpdateForm(instance=request.user)

    context = {
        'user_form': user_form,
        'current_profile': current_profile,
        'access_token': access_token
    }

    return render(request, 'users/profile_update.html', context)


@login_required
def token_check_view(request):
    try:
        token = Token.objects.get(user=request.user)
        token_check = check_token(token.access_token)
        if token_check['success']:
            return redirect('home')
        else:
            if token_check['data']['error'] == "The access token provided is invalid.":
                new_tokens = get_new_token(token.refresh_token)
                try:
                    token.access_token = new_tokens['access_token']
                    token.refresh_token = new_tokens['refresh_token']
                    token.save()
                    return redirect('home')
                except KeyError:
                    error_msg = f"Something went wrong with 'Generate Access Token' API!, {new_tokens['data']['error']}"
            else:
                error_msg = f"Something went wrong with 'Feed' API!, {token_check['data']['error']}"

    except Token.DoesNotExist:
        error_msg = "Token for the user does not exist!"

    return HttpResponse(f"<h1>{error_msg}</h1>")
