import discord
import os
import re
import random
from datetime import datetime
from lectures import lecture2, lecture3, lecture4  # Assume these are lists of question/term dictionaries

my_secret = os.getenv('apikey')
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# Global variable to store the current active item (question or term)
active_item = None

# Global variable to store the current lecture material; default to lecture3
current_lecture = lecture3

async def send_new_item(channel):
    """Selects a random item from the current lecture and sends it as an embed."""
    global active_item, current_lecture
    active_item = random.choice(current_lecture)
    embed = discord.Embed(
        color=discord.Color.orange(),
        timestamp=datetime.utcnow()
    )
    # Check if the active item is a multiple-choice question
    if "question" in active_item:
        embed.title = "Multiple Choice Question"
        embed.add_field(name="Question", value=active_item["question"], inline=False)
        embed.add_field(name="A", value=active_item["options"]["A"], inline=False)
        embed.add_field(name="B", value=active_item["options"]["B"], inline=False)
        embed.add_field(name="C", value=active_item["options"]["C"], inline=False)
    # Otherwise, assume it's a term-definition pair
    elif "term" in active_item:
        embed.title = "Lecture Term"
        embed.add_field(name="Term", value=active_item["term"], inline=False)
        embed.add_field(name="Definition", value=active_item["definition"], inline=False)
    await channel.send(embed=embed)

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
    # Post the first item when the bot starts up
    channel = discord.utils.get(client.get_all_channels(), name="general")
    if channel:
        await send_new_item(channel)
    else:
        print("General channel not found.")

@client.event
async def on_message(message):
    global active_item, current_lecture
    # Ignore messages from the bot itself
    if message.author == client.user:
        return

    # Help command
    if message.content.startswith('$help'):
        help_embed = discord.Embed(
            title="Bot Commands Help",
            description=(
                "**$msg <user_id or mention> <message>** - Sends a DM to the specified user.\n"
                "**$cool** - Receive a cool, positive message from the bot.\n"
                "**$setlecture <2|3|4>** - Choose lecture material."
            ),
            color=discord.Color.blue(),
            timestamp=datetime.utcnow()
        )
        await message.channel.send(embed=help_embed)
        return

    # Cool command
    if message.content.startswith('$cool'):
        cool_messages = [
            "Stay frosty, my friend!",
            "Keep calm and code on.",
            "May your code be bug-free!",
            "Coding is the new magic!"
        ]
        random_message = random.choice(cool_messages)
        cool_embed = discord.Embed(
            title="Cool Vibes",
            description=random_message,
            color=discord.Color.purple(),
            timestamp=datetime.utcnow()
        )
        await message.channel.send(embed=cool_embed)
        return

    # Direct message command
    if message.content.startswith('$msg'):
        parts = message.content.split(maxsplit=2)
        if len(parts) < 3:
            await message.channel.send("Usage: $msg <user_id or mention> <message>")
            return

        user_identifier = parts[1]
        msg_content = parts[2]

        # Try to extract a user ID from a mention (e.g., <@123456789012345678>)
        user_id = None
        mention_regex = r'<@!?(\d+)>'
        match = re.match(mention_regex, user_identifier)
        if match:
            user_id = int(match.group(1))
        else:
            try:
                user_id = int(user_identifier)
            except ValueError:
                await message.channel.send("Invalid user identifier. Please use a valid user ID or mention.")
                return

        try:
            target_user = await client.fetch_user(user_id)
        except discord.NotFound:
            await message.channel.send("User not found!")
            return
        except discord.HTTPException:
            await message.channel.send("An error occurred while fetching the user.")
            return

        try:
            dm_embed = discord.Embed(
                title="You've Got a Message!",
                description=msg_content,
                color=discord.Color.green(),
                timestamp=datetime.utcnow()
            )
            await target_user.send(embed=dm_embed)
            confirm_embed = discord.Embed(
                title="Message Sent!",
                description=f"Your message was sent to {target_user.name}.",
                color=discord.Color.green(),
                timestamp=datetime.utcnow()
            )
            await message.channel.send(embed=confirm_embed)
        except discord.Forbidden:
            await message.channel.send("I don't have permission to send DMs to that user.")
        return

    # Command to set lecture material
    if message.content.startswith('$setlecture'):
        parts = message.content.split()
        if len(parts) < 2:
            await message.channel.send("Usage: $setlecture <2|3|4>")
            return
        lecture_num = parts[1]
        if lecture_num == "2":
            current_lecture = lecture2
        elif lecture_num == "3":
            current_lecture = lecture3
        elif lecture_num == "4":
            current_lecture = lecture4
        else:
            await message.channel.send("Invalid lecture number. Please choose 2, 3, or 4.")
            return
        await message.channel.send(f"Lecture material set to Lecture {lecture_num}.")
        # Immediately send a new item from the selected lecture
        await send_new_item(message.channel)
        return

    # Answer checking in the "general" channel: only check if the active item is a multiple-choice question
    if message.channel.name == "general" and active_item and "correct" in active_item:
        if message.content.strip().lower() in ["a", "b", "c"]:
            user_answer = message.content.strip().upper()
            if user_answer == active_item["correct"]:
                await message.channel.send(f"Good job {message.author.mention}, you're right!")
            else:
                correct_letter = active_item["correct"]
                correct_option = active_item["options"][correct_letter]
                await message.channel.send(
                    f"Close but you're wrong, {message.author.mention}. The correct answer is {correct_letter}: {correct_option}.\n{active_item['explanation']}"
                )
            # Reset the active item and send a new one immediately
            active_item = None
            await send_new_item(message.channel)

client.run(my_secret)
