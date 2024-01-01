from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate,  logout
from django.contrib.auth.models import User 
from .models import UserProfile, SocialMediaPost
from .forms import CustomUserCreationForm
import twitter
import facebook
from django.conf import settings
import json
import logging
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from django.contrib import messages
# Create your views here.
# social_media_dashboard/views.py


@login_required
def dashboard(request):
    user_profile = UserProfile.objects.get(user=request.user)
    twitter_api = twitter.Api(consumer_key=settings.TWITTER_CONSUMER_KEY,
                              consumer_secret=settings.TWITTER_CONSUMER_SECRET,
                              access_token_key=user_profile.twitter_access_token,
                              access_token_secret=user_profile.twitter_access_token_secret)

    # Fetch user posts from Twitter
    twitter_posts = twitter_api.GetUserTimeline(count=10)

    # Fetch user posts from Facebook (assuming you have a proper implementation)
    # facebook_posts = ...

    context = {
        'twitter_posts': twitter_posts,
        'facebook_posts': facebook_posts,
    }
    return render(request, 'dashboard.html', context)

def register(request):
    if request.method == 'POST':
        # Handle user registration form submission
        username = request.POST['username']
        password = request.POST['password']
        user = User.objects.create_user(username=username, password=password)
        
        # Log the user in after registration
        login(request, user)
        return redirect('dashboard')

    return render(request, 'registration/register.html')

@login_required
def like_post(request, post_id):
    post = SocialMediaPost.objects.get(id=post_id)
    post.likes += 1
    post.save()
    return HttpResponse(json.dumps({'likes': post.likes}), content_type="application/json")

@login_required
def comment_post(request, post_id):
    if request.method == 'POST':
        comment_text = request.POST.get('comment_text')
        post = SocialMediaPost.objects.get(id=post_id)
        post.comments = comment_text
        post.save()
        return HttpResponse(json.dumps({'comments': post.comments}), content_type="application/json")

@login_required
def share_post(request, post_id):
    # Implement post sharing logic here
    return HttpResponse(json.dumps({'message': 'Post shared successfully'}), content_type="application/json")


logger = logging.getLogger(__name__)
def twitter_api_setup(user):
    user_profile = UserProfile.objects.get(user=user)
    logger.debug(f"Twitter Access Token: {user_profile.twitter_access_token}")
    logger.debug(f"Twitter Access Token Secret: {user_profile.twitter_access_token_secret}")
    return twitter.Api(
        consumer_key=settings.TWITTER_CONSUMER_KEY,
        consumer_secret=settings.TWITTER_CONSUMER_SECRET,
        access_token_key=user_profile.twitter_access_token,
        access_token_secret=user_profile.twitter_access_token_secret
    )

def facebook_api_setup(user):
    user_profile = UserProfile.objects.get(user=user)
    return facebook.GraphAPI(access_token=user_profile.facebook_access_token, version="3.0")

def social_media_dashboard(request):
    user = request.user
    user_profile = UserProfile.objects.get(user=user)
    
    # Twitter API
    twitter_api = twitter_api_setup(user)
    twitter_posts = twitter_api.GetUserTimeline(count=10)

    # Facebook API
    facebook_api = facebook_api_setup(user)
    # Assuming you have implemented a function to fetch Facebook posts
    facebook_posts = fetch_facebook_posts(facebook_api)

    context = {
        'twitter_posts': twitter_posts,
        'facebook_posts': facebook_posts,
    }
    return render(request, 'dashboard.html', context)

# social_media_dashboard/views.py
def fetch_facebook_posts(api):
    try:
        posts = api.get_object('me/posts')
        return posts.get('data', [])
    except facebook.GraphAPIError as e:
        print(f"Facebook API Error: {e}")
        return []



def twitter_like_post(request, post_id):
    twitter_api = twitter_api_setup(request.user)
    try:
        tweet = twitter_api.GetStatus(post_id)
        twitter_api.CreateFavorite(status=tweet)
        new_like_count = tweet.favorite_count + 1
        return JsonResponse({'likes': new_like_count})
    except twitter.error.TwitterError as e:
        print(f"Twitter API Error: {e}")
        return JsonResponse({'error': 'Failed to like the post'}, status=500)

def twitter_comment_post(request, post_id):
    twitter_api = twitter_api_setup(request.user)
    comment_text = request.POST.get('comment_text', '')
    try:
        tweet = twitter_api.GetStatus(post_id)
        twitter_api.PostUpdate(f"@{tweet.user.screen_name} {comment_text}", in_reply_to_status_id=post_id)
        return JsonResponse({'comments': comment_text})
    except twitter.error.TwitterError as e:
        print(f"Twitter API Error: {e}")
        return JsonResponse({'error': 'Failed to comment on the post'}, status=500)

def twitter_share_post(request, post_id):
    twitter_api = twitter_api_setup(request.user)
    try:
        tweet = twitter_api.GetStatus(post_id)
        twitter_api.PostUpdate(f"Check out this tweet: https://twitter.com/{tweet.user.screen_name}/status/{post_id}")
        return JsonResponse({'message': 'Post shared on Twitter'})
    except twitter.error.TwitterError as e:
        print(f"Twitter API Error: {e}")
        return JsonResponse({'error': 'Failed to share the post'}, status=500)


