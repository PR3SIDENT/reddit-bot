import praw

# Reddit API credentials
client_id = 'YOUR_CLIENT_ID'
client_secret = 'YOUR_CLIENT_SECRET'
user_agent = 'bot by /u/YOUR_USERNAME'
username = 'YOUR_USERNAME'
password = 'YOUR_PASSWORD'

# Whitelisted users
whitelisted_users = ['User1', 'User2', 'DeveloperUsername', 'CommunityManager']

# Initialize PRAW with your credentials
reddit = praw.Reddit(client_id=client_id,
                     client_secret=client_secret,
                     user_agent=user_agent,
                     username=username,
                     password=password)

# Subreddit to monitor
subreddit_name = 'YOUR_SUBREDDIT'

# The text for the sticky comment
sticky_comment_text = """
This post is from an approved developer. Here's some more information:
[Link to additional resources or information]
"""

def sticky_comment_on_whitelisted_user_post():
    subreddit = reddit.subreddit(subreddit_name)
    for submission in subreddit.stream.submissions():
        if submission.author and submission.author.name in whitelisted_users:
            print(f"Found a post by whitelisted user: {submission.author.name}")
            # Post the comment
            comment = submission.reply(sticky_comment_text)
            # Sticky the comment
            comment.mod.distinguish(how='yes', sticky=True)
            print(f"Stickied a comment on post: {submission.title}")

# Run the bot
sticky_comment_on_whitelisted_user_post()
