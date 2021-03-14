from django.urls import path
from . import views
from django.contrib.auth.views import LoginView,LogoutView
from django.contrib.auth import views as auth_views

urlpatterns = [
            path('',views.indexView,name="home"),
            path('about_us',views.about_us,name="about_us"),
            path('services',views.services,name="services"),
            path('queries',views.queries,name="queries"),
            path('contact_us',views.contact_us,name="contact_us"),
            path('dashboard/',views.dashboardView,name="dashboard"),
            path('login/',LoginView.as_view(),name="login_url"),
            path('registration/',views.registerView,name="register_url"),
            path('logout/',LogoutView.as_view(next_page='login_url'),name="logout"),
            path('password_reset',auth_views.PasswordResetView.as_view(),name="password_reset"),
            path('password_reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(),name="password_reset_confirm"),
            path('password_reset_done',auth_views.PasswordResetDoneView.as_view(),name="password_reset_done"),
            path('password_reset_complete',auth_views.PasswordResetCompleteView.as_view(),name="password_reset_complete"),
            path('post/<int:pk>/', views.post_detail, name='post_detail'),
            path('post/new/', views.post_new, name='post_new'),
            path('post/<int:pk>/edit',views.post_edit,name='post_edit'),
            path('post/<int:pk>/remove',views.post_remove,name='post_remove'),
            path('post_list', views.post_list, name='post_list'),
            path('queries',views.queries, name='queries'),
            path('detail/<int:id>',views.detail,name='detail'),

            path('save-upvote',views.save_upvote,name='save-upvote'),
            path('save-downvote',views.save_downvote,name='save-downvote'),
            path('ask-question',views.ask_form,name='ask-question'),
             # Tag Page
            path('tag/<str:tag>',views.tag,name='tag'),
            # Tags Page
            path('tags',views.tags,name='tags'),
            # Profile
            path('profile',views.profile,name='profile'),
            path('save-comment',views.save_comment,name='save-comment'),

]