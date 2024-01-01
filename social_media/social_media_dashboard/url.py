from django.urls import path
from django.contrib.auth import views as auth_views
from .views import dashboard, register, like_post, comment_post, share_post, connect_facebook, connect_twitter, facebook_callback, twitter_like_post, twitter_comment_post,twitter_share_post, facebook_like_post,facebook_comment_post,facebook_share_post, user_login, user_logout


urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('connect-twitter/', connect_twitter, name='connect_twitter'),
    path('connect-facebook/', connect_facebook, name='connect_facebook'),
    path('facebook-callback/', facebook_callback, name='facebook_callback'),
    path('register/', register, name='register'),
    path('like/<int:post_id>/', like_post, name='like_post'),
    path('comment/<int:post_id>/', comment_post, name='comment_post'),
    path('share/<int:post_id>/', share_post, name='share_post'),
    # path('', user_login, name='login'),
    # path('logout/', user_logout, name='logout'),

    path('twitter/like/<int:post_id>/', twitter_like_post, name='twitter_like_post'),
    path('twitter/comment/<int:post_id>/', twitter_comment_post, name='twitter_comment_post'),
    path('twitter/share/<int:post_id>/', twitter_share_post, name='twitter_share_post'),
    path('facebook/like/<int:post_id>/', facebook_like_post, name='facebook_like_post'),
    path('facebook/comment/<int:post_id>/', facebook_comment_post, name='facebook_comment_post'),
    path('facebook/share/<int:post_id>/', facebook_share_post, name='facebook_share_post'),

]