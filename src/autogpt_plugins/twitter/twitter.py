"""This module contains functions for interacting with the Twitter API."""
from __future__ import annotations
from . import AutoGPTTwitter
import tweepy

plugin = AutoGPTTwitter()


def send_tweet(tweet: str) -> str:
    """Posts a tweet to twitter.
    Args:
        tweet (str): The tweet to post.
    Returns:
        str: The tweet that was posted.
    """

    _tweetID = plugin.api.update_status(status=tweet)

    return f"Success! Tweet: {_tweetID.text}"


def post_reply(tweet: str, tweet_id: int) -> str:
    """Posts a reply to a tweet.
    Args:
        tweet (str): The tweet to post.
        tweet_id (int): The ID of the tweet to reply to.
    Returns:
        str: The tweet that was posted.
    """

    replyID = plugin.api.update_status(
        status=tweet, in_reply_to_status_id=tweet_id, auto_populate_reply_metadata=True
    )

    return f"Success! Tweet: {replyID.text}"


def send_direct_message(user_id: int, message: str) -> str:
    """Sends a direct message to a user.
    Args:
        user_id (int): The ID of the user to send the message to.
        message (str): The message to send.
    Returns:
        str: The message that was sent.
    """
    _message = plugin.api.send_direct_message(user_id, message)

    return f"Success! Message: {_message.message_create['message_data']['text']}"


def like_tweet(tweet_id: int) -> str:
    """Likes a tweet.
    Args:
        tweet_id (int): The ID of the tweet to like.
    Returns:
        str: The tweet that was liked.
    """

    _tweet = plugin.api.get_status(tweet_id)
    _tweet.favorite()

    return f"Success! Liked tweet: {_tweet.text}"


def unlike_tweet(tweet_id: int) -> str:
    """Unlikes a tweet.
    Args:
        tweet_id (int): The ID of the tweet to unlike.
    Returns:
        str: The tweet that was unliked.
    """

    _tweet = plugin.api.get_status(tweet_id)
    _tweet.unfavorite()

    return f"Success! Unliked tweet: {_tweet.text}"


def retweet_tweet(tweet_id: int) -> str:
    """Retweets a tweet.
    Args:
        tweet_id (int): The ID of the tweet to retweet.
    Returns:
        str: The tweet that was retweeted.
    """

    _tweet = plugin.api.get_status(tweet_id)
    _tweet.retweet()

    return f"Success! Retweeted tweet: {_tweet.text}"


def unretweet_tweet(tweet_id: int) -> str:
    """Unretweets a tweet.
    Args:
        tweet_id (int): The ID of the tweet to unretweet.
    Returns:
        str: The tweet that was unretweeted.
    """

    _tweet = plugin.api.get_status(tweet_id)
    _tweet.unretweet()

    return f"Success! Unretweeted tweet: {_tweet.text}"


def follow_user(user_id: int) -> str:
    """Follows a user.
    Args:
        user_id (int): The ID of the user to follow.
    Returns:
        str: The user that was followed.
    """

    _user = plugin.api.get_user(user_id)
    _user.follow()

    return f"Success! Followed user: {_user.screen_name}"


def unfollow_user(user_id: int) -> str:
    """Unfollows a user.
    Args:
        user_id (int): The ID of the user to unfollow.
    Returns:
        str: The user that was unfollowed.
    """

    _user = plugin.api.get_user(user_id)
    _user.unfollow()

    return f"Success! Unfollowed user: {_user.screen_name}"


def get_mentions(count: int) -> str | None:
    """Gets the most recent mention.
    Returns:
        str | None: The most recent mention.
    """

    _tweets = plugin.api.mentions_timeline(count=count, tweet_mode="extended")

    for tweet in _tweets:
        return (
            f"@{tweet.user.screen_name} Replied: {tweet.full_text}"
            f" Tweet ID: {tweet.id}"
        )  # Returns most recent mention


