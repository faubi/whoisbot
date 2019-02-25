import discord
import asyncio
import sqlite3

client = discord.Client();
db = sqlite3.connect('names.db')
db.execute("CREATE TABLE IF NOT EXISTS names (discord_id text primary key, label text);")

print(discord.utils.oauth_url('549371343435464725', discord.Permissions(3072)))

async def send(channel, message):
	await asyncio.sleep(0.3)
	await client.send_message(channel, message)

@client.event
async def on_message(msg):
	if msg.content.startswith("!who-is "):
		name = msg.content[8:]
		member = msg.server.get_member_named(name)
		if member is None:
			await send(msg.channel, "Error: user " + name + " not found")
		else:
			cursor = db.cursor()
			cursor.execute("SELECT label FROM names WHERE discord_id=?;", (member.id,));
			result = cursor.fetchone();
			await send(msg.channel, "The user " + name + " is " + (result[0] if result is not None else "not in db"));
	if msg.content.startswith("!set-label "):
		s = msg.content[11:].split(' ', 1)
		label = s[0]
		name = s[1]
		member = msg.server.get_member_named(name)
		if member is None:
			await send(msg.channel, "Error: user " + name + " not found")
		else:
			cursor = db.cursor()
			cursor.execute("INSERT OR REPLACE INTO names(discord_id, label) VALUES(?,?);", (member.id, label))
			db.commit()
			await send(msg.channel, "Successfully set label of user " + name + " to " + label)
	if msg.content.startswith("!who-has-label "):
		label = msg.content[15:].strip()
		cursor = db.cursor()
		cursor.execute("SELECT discord_id FROM names WHERE label=?;", (label,));
		result = cursor.fetchall()
		if not result:
			await send(msg.channel, "No one has that label")
		else:
			names = []
			for user_id in result:
				user = msg.server.get_member(user_id[0])
				names.append(user.name + " (" + user.nick + ")")
			await send(msg.channel, "The user(s) with label " + label + ": " + ", ".join(names))
		

with open('token.txt') as token_file:
	token = token_file.readline().strip()

client.run(token);
