import os
import ast
from dotenv import load_dotenv
import praw

# Load environment variables from .env file
# Will not overwrite existing environment variables
load_dotenv()

# Reddit API credentials
client_id = os.environ["CLIENT_ID"]
client_secret = os.environ["CLIENT_SECRET"]
user_agent = 'Reddit Sticky Bot'
username = os.environ["USERNAME"]
password = os.environ["PASSWORD"]

# Whitelisted users
whitelisted_users = ast.literal_eval(os.environ["WHITELIST"])
whitelisted_users_lower = [name.lower() for name in whitelisted_users]

# Initialize PRAW with your credentials
reddit = praw.Reddit(client_id=client_id,
                     client_secret=client_secret,
                     user_agent=user_agent,
                     username=username,
                     password=password)

# Subreddit to monitor
subreddit_name = os.environ["SUBREDDIT"]

# The text for the sticky comment
sticky_comment_text = """
This post is from an approved developer. Here's some more information:
[Link to additional resources or information]
"""

def sticky_comment_on_whitelisted_user_post():
    print(f"Bot started and listening in r/{subreddit_name}")
    subreddit = reddit.subreddit(subreddit_name)
    for submission in subreddit.stream.submissions(skip_existing=True):
        if submission.author and (submission.author.name.lower() in whitelisted_users_lower):
            print(f"Found a post by whitelisted user: {submission.author.name}")
            # Post the comment
            comment = submission.reply(sticky_comment_text)
            # Sticky the comment
            comment.mod.distinguish(how='yes', sticky=True)
            print(f"Stickied a comment on post: {submission.title}")

# Run the bot
sticky_comment_on_whitelisted_user_post()
