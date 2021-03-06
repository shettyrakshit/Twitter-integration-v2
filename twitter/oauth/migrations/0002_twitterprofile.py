# Generated by Django 3.2.8 on 2021-11-07 04:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oauth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TwitterProfile',
            fields=[
                ('profile_id', models.AutoField(primary_key=True, serialize=False)),
                ('influencer_id', models.BigIntegerField(db_index=True, default=0)),
                ('twitter_id', models.BigIntegerField(db_index=True, default=0)),
                ('screen_name', models.CharField(db_index=True, max_length=64)),
                ('name', models.CharField(default=None, max_length=64, null=True)),
                ('location', models.CharField(default=None, max_length=64, null=True)),
                ('followers_count', models.IntegerField(default=0)),
                ('following_count', models.IntegerField(default=0)),
                ('favourites_tweet_count', models.IntegerField(default=0)),
                ('tweet_and_retweet_count', models.IntegerField(default=0)),
                ('listed_count', models.IntegerField(default=0)),
                ('language', models.CharField(default=None, max_length=64, null=True)),
                ('protected', models.BooleanField(default=False)),
                ('verified', models.BooleanField(default=False)),
                ('website', models.URLField(default=None, max_length=128, null=True)),
                ('bio', models.TextField(default=None, null=True)),
                ('profile_image_url', models.CharField(default=None, max_length=512, null=True)),
                ('profile_banner_url', models.CharField(default=None, max_length=512, null=True)),
                ('email', models.CharField(default=None, max_length=255, null=True)),
                ('twitter_account_created_on', models.DateTimeField(default=None, null=True)),
                ('enabled', models.BooleanField(default=True)),
                ('connected', models.BooleanField(default=True)),
                ('created_on', models.DateTimeField(default=None, null=True)),
                ('last_updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'twitter_profile',
            },
        ),
    ]