def search_tweets(query: str, count: int) -> str:
    """Searches for tweets.
    Args:
        query (str): The query to search for.
        count (int): The number of tweets to get.
    Returns:
        str: The tweets that were found.
    """
    try:
        tweets = plugin.api.search_tweets(q=query, count=count)
        for tweet in tweets:
            tweet_list = tweet_list + (f"{tweet.text} - Tweet ID: {tweet.id}")  # noqa: F821 E501
        return tweet_list
    except (tweepy.RateLimitError, tweepy.TweepError) as e:
        return (f"Error searching tweets in search_tweets(): {e}")
    except Exception as e:
        return (f"Unexpected error in search_tweets(): {e}")


def get_user_tweets(user_id: int, count: int) -> str:
    """Gets the tweets of a user.
    Args:
        user_id (int): The ID of the user to get tweets for.
        count (int): The number of tweets to get.
    Returns:
        str: The tweets of the user.
    """
    try:
        tweets = plugin.api.user_timeline(user_id=user_id, count=count)
        for tweet in tweets:
            tweet_list = tweet_list + (f"{tweet.text} - Tweet ID: {tweet.id}")  # noqa: F821 E501
        return tweet_list
    except (tweepy.RateLimitError, tweepy.TweepError) as e:
        return (f"Error getting user tweets in get_user_tweets(): {e}")
    except Exception as e:
        return (f"Unexpected error in get_user_tweets(): {e}")


def get_tweet_replies(tweet_id: int, count: int) -> str:
    """Gets the replies to a tweet.
    Args:
        tweet_id (int): The ID of the tweet to get replies for.
        count (int): The number of replies to get.
    Returns:
        str: The replies to the tweet.
        """
    try:
        replies = plugin.api.search_tweets(q="to:{}".format(plugin.api.get_status(tweet_id).author.screen_name), since_id=tweet_id, count=count)  # noqa: E501
        for reply in replies:
            if hasattr(reply, 'in_reply_to_status_id_str'):
                if reply.in_reply_to_status_id_str == tweet_id:
                    tweet_list = tweet_list + (f"{reply.text} - Reply ID: {reply.id}")  # noqa: F821 E501
        return tweet_list
    except (tweepy.RateLimitError, tweepy.TweepError) as e:
        return (f"Error getting tweet replies in get_tweet_replies(): {e}")
    except Exception as e:
        return (f"Unexpected error in get_tweet_replies(): {e}")


def get_user_timeline(user_id: int, count: int) -> str:
    """Gets the timeline of a user.
    Args:
        user_id (int): The ID of the user to get the timeline for.
        count (int): The number of tweets to get.
    Returns:
        str: The timeline of the user.
    """
    try:
        timeline = plugin.api.user_timeline(user_id=user_id, count=count)
        for tweet in timeline:
            tweet_list = tweet_list + (f"{tweet.text} - Tweet ID: {tweet.id}")  # noqa: F821 E501
        return tweet_list
    except tweepy.TweepyException as e:
        return ("Error getting user timeline: {}".format(e.reason))


def get_trending_topics(count: int) -> str:
    """Gets the trending topics.
    Args:
        count (int): The number of trending topics to get.
    Returns:
        str: The trending topics.
    """
    try:
        trends = plugin.api.trends_place(1)
        for trend in trends[0]['trends'][:count]:
            tweet_list = tweet_list + (trend['name'])  # noqa: F821
        return tweet_list
    except tweepy.TweepyException as e:
        return ("Error getting trending topics: {}".format(e.reason))


def get_trending_topics_by_location(lat: float, long: float, count: int) -> str:
    """Gets the trending topics by location.
    Args:
        lat (float): The latitude of the location.
        long (float): The longitude of the location.
        count (int): The number of trending topics to get.
    Returns:
        str: The trending topics.
    """
    try:
        closest_trends = plugin.api.trends_closest(lat, long)
        trends = plugin.api.trends_place(closest_trends[0]['woeid'])
        for trend in trends[0]['trends'][:count]:
            tweet_list = tweet_list + (trend['name'])  # noqa: F821
        return tweet_list
    except tweepy.TweepyException as e:
        return ("Error getting trending topics: {}".format(e.reason))


