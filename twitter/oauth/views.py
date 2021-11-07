import requests
from django.http import HttpResponseRedirect
from rest_framework.views import APIView
from requests_oauthlib import OAuth1, OAuth1Session
from datetime import datetime
from .serializers import TwitterCredentialsSerializer, TwitterProfileSerializer
from .models import TwitterCredentials, TwitterProfile


class SocialConnect:

    def __init__(self, influencer_id, version='v1',
                 oauth_token=None, oauth_verifier=None):
        self.influencer_id = influencer_id
        self.profile_id = None
        self.version = version if version in ('v1', 'v2') else 'v1'
        self.oauth_token = oauth_token
        self.oauth_verifier = oauth_verifier


class TwitterConnect(SocialConnect):
    """
    """
    consumer_key = '<consumer_key>'
    consumer_secret = '<consumer_secret>'
    oauth_access_url = 'https://api.twitter.com/oauth/access_token'
    profile_url = 'https://api.twitter.com/1.1/users/'\
        'show.json?user_id={user_id}'
    client_oauth_token = None
    client_oauth_token_secret = None
    user_id = None
    screen_name = None
    connection_status = None

    def get_access_token(self):
        """
        """
        # Returns Oauth access credentials
        oauth = OAuth1Session(self.consumer_key,
                              client_secret=self.consumer_secret,
                              resource_owner_key=self.oauth_token,
                              verifier=self.oauth_verifier)

        try:
            oauth_tokens = oauth.fetch_access_token(self.oauth_access_url)

            if isinstance(oauth_tokens, dict) and oauth_tokens:
                self.client_oauth_token = oauth_tokens.get('oauth_token', None)
                self.client_oauth_token_secret = oauth_tokens.get(
                    'oauth_token_secret', None)
                self.user_id = oauth_tokens.get('user_id', None)
                self.screen_name = oauth_tokens.get('screen_name', None)

                if not self.client_oauth_token or not\
                        self.client_oauth_token_secret:
                    self.connection_status = 'twitter_access_token_error'
                    return

            else:
                self.connection_status = 'twitter_access_token_error'
                return

        except Exception as e:
            print(e)
            self.connection_status = 'twitter_access_token_error'
            return

        # Store profile data
        profile_response = self.get_profile_data()
        if profile_response == 'error':
            return

        # Store Oauth credentials
        self.store_oauth_credentials()

    def get_profile_data(self):
        """
        """
        auth = OAuth1(self.consumer_key,
                      client_secret=self.consumer_secret,
                      resource_owner_key=self.client_oauth_token,
                      resource_owner_secret=self.client_oauth_token_secret)
        response = requests.get(self.profile_url.format(
            user_id=self.user_id), auth=auth)

        if response.status_code == 200:
            response = response.json()

        else:
            self.connection_status = 'profile_data_error'
            return 'error'

        store_user = self.store_profile_data(response)
        return store_user

    def store_profile_data(self, response):
        """
        """
        self.twitter_id = response.get('id')
        if self.check_one_to_one_link():
            self.connection_status = 'different_account'
            return 'error'

        if self.check_connected_to_other_influencer():
            self.connection_status = 'twitter_existing_account'
            return 'error'

        data = {'twitter_id': self.twitter_id,
                'screen_name': response.get('screen_name'),
                'name': response.get('name', None) or None,
                'location': response.get('location', None) or None,
                'followers_count': response.get('followers_count', 0) or 0,
                'following_count': response.get('friends_count', 0) or 0,
                'favourites_tweet_count': response.get(
                    'favourites_count', 0) or 0,
                'tweet_and_retweet_count': response.get(
                    'statuses_count', 0) or 0,
                'listed_count': response.get('listed_count', 0) or 0,
                'language': response.get('lang', None) or None,
                'protected': response.get('protected', False) or False,
                'verified': response.get('verified', False) or False,
                'website': None,
                'bio': response.get('description', None) or None,
                'profile_image_url': response.get('profile_image_url_https',
                                                  None) or None,
                'profile_banner_url': response.get('profile_banner_url',
                                                   None) or None,
                'twitter_account_created_on': None,
                'created_on': datetime.now(),
                'influencer_id': self.influencer_id,
                'enabled': True,
                'connected': True}

        try:
            # Website
            website = response.get('entities', {}).get('url', {}).get(
                'urls', [])
            if website and isinstance(website, list):
                website = website[0]
                if website and isinstance(website, dict):
                    data['website'] = website.get('expanded_url', None) or None

            # Account created on
            if response.get('created_at', None):
                data['twitter_account_created_on'] = datetime.strftime(
                        datetime.strptime(response.get('created_at'),
                                          '%a %b %d %H:%M:%S +0000 %Y'),
                        '%Y-%m-%d %H:%M:%S')

        except Exception as e:
            print(e)
            pass

        if self.check_if_exists():
            profile_ = TwitterProfile.objects.get(
                influencer_id=self.influencer_id,
                twitter_id=self.twitter_id)
            serializer = TwitterProfileSerializer(profile_, data=data)

        else:
            serializer = TwitterProfileSerializer(data=data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
        self.profile_id = serializer.data['profile_id']
        self.connection_status = 'successful'

    def check_one_to_one_link(self):
        """
        """
        if TwitterProfile.objects.filter(influencer_id=self.influencer_id,
                                         enabled=1, connected=1).exclude(
                                            twitter_id=self.twitter_id):
            return True

        return False

    def check_connected_to_other_influencer(self):
        """
        """
        if TwitterProfile.objects.filter(twitter_id=self.twitter_id,
                                         enabled=1, connected=1).exclude(
                    influencer_id=self.influencer_id):
            return True

        return False

    def check_if_exists(self):
        """
        """
        if TwitterProfile.objects.filter(influencer_id=self.influencer_id,
                                         connected=1).exclude(
                                            twitter_id=self.twitter_id)\
            or not TwitterProfile.objects.filter(
                                influencer_id=self.influencer_id):
            return False

        return True

    def store_oauth_credentials(self):
        """
        """
        data = {'influencer_id': self.influencer_id,
                'profile_id': self.profile_id,
                'oauth_token': self.client_oauth_token,
                'oauth_token_secret': self.client_oauth_token_secret,
                'is_valid': True,
                'created_at': datetime.now()
                }
        if TwitterCredentials.objects.filter(influencer_id=self.influencer_id,
                                             profile_id=self.profile_id):
            oauth_ = TwitterCredentials.objects.get(
                influencer_id=self.influencer_id,
                profile_id=self.profile_id)
            serializer = TwitterCredentialsSerializer(oauth_, data=data)

        else:
            serializer = TwitterCredentialsSerializer(data=data)

        if serializer.is_valid(raise_exception=False):
            serializer.save()


class SocialConnectView(APIView):
    """
    Replace redirect url as per your requirement
    """
    def get(self, request, platform=None, version=None):
        """
        Get request
        """
        query_params = request.query_params

        # Successful request
        state = query_params.get('state')
        influencer_id = None
        if state:
            state = state.split(',')
            influencer_id = state[0]

        oauth_token = query_params.get('oauth_token')
        oauth_verifier = query_params.get('oauth_verifier')
        social_platform = TwitterConnect(
                influencer_id=influencer_id,
                oauth_token=oauth_token,
                oauth_verifier=oauth_verifier)

        redirect_to_url = '<default redirect url>'
        if state[-1] == 'web':
            redirect_to_url = '<web redirect url>'

        if state[-1] == 'betaweb':
            redirect_to_url = '<beta-web redirect url>'

        try:
            social_platform.get_access_token()
        except Exception as e:
            return HttpResponseRedirect(redirect_to='<default redirect url>')

        connection_status = social_platform.connection_status
        if not connection_status:
            connection_status = 'twitter_access_token_error'
        redirect_to_url = '<redirect url on success>' + connection_status

        return HttpResponseRedirect(redirect_to=redirect_to_url)
