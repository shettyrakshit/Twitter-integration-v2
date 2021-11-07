from django.db import models


class TwitterCredentials(models.Model):
    """
    """
    token_id = models.AutoField(primary_key=True)
    influencer_id = models.IntegerField(null=False, blank=False, unique=True)
    profile_id = models.IntegerField(null=False, blank=False, db_index=True)
    oauth_token = models.CharField(max_length=512, null=True,
                                   blank=False, default=None)
    oauth_token_secret = models.CharField(max_length=512, null=True,
                                          blank=False, default=None)
    is_valid = models.BooleanField(default=True)
    created_at = models.DateTimeField(null=True, default=None)
    last_updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'twitter_access_token'


class TwitterProfile(models.Model):
    """
    """
    profile_id = models.AutoField(primary_key=True)
    influencer_id = models.BigIntegerField(null=False, blank=False,
                                           db_index=True, default=0)
    twitter_id = models.BigIntegerField(null=False, blank=False,
                                        db_index=True, default=0)
    screen_name = models.CharField(max_length=64, null=False, blank=False,
                                   db_index=True)
    name = models.CharField(max_length=64, null=True, blank=False,
                            default=None)
    location = models.CharField(max_length=64, null=True, blank=False,
                                default=None)
    followers_count = models.IntegerField(null=False, blank=False,
                                          default=0)
    following_count = models.IntegerField(null=False, blank=False, default=0)
    favourites_tweet_count = models.IntegerField(null=False, blank=False,
                                                 default=0)
    tweet_and_retweet_count = models.IntegerField(null=False, blank=False,
                                                  default=0)
    listed_count = models.IntegerField(null=False, blank=False, default=0)
    language = models.CharField(max_length=64, null=True, blank=False,
                                default=None)
    protected = models.BooleanField(default=False)
    verified = models.BooleanField(default=False)
    website = models.URLField(max_length=128, null=True, blank=False,
                              default=None)
    bio = models.TextField(null=True, blank=False, default=None)
    profile_image_url = models.CharField(max_length=512, null=True,
                                         blank=False,  default=None)
    profile_banner_url = models.CharField(max_length=512, null=True,
                                          blank=False, default=None)
    email = models.CharField(max_length=255, null=True, blank=False,
                             default=None)
    twitter_account_created_on = models.DateTimeField(null=True, default=None)
    enabled = models.BooleanField(default=True)
    connected = models.BooleanField(default=True)
    created_on = models.DateTimeField(null=True, default=None)
    last_updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'twitter_profile'
