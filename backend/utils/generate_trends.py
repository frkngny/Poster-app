import django
import os
import sys
from post.models import Post
from datetime import datetime, timedelta, timezone

sys.path.append(os.path.join(os.path.abspath(os.path.dirname(__file__)), '..'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', "poster.settings")
django.setup()


def get_date_range(date_range_hours):
    now = datetime.now(timezone.utc)
    from_date = now - timedelta(hours=date_range_hours)
    return from_date

def generate(date_range_hours):
    def extract_hashtag(text):
        hashtag_list = []
        for word in text.split():
            if word[0] == '#':
                hashtag_list.append(word)
        return hashtag_list
    from_date = get_date_range(date_range_hours)
    trends = {}
    for post in Post.objects.filter(created_at__gte=from_date).filter(body__icontains='#'):
        hashtags = extract_hashtag(post.body)
        if len(hashtags) > 0:
            for hashtag in hashtags:
                if hashtag in trends.keys():
                    trends[hashtag] += 1
                else:
                    trends[hashtag] = 1
                    
    trends_sorted = sorted(trends.items(), key=lambda x:x[1], reverse=True)
    return trends_sorted

