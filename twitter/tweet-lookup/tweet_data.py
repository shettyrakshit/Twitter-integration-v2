import requests
import json
import re
import time
from requests_oauthlib import OAuth1Session, OAuth1
from datetime import datetime

url = 'https://api.twitter.com/2/users/{twitter_id}/tweets'
params = {
        "expansions": "attachments.poll_ids,attachments.media_keys,author_id,"\
        "entities.mentions.username,geo.place_id,in_reply_to_user_id",
        "media.fields": "duration_ms,height,media_key,preview_image_url,type,url,width,"\
                "public_metrics,non_public_metrics,organic_metrics,alt_text",
        "tweet.fields": "attachments,author_id,context_annotations,conversation_id,created_at,"\
                "entities,geo,id,in_reply_to_user_id,lang,non_public_metrics,public_metrics,"\
                "organic_metrics,possibly_sensitive,referenced_tweets,"\
                "reply_settings,source,text,withheld",
        "place.fields": "contained_within,country,country_code,full_name,geo,id,name,place_type",
        "poll.fields": "duration_minutes,end_datetime,id,options,voting_status",
        "user.fields": "created_at,description,entities,id,location,name,pinned_tweet_id,"\
                "profile_image_url,protected,public_metrics,url,username,verified,withheld",
        "max_results": 35}
non_oauth_url = 'https://api.twitter.com/2/users/{twitter_id}/tweets?expansions=attachments.poll_ids,'\
        'attachments.media_keys,author_id,entities.mentions.username,geo.place_id,in_reply_to_user_id'\
        '&tweet.fields=attachments,author_id,context_annotations,conversation_id,created_at,'\
        'entities,geo,id,in_reply_to_user_id,lang,public_metrics,'\
        'possibly_sensitive,referenced_tweets,'\
        'reply_settings,source,text,withheld'\
        '&media.fields=duration_ms,height,media_key,preview_image_url,type,url,width,'\
        'public_metrics,alt_text'\
        '&place.fields=contained_within,country,country_code,full_name,geo,id,name,place_type'\
        '&poll.fields=duration_minutes,end_datetime,id,options,voting_status&'\
        '&user.fields=created_at,description,entities,id,location,name,pinned_tweet_id,'\
        'profile_image_url,protected,public_metrics,url,username,verified,withheld'\
        '&max_results=10&exclude=retweets,replies'

client_token = '<client_token>'
client_secret = '<client_secret>'
bearer_token = '<bearer_token>'


