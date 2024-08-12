# Environment Variables

### Set these environment variables by either editing the .env file before building the Docker image or adding them in the Docker container's settings

 - CLIENT_ID `# Reddit application client ID`
 - CLIENT_SECRET `# Reddit application client secret`
 - USERNAME `# Bot's Reddit username`
 - PASSWORD `# Bot's Reddit password`
 - WHITELIST `# List of Reddit usernames that will have their posts stickied. Format: ["Username1", "Username2"]`
 - SUBREDDIT `# Subreddit to watch for posts. Do not include the r/`
 - DISCORD_WEBHOOK_URL `# Optional: Discord logging Webhook URL`

Here is an example of what the bot does for the attached subreddit...
![image](https://github.com/user-attachments/assets/dbdd562e-3066-44ac-a1a8-54c9f01ac3d1)
