# whoisbot
Very simple discord bot for assigning labels to server members

When you run it it will read the bot token from token.txt and print out the link to add it to your server. It listens for a few commands in chat:
* `!set-label <label> <user>` - associates label with a user
* `!who-is <user>` - shows the label associated with a user
* `!who-has-label <label>` - shows which user(s) have that label
