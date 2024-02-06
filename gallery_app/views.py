from django.shortcuts import render, reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView
from .models import PhotoCard, VideoCard, VoiceCard, ChatCard
from users.models import Token
from django.db.models import Q
from django.core.paginator import Paginator


@login_required
def home(request):
    return render(request, 'gallery_app/home_page.html')


def views_abstract(request, view_page, model):

    search_query = request.GET.get('q', '')
    sort_order = request.GET.get('sort', '')
    order_by = request.GET.get('order-by', '?')

    if sort_order == 'DES':
        DES_icon = "fa-solid fa-arrow-down-z-a"
        ASC_DES_icon = DES_icon
        ASC_DES = 'ASC'
    else:
        ASC_icon = "fa-solid fa-arrow-up-a-z"
        ASC_DES_icon = ASC_icon
        ASC_DES = 'DES'

    sorting_url = f"{reverse(view_page)}?q={search_query}&order-by={order_by}"
    ordering_url = f"{reverse(view_page)}?q={search_query}&sort={sort_order}"
    pagination_url = f"{reverse(view_page)}?q={search_query}&sort={sort_order}&order-by={order_by}"

    posts_list = model.objects.filter(
        Q(title__icontains=search_query) |
        Q(body__icontains=search_query) |
        Q(date__icontains=search_query) |
        Q(author__username__icontains=search_query)
    ).order_by('-' + order_by if sort_order == 'DES' and order_by != '?' else order_by)

    content_count = posts_list.count()

    paginator = Paginator(posts_list, 40)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    objs_num = len(page_obj)
    col_objs_num = objs_num // 4
    rem_division = objs_num % 4
    col_01_rem = 0
    col_02_rem = 0
    col_03_rem = 0
    if rem_division == 3:
        col_01_rem = 1
        col_02_rem = 2
        col_03_rem = 3
    if rem_division == 2:
        col_01_rem = 1
        col_02_rem = 2
        col_03_rem = 2
    if rem_division == 1:
        col_01_rem = 1
        col_02_rem = 1
        col_03_rem = 1

    col_01_objs = page_obj[:col_objs_num+col_01_rem]
    col_02_objs = page_obj[col_objs_num+col_01_rem:col_objs_num*2+col_02_rem]
    col_03_objs = page_obj[col_objs_num*2+col_02_rem:col_objs_num*3+col_03_rem]
    col_04_objs = page_obj[col_objs_num*3+col_03_rem:]
    cols_objs = [col_01_objs, col_02_objs, col_03_objs, col_04_objs]

    return {
        'view_page': view_page,
        'cols_objs': cols_objs,

        'ASC_DES': ASC_DES,
        'ASC_DES_icon': ASC_DES_icon,

        'sorting_url': sorting_url,
        'ordering_url': ordering_url,
        'pagination_url': pagination_url,

        'content_count': content_count,
        'page_obj': page_obj,
    }


@login_required
def photos(request):
    context = views_abstract(request, 'photos', PhotoCard)
    return render(request, 'gallery_app/posts_pages/photos_page.html', context)


@login_required
def videos(request):
    context = views_abstract(request, 'videos', VideoCard)
    return render(request, 'gallery_app/posts_pages/videos_page.html', context)


@login_required
def voices(request):
    context = views_abstract(request, 'voices', VoiceCard)
    return render(request, 'gallery_app/posts_pages/voices_page.html', context)


@login_required
def chats(request):
    context = views_abstract(request, 'chats', ChatCard)
    return render(request, 'gallery_app/posts_pages/chats_page.html', context)


class AbstractCreateView(LoginRequiredMixin, CreateView):
    fields = ['title', 'body']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        token_obj = Token.objects.get(user=self.request.user)
        context['access_token'] = token_obj.access_token
        return context

    def form_valid(self, form):
        form.instance.image = self.request.POST.get('image')
        if self.request.POST.get('date'):
            form.instance.date = self.request.POST.get('date')
        form.instance.author = self.request.user
        return super().form_valid(form)


class PhotoCreateView(AbstractCreateView):
    model = PhotoCard
    template_name = 'gallery_app/create&edit_pages/photo_create.html'


class VideoCreateView(AbstractCreateView):
    model = VideoCard
    template_name = 'gallery_app/create&edit_pages/video_create.html'


class VoiceCreateView(AbstractCreateView):
    model = VoiceCard
    template_name = 'gallery_app/create&edit_pages/video_create.html'


class ChatCreateView(AbstractCreateView):
    model = ChatCard
    template_name = 'gallery_app/create&edit_pages/photo_create.html'


def select_post_type(request):
    return render(request, 'gallery_app/create&edit_pages/select_post_type.html')


class AbstractDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    template_name = 'gallery_app/post_details.html'
    fields = ['title', 'body', 'image', 'date']

    def test_func(self):
        photo_card = self.get_object()
        if self.request.user == photo_card.author:
            return True
        return False


class PhotoDetailView(AbstractDetailView):
    model = PhotoCard


class VideoDetailView(AbstractDetailView):
    model = VideoCard


class VoiceDetailView(AbstractDetailView):
    model = VoiceCard


class ChatDetailView(AbstractDetailView):
    model = ChatCard


class AbstractEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    fields = ['title', 'body']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        token_obj = Token.objects.get(user=self.request.user)
        context['access_token'] = token_obj.access_token
        return context

    def form_valid(self, form):
        form.instance.image = self.request.POST.get('image')
        if self.request.POST.get('date'):
            form.instance.date = self.request.POST.get('date')
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        photo_card = self.get_object()
        if self.request.user == photo_card.author:
            return True
        return False


class PhotoEditView(AbstractEditView):
    model = PhotoCard
    template_name = 'gallery_app/create&edit_pages/photo_create.html'


class VideoEditView(AbstractEditView):
    model = VideoCard
    template_name = 'gallery_app/create&edit_pages/video_create.html'


class VoiceEditView(AbstractEditView):
    model = VoiceCard
    template_name = 'gallery_app/create&edit_pages/video_create.html'


class ChatEditView(AbstractEditView):
    model = ChatCard
    template_name = 'gallery_app/create&edit_pages/photo_create.html'


class AbstractDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    template_name = 'gallery_app/post_delete.html'
    success_url = '/profile/'

    def test_func(self):
        photo_card = self.get_object()
        if self.request.user == photo_card.author:
            return True
        return False


class PhotoDeleteView(AbstractDeleteView):
    model = PhotoCard


class VideoDeleteView(AbstractDeleteView):
    model = VideoCard


class VoiceDeleteView(AbstractDeleteView):
    model = VoiceCard


class ChatDeleteView(AbstractDeleteView):
    model = ChatCard
