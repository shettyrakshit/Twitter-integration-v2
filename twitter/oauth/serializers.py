from rest_framework import serializers
from .models import TwitterCredentials, TwitterProfile


class TwitterCredentialsSerializer(serializers.ModelSerializer):
    """
    """
    class Meta:
        model = TwitterCredentials
        fields = ('token_id', 'influencer_id', 'profile_id', 'oauth_token',
                  'oauth_token_secret', 'is_valid', 'created_at',
                  'last_updated_at')

    def create(self, validated_data):
        """
        """
        return TwitterCredentials.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        """
        instance.oauth_token = validated_data.get('oauth_token')
        instance.oauth_token_secret = validated_data.get('oauth_token_secret')
        instance.is_valid = validated_data.get('is_valid')
        instance.created_at = instance.created_at

        instance.save()
        return instance


class TwitterProfileSerializer(serializers.ModelSerializer):
    """
    """
    class Meta:
        model = TwitterProfile
        fields = ('profile_id', 'influencer_id', 'twitter_id', 'screen_name',
                  'name', 'location', 'followers_count', 'following_count',
                  'favourites_tweet_count', 'tweet_and_retweet_count',
                  'listed_count', 'language', 'protected',
                  'verified', 'website', 'bio', 'profile_image_url',
                  'profile_banner_url', 'twitter_account_created_on',
                  'enabled', 'connected', 'created_on', 'last_updated_at')

    def create(self, validated_data):
        """
        """
        return TwitterProfile.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        """
        instance.screen_name = validated_data.get('screen_name')
        instance.name = validated_data.get('name')
        instance.location = validated_data.get('location')
        instance.followers_count = validated_data.get('followers_count')
        instance.following_count = validated_data.get('following_count')
        instance.favourites_tweet_count = validated_data.get(
            'favourites_tweet_count')
        instance.tweet_and_retweet_count = validated_data.get(
            'tweet_and_retweet_count')
        instance.listed_count = validated_data.get('listed_count')
        instance.language = validated_data.get('language')
        instance.protected = validated_data.get('protected')
        instance.verified = validated_data.get('verified')
        instance.website = validated_data.get('website')
        instance.bio = validated_data.get('bio')
        instance.profile_image_url = validated_data.get('profile_image_url')
        instance.profile_banner_url = validated_data.get('profile_banner_url')
        instance.created_on = instance.created_on
        instance.enabled = validated_data.get('enabled')
        instance.connected = validated_data.get('connected')

        instance.save()
        return instance