def facebook_like_post(request, post_id):
    facebook_api = facebook_api_setup(request.user)
    try:
        facebook_api.put_like(object_id=post_id)
        # Assuming Facebook returns the updated like count (you may need to fetch it separately)
        new_like_count = 0
        return JsonResponse({'likes': new_like_count})
    except facebook.GraphAPIError as e:
        print(f"Facebook API Error: {e}")
        return JsonResponse({'error': 'Failed to like the post'}, status=500)

def facebook_comment_post(request, post_id):
    facebook_api = facebook_api_setup(request.user)
    comment_text = request.POST.get('comment_text', '')
    try:
        facebook_api.put_comment(object_id=post_id, message=comment_text)
        return JsonResponse({'comments': comment_text})
    except facebook.GraphAPIError as e:
        print(f"Facebook API Error: {e}")
        return JsonResponse({'error': 'Failed to comment on the post'}, status=500)

def facebook_share_post(request, post_id):
    facebook_api = facebook_api_setup(request.user)
    try:
        # Assuming you have the necessary parameters for sharing a post
        # Update the 'message', 'link', etc. based on your requirements
        facebook_api.put_object(parent_object=post_id, connection_name='feed', message='Check out this post!')
        return JsonResponse({'message': 'Post shared on Facebook'})
    except facebook.GraphAPIError as e:
        print(f"Facebook API Error: {e}")
        return JsonResponse({'error': 'Failed to share the post'}, status=500)


@login_required
def connect_twitter(request):
    user = request.user
    user_profile, created = UserProfile.objects.get_or_create(user=user)
    
    if not user_profile.twitter_access_token:
        try:
            api = twitter.Api(
                consumer_key=settings.TWITTER_CONSUMER_KEY,
                consumer_secret=settings.TWITTER_CONSUMER_SECRET,
                access_token_key=user_profile.twitter_access_token,
                access_token_secret=user_profile.twitter_access_token_secret
            )
            request_token = api.getRequestToken()
            auth_url = api.getAuthorizationURL(request_token)
            request.session['twitter_request_token'] = request_token.to_string()
            return redirect(auth_url)
        except twitter.error.TwitterError as e:
            print(f"Twitter API Error: {e}")
            messages.error(request, 'Error connecting to Twitter. Please try again.')
    else:
        messages.warning(request, 'Twitter account already connected.')

    return redirect(reverse('dashboard'))

@login_required
def connect_facebook(request):
    user = request.user
    user_profile, created = UserProfile.objects.get_or_create(user=user)
    
    if not user_profile.facebook_access_token:
        try:
            # Your Facebook App credentials
            app_id = 'your_facebook_app_id'
            app_secret = 'your_facebook_app_secret'
            
            # Redirect the user to the Facebook login page
            redirect_uri = request.build_absolute_uri(reverse('facebook_callback'))
            auth_url = f'https://www.facebook.com/v11.0/dialog/oauth?client_id={app_id}&redirect_uri={redirect_uri}&scope=public_profile,email'
            
            # Store the state in the session to prevent CSRF attacks
            request.session['facebook_state'] = 'your_random_state_value'
            
            return redirect(auth_url)
        except facebook.GraphAPIError as e:
            print(f"Facebook API Error: {e}")
            messages.error(request, 'Error connecting to Facebook. Please try again.')
    else:
        messages.warning(request, 'Facebook account already connected.')

    return redirect(reverse('dashboard'))

@csrf_exempt
def facebook_callback(request):
    user = request.user
    user_profile, created = UserProfile.objects.get_or_create(user=user)

    # Verify the state to prevent CSRF attacks
    if request.GET.get('state') != request.session.get('facebook_state'):
        messages.error(request, 'CSRF attack detected.')
        return JsonResponse({'error': 'CSRF attack detected.'}, status=403)

    try:
        # Your Facebook App credentials
        app_id = 'your_facebook_app_id'
        app_secret = 'your_facebook_app_secret'
        
        # Get the access token using the authorization code
        code = request.GET.get('code')
        redirect_uri = request.build_absolute_uri(reverse('facebook_callback'))
        access_token_url = f'https://graph.facebook.com/v11.0/oauth/access_token?client_id={app_id}&redirect_uri={redirect_uri}&client_secret={app_secret}&code={code}'
        response = facebook.GraphAPI().get_object('oauth/access_token', **{'client_id': app_id, 'redirect_uri': redirect_uri, 'client_secret': app_secret, 'code': code})
        access_token = response['access_token']

        # Store the access token securely in the UserProfile model
        user_profile.facebook_access_token = access_token
        user_profile.save()

        messages.success(request, 'Facebook account connected successfully.')
    except facebook.GraphAPIError as e:
        print(f"Facebook API Error: {e}")
        messages.error(request, 'Error connecting to Facebook. Please try again.')

    return redirect(reverse('dashboard'))


def user_login(request):
    if request.method == 'POST':
        form =CustomUserCreationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')  # Replace 'home' with the URL you want to redirect to after login
    else:
        form = CustomUserCreationForm()

    return render(request, 'registration/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('login')