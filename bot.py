import os
import ast
import requests  # Import requests to use for the Discord webhook
from dotenv import load_dotenv
import praw
from sqlitedict import SqliteDict

# Load environment variables from .env file
# Will not overwrite existing environment variables
load_dotenv()
db = SqliteDict("/data/reddit.sqlite", autocommit=True)

# Reddit API credentials
client_id = os.environ["CLIENT_ID"]
client_secret = os.environ["CLIENT_SECRET"]
user_agent = 'Reddit Sticky Bot'
username = os.environ["USERNAME"]
password = os.environ["PASSWORD"]

# Whitelisted users
whitelisted_users = ast.literal_eval(os.environ["WHITELIST"])
whitelisted_users_lower = [name.lower() for name in whitelisted_users]

# Discord Webhook URL
discord_webhook_url = os.environ["DISCORD_WEBHOOK_URL"]

# Initialize PRAW with your credentials
reddit = praw.Reddit(client_id=client_id,
                     client_secret=client_secret,
                     user_agent=user_agent,
                     username=username,
                     password=password)

reddit.validate_on_submit = True

bot_user = reddit.user.me()

# Subreddit to monitor
subreddit_name = os.environ["SUBREDDIT"]

# The text for the sticky comment
sticky_comment_text = """
This post contains replies from employees of Keen Games, you can see them here:

"""

def send_to_discord(message):
    """
    Sends a message to the Discord webhook.
    """
    data = {"content": message}
    response = requests.post(discord_webhook_url, json=data)
    response.raise_for_status()

def sticky_comment_on_whitelisted_user_post():
    print(f"Bot started and listening in r/{subreddit_name}")
    print(f"Whitelisted users: {whitelisted_users_lower}")
    subreddit = reddit.subreddit(subreddit_name)
    for comment in subreddit.stream.comments(skip_existing=True):
        # Check if new comment is from a whitelisted username
        if comment.author and (comment.author.name.lower() in whitelisted_users_lower):
            print(f"Found a post by whitelisted user: {comment.author.name}")
            submission = comment.submission
            existing_sticky = None
            
            # Check if post already has developer comments bot sticky
            if submission.id in db.keys():
                existing_sticky = reddit.comment(db[submission.id])
                print(f"Found bot post id: {existing_sticky.id}")
            
            if existing_sticky:
                sticky_body = existing_sticky.body
                # Append comment to template
                comment_body:str = comment.body
                comment_body_split = comment_body.split()
                # Shorten comment to first 5 words if longer
                if (len(comment_body_split) > 5):
                    comment_body = " ".join(comment_body_split[:5]) + " ..."
                sticky_comment_text_with_comment = f"{sticky_body}\n\n/u/{comment.author.name} posted a comment: [{comment_body}]({comment.permalink})"
                # Edit sticky comment with new post
                existing_sticky.edit(sticky_comment_text_with_comment)
                print(f"Edited a comment on post: {submission.title}")
                # Send notification to Discord
                send_to_discord(f"A stickied reply has been updated in r/{subreddit_name} by {comment.author.name}. [Link to comment](https://www.reddit.com{comment.permalink})")
                
            # Else, create new comment and sticky
            else:
                # Append comment to template
                comment_body:str = comment.body
                comment_body_split = comment_body.split()
                # Shorten comment to first 5 words if longer
                if (len(comment_body_split) > 5):
                    comment_body = " ".join(comment_body_split[:5]) + " ..."
                sticky_comment_text_with_comment = f"{sticky_comment_text}\n\n/u/{comment.author.name} posted a comment: [{comment_body}]({comment.permalink})"
                # Post the comment
                bot_sticky_comment = submission.reply(sticky_comment_text_with_comment)
                db[submission.id] = bot_sticky_comment.id
                # Sticky and distinguish the comment
                bot_sticky_comment.mod.distinguish(how='yes', sticky=True)
                print(f"Stickied a comment on post: {submission.title}\nPost id: {submission.id}\nComment id: {bot_sticky_comment.id}")
                # Send notification to Discord
                send_to_discord(f"A stickied reply has been posted in r/{subreddit_name} by {comment.author.name}. [Link to comment](https://www.reddit.com{comment.permalink})")

# Run the bot
sticky_comment_on_whitelisted_user_post()
