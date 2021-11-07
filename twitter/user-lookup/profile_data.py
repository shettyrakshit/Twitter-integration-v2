import json
import requests


class TwitterProfileUpdater:
    """
    """
    def __init__(self):
        """
        """
        self.url = "https://api.twitter.com/1.1/users/lookup.json?"\
            "user_id={user_id}"
        self.bearer_token = "<bearer_token>"

    def bearer_oauth(self, r):
        """
        Method required by bearer token authentication.
        """

        r.headers["Authorization"] = f"Bearer {self.bearer_token}"
        r.headers["User-Agent"] = "<User-Agent>"
        return r

    def get_data(self, profile_list):
        """
        """
        if not profile_list:
            return

        ids_ = ','.join(profile_list)
        response = requests.request("GET", self.url.format(
            user_id=ids_), auth=self.bearer_oauth,)
        if response.status_code == 200:
            response = response.json()
            self.update_db(response)

    def process_profiles(self):
        """
        """
        # list of twitter handle
        profile_list = []
        self.get_data(profile_list)

    def get_db_data(self, twitter_id):
        """
        """
        # Return current db data
        return {}

    def update_db(self, response):
        """
        """
        if not response:
            return

        for item in response:
            instance = self.get_db_data(item.get('id'))
            if not instance:
                continue

            data = {
                    'twitter_id': item.get('id'),
                    'screen_name': item.get('screen_name'),
                    'name': item.get('name', instance.get(
                        'name')) or instance.get('name'),
                    'location': item.get('location', instance.get(
                        'location')) or None,
                    'followers_count': item.get('followers_count',
                                                instance.get(
                                                    'followers_count')),
                    'following_count': item.get('friends_count', instance.get(
                        'following_count')),
                    'favourites_tweet_count': item.get(
                        'favourites_count', instance.get(
                            'favourites_tweet_count')),
                    'tweet_and_retweet_count': item.get(
                        'statuses_count', instance.get(
                            'tweet_and_retweet_count')),
                    'listed_count': item.get('listed_count', instance.get(
                        'listed_count')),
                    'language': item.get('lang', instance.get(
                        'language')) or None,
                    'protected': item.get('protected', instance.get(
                        'protected')),
                    'verified': item.get('verified', instance.get('verified')),
                    'website': instance.get('website'),
                    'bio': item.get('description', instance.get(
                        'bio')) or None,
                    'profile_image_url': item.get(
                        'profile_image_url_https', None),
                    'profile_banner_url': item.get('profile_banner_url', None),
                    'email': None
                    }

            try:
                # Website
                website = item.get('entities', {}).get('url', {}).get(
                    'urls', [])
                if website and isinstance(website, list):
                    website = website[0]
                    if website and isinstance(website, dict):
                        data['website'] = website.get(
                            'expanded_url', None) or None

            except Exception as e:
                print(e)
                data['website'] = instance.get('website')

            # Update db


def oauth_profile_update():
    """
    """
    obj = TwitterProfileUpdater()
    obj.process_profiles()