def get_user_mentions(user_id: int, count: int) -> str:
    """Gets the mentions of a user.
    Args:
        user_id (int): The ID of the user to get mentions for.
        count (int): The number of mentions to get.
    Returns:
        str: The mentions of the user.
    """
    try:
        mentions = plugin.api.mentions_timeline(user_id=user_id, count=count)
        for mention in mentions:
            tweet_list = tweet_list + (f"{mention.text} - Mention ID: {mention.id}")  # noqa: F821 E501
        return tweet_list
    except tweepy.TweepyException as e:
        return ("Error getting user mentions: {}".format(e.reason))


def get_user_liked_tweets(user_id: int, count: int) -> str:
    """Gets the liked tweets of a user.
    Args:
        user_id (int): The ID of the user to get liked tweets for.
        count (int): The number of liked tweets to get.
    Returns:
        str: The liked tweets of the user.
    """
    try:
        liked_tweets = plugin.api.favorites(user_id=user_id, count=count)
        for tweet in liked_tweets:
            tweet_list = tweet_list + (f"{tweet.text} - Tweet ID: {tweet.id}")  # noqa: F821 E501
        return tweet_list
    except tweepy.TweepyException as e:
        return ("Error getting user's liked tweets: {}".format(e.reason))


def get_user_retweets(user_id: int, count: int) -> str:
    """Gets the retweets of a user.
    Args:
        user_id (int): The ID of the user to get retweets for.
        count (int): The number of retweets to get.
    Returns:
        str: The retweets of the user.
    """
    try:
        retweets = plugin.api.user_timeline(user_id=user_id,
                                            count=count, include_rts=True)
        for tweet in retweets:
            if hasattr(tweet, 'retweeted_status'):
                tweet_list = tweet_list + (f"{tweet.retweeted_status.text} - Retweet ID: {tweet.id}")  # noqa: F821 E501
        return tweet_list
    except tweepy.TweepyException as e:
        return ("Error getting user's retweets: {}".format(e.reason))


def get_tweet_retweeters(tweet_id: int, count: int) -> str:
    """Gets the retweeters of a tweet.
    Args:
        tweet_id (int): The ID of the tweet to get retweeters for.
        count (int): The number of retweeters to get.
    Returns:
        str: The retweeters of the tweet.
    """
    try:
        retweets = plugin.api.retweeters(tweet_id, count=count)
        for retweeter_id in retweets:
            user = plugin.api.get_user(retweeter_id)
            user_list = user_list + (f"{user.name} - Retweeter ID: {user.id}")  # noqa: F821 E501
        return user_list
    except tweepy.TweepyException as e:
        return ("Error getting tweet retweeters: {}".format(e.reason))


def search_users(query: str, count: int) -> str:
    """Searches for users.
    Args:
        query (str): The search query.
        count (int): The number of users to get.
    Returns:
        str: The users that match the search query.
    """
    try:
        users = plugin.api.search_users(query, count=count)
        for user in users:
            user_list = user_list + (f"{user.name} - User ID: {user.id}")  # noqa: F821
        return user_list
    except tweepy.TweepyException as e:
        return ("Error searching for users: {}".format(e.reason))


def get_user_follow_counts(user_id: int) -> str:
    """Gets the follow counts of a user.
    Args:
        user_id (int): The ID of the user to get follow counts for.
    Returns:
        str: The follow counts of the user.
    """
    try:
        user = plugin.api.get_user(user_id)
        return (f"Followers: {user.followers_count}; ") + (f"Following: {user.friends_count}")  # noqa: E501
    except tweepy.TweepyException as e:
        return ("Error getting user follow counts: {}".format(e.reason))


def get_user_blocked_users(count: int) -> str:
    """Gets the blocked users of the authenticated user.
    Args:
        count (int): The number of blocked users to get.
    Returns:
        str: The blocked users of the authenticated user.
    """
    try:
        blocked_users = plugin.api.get_blocked_users(count=count)
        for user in blocked_users:
            user_list = user_list + (f"{user.name} - User ID: {user.id}")  # noqa: F821
        return user_list
    except tweepy.TweepyException as e:
        return ("Error getting blocked users: {}".format(e.reason))
