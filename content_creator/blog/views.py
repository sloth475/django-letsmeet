from datetime import datetime

from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.http import HttpResponseNotFound, HttpResponseRedirect
from django.views.generic import ListView, DetailView, CreateView, FormView, UpdateView
from rest_framework import mixins, status, generics, viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet, ViewSet, ModelViewSet
from rest_framework import viewsets

from .models import Post, Author, Tag
from django.views import View
from django.views.generic.base import TemplateView
from .forms import UploadForm, NewUserForm, RegisterEventForm, UpdateEventForm
from django.urls import reverse
from .models import Post
from .serializers import PostSerializer


# class MyPagination(PageNumberPagination):
#     page_size = 6
#     page_size_query_param = "page_size"
#     max_page_size = 20
#
# class EventGenericViewSet(GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin,
#                                 mixins.DestroyModelMixin):
#         serializer_class = EventSerializer
#         queryset = Post.objects.all()
#         pagination_class = MyPagination
#
#         def get_queryset(self):  # Generic View Sets and Generic Views
#             qs = super().get_queryset()
#             author = self.request.query_params.get("author", None)
#             if author:
#                 qs = qs.filter(author=author)
#             return qs
#
# # Viewset are specifically designed for CRUD Operations
# # list fetch
# # create - creating



class PostApiView(APIView):
    serializer_class=PostSerializer


    # Get all Data
    def list(self, request):
        events = Post.objects.all()
        author = request.query_params.get("author", None)
        if author:
            events = events.filter(author = author)
        result_set = self.paginate_queryset(events, request, view=self)
        serializers = PostSerializer(result_set, many=True)
        # return Response(serializers.data)
        return self.get_paginated_response(serializers.data)

    # Post a given data
    def create(self, request):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Get Specifc data
    def retrieve(self, request, pk):
        qs = Post.objects.all()
        article = get_object_or_404(qs, pk=pk)
        serializer = PostSerializer(article)
        return Response(serializer.data)

    # PUT
    def update(self, request, pk):
        qs = Post.objects.all()
        article = get_object_or_404(qs, pk=pk)
        serializer = PostSerializer(article, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # delete
    def destroy(self, request, pk):
        qs = Post.objects.all()
        article = get_object_or_404(qs, pk=pk)
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
#     #---------------------------------------------------------------------------------------------------------------------------


class StartingPageView(TemplateView):
    template_name = "blog/index.html"

    def get_context_data(self, **kwargs):
        latest = Post.objects.all().order_by('-date') [:2]
        context = super().get_context_data(**kwargs)
        context ["posts"] = latest
        return context


# def posts(request):
#     all_posts = Post.objects.all()
#     return render(request, "blog/all_posts.html", {"posts": all_posts})
class PostsView(ListView):
    template_name = "blog/all_posts.html"
    model = Post
    context_object_name = "posts"


class PostsDetailViewsss(DetailView):
    template_name = 'blog/post_detail.html'
    model = Post
    context_object_name = 'post'


class PostsDetailView(View):  # remove s

    def get(self, request, slug):
        post = Post.objects.get(slug=slug)
        register_form = RegisterEventForm()
        # print(self.is_read_later(request, post.id))
        return render(request, "blog/post_detail.html",
                      {"post": post, "post_tags": post.tags.all(), "registrations": post.registrations.all().order_by("-id"), "register_form": register_form, })

    # return render(request, "blog/post_detail.html",
    #               {"post": post, "post_tags": post.tags.all(), "comments": post.comments.all().order_by("-id"), "comment_form": comment_form, })

    def post(self, request, slug):
        post = Post.objects.get(slug=slug)
        register_form = RegisterEventForm(request.POST)
        if register_form.is_valid():
            register_form = register_form.save(commit=False)
            register_form.post = post
            register_form.save()
            url = reverse("selected-post", args=[slug, ])
            return HttpResponseRedirect(url)
        return render(request, "blog/post_detail.html",
                      {"post": post, "post_tags": post.tags.all(), "registrations": post.registrations.all().order_by("-id"), "register_form": register_form, }
                      # {"post": post, "post_tags": post.tags.all(), "comments": post.comments.all().order_by("-id"), "comment_form": comment_form, }
                      )


class AboutView(TemplateView):
    template_name = "blog/about.html"


class PolicyView(TemplateView):
    template_name = "blog/policy.html"


class CarrersView(TemplateView):
    template_name = "blog/carrers.html"


class ThankYouView(TemplateView):
    template_name = "blog/thank_you.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context ["message"] = "You Action is saved!!!!"
        return context


class CreateView(CreateView):  # form view will do get and post
    template_name = "blog/create_view.html"
    form_class = UploadForm
    success_url = "/thank-you"
    model = Post


class UpdateView(UpdateView):  # form view will do get and post
    template_name = "blog/update_view.html"
    form_class = UpdateEventForm
    success_url = "/thank-you"
    model = Post


def register_request(request):
    if request.method=="POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect('/')
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    return render(request=request, template_name="blog/register.html", context={"register_form": form})


def login_request(request):
    if request.method=="POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("/")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request=request, template_name="blog/login.html", context={"login_form": form})


def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("/")


# -------------------------------------------------------------------------------------
# class EventListViewssss(APIView, MyPagination):
#
#     def get(self, request):
#         articles = Post.objects.all()
#         author = request.query_params.get("author", None)
#         if author:
#             articles = articles.filter(author = author)
#         result_set = self.paginate_queryset(articles, request, view=self)
#         serializers = EventSerializer(result_set, many=True)
#         # return Response(serializers.data)
#         return self.get_paginated_response(serializers.data)
#
#     def post(self, request):
#         serializer = EventSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
# class EventDetailViewssss(APIView):
#     def get_article(self, slug):
#         try:
#             return Post.objects.get(slug=slug)
#         except:
#             return None
#
#     def get(self, request, pk):
#         article = self.get_article(pk)
#         if article:
#             serializer = EventSerializer(article)
#             return Response(serializer.data)
#         return Response(status=status.HTTP_404_NOT_FOUND)
#
#     def put(self, request, pk):
#         article = self.get_article(pk)
#         if article:
#             serializer = EventSerializer(article, data=request.data)
#             if serializer.is_valid():
#                 serializer.save()
#                 return Response(serializer.data, status=status.HTTP_200_OK)
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#         return Response(status=status.HTTP_404_NOT_FOUND)
#
#     def delete(self, request, slug):
#         article = self.get_post(slug)
#         if article:
#             article.delete()
#             return Response(status=status.HTTP_204_NO_CONTENT)
#         return Response(status=status.HTTP_404_NOT_FOUND)
# #######################################
# class EventListView(generics.ListCreateAPIView):
#     qs=Post.objects.all()
#     serializer_class=EventSerializer
# class EventDetailView(generics.RetrieveUpdateDestroyAPIView):
#     qs=Post.objects.all()
#     serializer_class = EventSerializer
class PostViewSet(viewsets.ViewSet):
    def list(self, request):
        queryset = Post.objects.all()
        serializer = PostSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, slug):
        queryset = Post.objects.all()
        post = get_object_or_404(queryset, slug=slug)
        serializer = PostSerializer(post)
        return Response(serializer.data)