def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """
    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "<User-Agent>"
    return r


def check_tweet_present(tweet_id, profile_id):
    """
    """
    # Check tweet id if tweet present in db
    return


def get_tweet_data(media_id):
    """
    """
    # tweet data in db
    return {}


def insert_tweet(data_to_insert, is_oauth):
    """
    """
    # Insert tweet in db
    return


def update_tweet(data_to_insert, media_id):
    """
    """
    previous_data = get_tweet_data(media_id)
    if not previous_data:
        return

    # Update tweet data in db..


def update_table(tweet_metrics, is_oauth):
    """
    """
    media_id = check_tweet_present(tweet_metrics['id'],
                                   tweet_metrics['profile_id'])
    if media_id:
        update_tweet(data_to_insert=tweet_metrics,
                     media_id=media_id)
    else:
        media_id = insert_tweet(data_to_insert=tweet_metrics,
                                is_oauth=is_oauth)


def get_tweet_analytics(twitter_id,
                        influencer_id, profile_id,
                        oauth_token, oauth_token_secret,
                        screen_name, is_oauth):
    """
    """
    oauth = OAuth1Session(client_token,
                          client_secret=client_secret,
                          resource_owner_key=oauth_token,
                          resource_owner_secret=oauth_token_secret)
    response = oauth.get(url.format(twitter_id=twitter_id),
                         params=params)

    if response.status_code == 200:
        response = response.json()
        tweets_list = response.get('data', [])
        includes = response.get('includes', {})
        places = includes.get('places', [])
        polls = includes.get('polls', [])
        media_ = includes.get('media', [])

        if not tweets_list:
            return

        for tweet in tweets_list:
            tweet_metrics = tweet
            if not tweet_metrics.get('id', None):
                continue
            tweet_metrics['id'] = int(tweet_metrics['id'])

            tweet_metrics['influencer_id'] = influencer_id
            tweet_metrics['profile_id'] = profile_id
            if tweet_metrics.get('created_at', None):
                try:
                    tweet_metrics['created_at'] = datetime.strptime(
                            tweet_metrics['created_at'],
                            "%Y-%m-%dT%H:%M:%S.000Z").strftime(
                                    "%Y-%m-%d %H:%M:%S")
                except:
                    tweet_metrics['created_at'] = None

            else:
                tweet_metrics['created_at'] = None
            tweet_metrics['permalink'] = 'https://twitter.com/{username}/status/{tweet_id}'.format(
                    username=screen_name, tweet_id=tweet_metrics.get('id', 0))
            tweet_metrics['retweet_count'] = tweet_metrics.get(
                    'public_metrics', {}).get('retweet_count', 0)
            tweet_metrics['reply_count'] = tweet_metrics.get(
                    'public_metrics', {}).get('reply_count', 0)
            tweet_metrics['like_count'] = tweet_metrics.get(
                    'public_metrics', {}).get('like_count', 0)
            tweet_metrics['quote_count'] = tweet_metrics.get(
                    'public_metrics', {}).get('quote_count', 0)
            tweet_metrics['impression_count'] = tweet_metrics.get(
                    'non_public_metrics', {}).get('impression_count', 0)
            tweet_metrics['user_profile_clicks'] = tweet_metrics.get(
                    'non_public_metrics', {}).get('user_profile_clicks', 0)
            tweet_metrics['url_link_clicks'] = tweet_metrics.get(
                    'non_public_metrics', {}).get('url_link_clicks', 0)

            tweet_metrics['video_views'] = 0
            tweet_metrics['playback_0_count'] = 0
            tweet_metrics['playback_25_count'] = 0
            tweet_metrics['playback_50_count'] = 0
            tweet_metrics['playback_75_count'] = 0
            tweet_metrics['playback_100_count'] = 0
            tweet_metrics['media_details'] = []
            tweet_metrics['media_type'] = None
            if tweet_metrics.get('attachments', {}).get('media_keys', []):
                media_keys = tweet_metrics.get('attachments', {}).get(
                        'media_keys', [])
                for data in media_:
                    if data.get('media_key', None) in media_keys:
                        url_ = data.get('url', None) or data.get('preview_image_url', None)
                        media_text_ = data.get('alt_text', None)
                        tweet_metrics['media_details'].append(
                                {'media_url': url_, 'media_text': media_text_})
                        tweet_metrics['media_type'] = data.get('type', None)
                        tweet_metrics['video_views'] = data.get(
                            'public_metrics', {}).get(
                                'view_count', 0)
                        tweet_metrics['playback_0_count'] = data.get(
                            'organic_metrics', {}).get(
                                'playback_0_count', 0)
                        tweet_metrics['playback_25_count'] = data.get(
                            'organic_metrics', {}).get(
                                'playback_25_count', 0)
                        tweet_metrics['playback_50_count'] = data.get(
                            'organic_metrics', {}).get(
                                'playback_50_count', 0)
                        tweet_metrics['playback_75_count'] = data.get(
                            'organic_metrics', {}).get(
                                'playback_75_count', 0)
                        tweet_metrics['playback_100_count'] = data.get(
                            'organic_metrics', {}).get(
                                'playback_100_count', 0)

            tweet_metrics['engagement'] = tweet_metrics['retweet_count'] + \
                tweet_metrics['reply_count'] + tweet_metrics['like_count'] +\
                tweet_metrics['quote_count']

            tweet_metrics['reply_settings'] = tweet_metrics.get(
                    'reply_settings', None)
            tweet_metrics['lang'] = tweet_metrics.get('lang', None)

            hashtags_mentioned = tweet_metrics.get(
                    'entities', {}).get('hashtags', [])
            hashtags_mentioned = ['#' + hashtag.get('tag') for hashtag in hashtags_mentioned\
                if 'tag' in hashtag]
            hashtags_mentioned = ','.join(hashtags_mentioned)
            tweet_metrics['hashtags_mentioned'] = None
            if hashtags_mentioned:
                tweet_metrics['hashtags_mentioned'] = hashtags_mentioned

            accounts_mentioned = tweet_metrics.get(
                    'entities', {}).get('mentions', [])
            accounts_mentioned = ['@' + mention.get('username') for mention in accounts_mentioned\
                    if 'username' in mention]
            accounts_mentioned = ','.join(accounts_mentioned)
            tweet_metrics['accounts_mentioned'] = None
            if accounts_mentioned:
                tweet_metrics['accounts_mentioned'] = accounts_mentioned

            tweet_metrics['text'] = None
            
            tweet_metrics['poll_id'] = []
            tweet_metrics['poll_options'] = []
            tweet_metrics['poll_duration_minutes'] = None
            tweet_metrics['poll_voting_status'] = None
            tweet_metrics['poll_end_time'] = None
            tweet_metrics['tweet_type'] = 'tweet'
            if tweet_metrics.get('attachments', {}).get('poll_ids', []):
                tweet_metrics['tweet_type'] = 'poll'
                tweet_metrics['poll_id'] = tweet_metrics.get(
                        'attachments', {}).get('poll_ids', [])
                poll_id = tweet_metrics['poll_id'][0]
                for poll in polls:
                    if poll.get('id', None) and poll.get('id', None) == poll_id:
                        tweet_metrics['poll_options'] = poll.get('options', [])
                        tweet_metrics['poll_duration_minutes'] = poll.get('duration_minutes', None)
                        tweet_metrics['poll_voting_status'] = poll.get('voting_status', None)
                        if poll.get('end_datetime', None):
                            try:
                                tweet_metrics['poll_end_time'] = datetime.strptime(
                                        poll['end_datetime'], "%Y-%m-%dT%H:%M:%S.000Z").strftime(
                                                "%Y-%m-%d %H:%M:%S")

                            except:
                                tweet_metrics['poll_end_time'] = None

            tweet_metrics['in_reply_to_user_id'] = tweet_metrics.get('in_reply_to_user_id', None)
            if tweet_metrics['in_reply_to_user_id']:
                tweet_metrics['in_reply_to_user_id'] = int(tweet_metrics['in_reply_to_user_id'])
            tweet_metrics['possibly_sensitive'] = tweet_metrics.get('possibly_sensitive', False)
            tweet_metrics['genre'] = tweet_metrics.get('context_annotations', [])

            tweet_metrics['location'] = None
            tweet_metrics['location_type'] = None
            tweet_metrics['location_details'] = None
            tweet_metrics['country'] = None
            if tweet_metrics.get('geo', {}).get('place_id', None):
                place_id = tweet_metrics.get('geo', {}).get('place_id', None)
                for place in places:
                    if place.get('id', None) and place.get('id', None) == place_id:
                        tweet_metrics['location'] = place.get('name', None)
                        tweet_metrics['location_type'] = place.get('place_type', None)
                        tweet_metrics['location_details'] = place.get('full_name', None)
                        tweet_metrics['country'] = place.get('country', None)

            tweet_metrics['source'] = tweet_metrics.get('source', None)

            if tweet_metrics.get('referenced_tweets', []):
                referenced_tweet_ = tweet_metrics.get('referenced_tweets', [])
                if isinstance(referenced_tweet_[0], dict) and 'type' in referenced_tweet_[0]:
                    tweet_metrics['tweet_type'] = referenced_tweet_[0]['type']
                tweet_metrics['referenced_tweets'] = referenced_tweet_

            else:
                tweet_metrics['referenced_tweets'] = []

            tweet_metrics['urls_mentioned'] = None
            mentioned_urls = tweet_metrics.get('entities', {}).get('urls', [])
            regex = '^(https://twitter.com/)+(\w|\_|\-|\.)+(/status)'
            mentioned_urls = [urls_.get('expanded_url') for urls_ in mentioned_urls if not re.search(
                regex, urls_.get('expanded_url', ''))]
            mentioned_urls = ','.join(mentioned_urls)
            if mentioned_urls:
                tweet_metrics['urls_mentioned'] = mentioned_urls

            # Update table
            update_table(tweet_metrics, is_oauth)

    # If twitter access revoked
    elif response.status_code == 401 and is_oauth:
        # Update in db that user has revoked twitter permissions
        return


def get_user_details():
    """
    """
    # Retuen access token, user details etc..
    # twitter_id, influencer_id, profile_id, 
    # oauth_token, oauth_token_secret, screen_name
    return


def media_update():
    """
    """
    user_data = get_user_details()

    for twitter_id, influencer_id, profile_id,\
            oauth_token, oauth_token_secret, screen_name in user_data:

        get_tweet_analytics(twitter_id=twitter_id,
                            influencer_id=influencer_id,
                            profile_id=profile_id,
                            oauth_token=oauth_token,
                            oauth_token_secret=oauth_token_secret,
                            screen_name=screen_name,
                            is_oauth=True)
