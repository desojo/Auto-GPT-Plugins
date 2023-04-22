"""Twitter API integrations using Tweepy."""
from typing import TypedDict, TypeVar
from dotenv import load_dotenv
from auto_gpt_plugin_template import AutoGPTPluginTemplate
from pathlib import Path
import os
import tweepy


PromptGenerator = TypeVar("PromptGenerator")

with open(str(Path(os.getcwd()) / ".env"), 'r') as fp:
    load_dotenv(stream=fp)


class Message(TypedDict):
    role: str
    content: str


class AutoGPTTwitter(AutoGPTPluginTemplate):
    """
    Twitter API integrations using Tweepy
    """

    def __init__(self):
        super().__init__()
        self.load_commands = os.getenv("TW_CONSUMER_KEY") and os.getenv("EMAIL_PASSWORD")
        self._name = "autogpt-twitter"
        self._version = "0.1.0"
        self._description = "Twitter API integrations using Tweepy."
        self.twitter_consumer_key = os.getenv("TW_CONSUMER_KEY")
        self.twitter_consumer_secret = os.getenv("TW_CONSUMER_SECRET")
        self.twitter_access_token = os.getenv("TW_ACCESS_TOKEN")
        self.twitter_access_token_secret = os.getenv("TW_ACCESS_TOKEN_SECRET")
        self.tweet_id = []
        self.tweets = []

        # Authenticating to twitter
        self.auth = tweepy.OAuth1UserHandler(
            self.twitter_consumer_key,
            self.twitter_consumer_secret,
            self.twitter_access_token,
            self.twitter_access_token_secret,
        )

        self.api = tweepy.API(self.auth)
        self.stream = tweepy.Stream(
            self.twitter_consumer_key,
            self.twitter_consumer_secret,
            self.twitter_access_token,
            self.twitter_access_token_secret,
        )

    def post_prompt(self, prompt: PromptGenerator) -> PromptGenerator:
        """This method is called just after the generate_prompt is called,
            but actually before the prompt is generated.
        Args:
            prompt (PromptGenerator): The prompt generator.
        Returns:
            PromptGenerator: The prompt generator.
        """
        if self.load_commands:
            from .twitter import (
                get_mentions,
                post_reply,
                post_tweet,
                search_twitter_user,
            )

            prompt.add_command(
                "post_tweet", "Post Tweet", {"tweet_text": "<tweet_text>"}, post_tweet
            )
            prompt.add_command(
                "post_reply",
                "Post Twitter Reply",
                {"tweet_text": "<tweet_text>", "tweet_id": "<tweet_id>"},
                post_reply,
            )
            prompt.add_command("get_mentions", "Get Twitter Mentions", {}, get_mentions)
            prompt.add_command(
                "search_twitter_user",
                "Search Twitter",
                {"target_user": "<target_user>",
                 "number_of_tweets": "<number_of_tweets>"},
                search_twitter_user,
            )

        return prompt
