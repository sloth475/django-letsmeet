from django.urls import path,include
from . import views
from rest_framework.routers import DefaultRouter
router=DefaultRouter()
router.register('post',views.PostViewSet,basename="viewset-post")
# router.register("generic",views.EventGenericViewSet,basename="viewset-generic")

urlpatterns = [
    path("viewset/", include(router.urls)),
    path("api-view/", views.PostApiView),
    path("", views.StartingPageView.as_view(), name="starting-page"),
    path("events/", views.PostsView.as_view(), name="all-posts"),
    path("events/<slug:slug>", views.PostsDetailView.as_view(), name="selected-post"),
    # path("read-later", views.ReadLaterView.as_view(), name="read-later"),
    path("thank-you/", views.ThankYouView.as_view(), name="thank-you"),
    path("create_view/", views.CreateView.as_view(), name="add-post"),
    path("<slug>/update", views.UpdateView.as_view(), name="update-event"),
    path("register/", views.register_request, name="register"),
    path("login", views.login_request, name="login"),
    path("logout", views.logout_request, name="logout"),
    # path("article", views.EventListView.as_view(), name="article-list"),
    # path("article/<slug:slug>", views.EventDetailView.as_view(), name="article-detail"),

]