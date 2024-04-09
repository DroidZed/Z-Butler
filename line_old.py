from sys import stderr
from traceback import print_exception
from discord.ext import commands, tasks
from datetime import datetime, timedelta

intents = discord.Intents.all()

bot = commands.Bot(command_prefix="?", intents=intents)
bot.remove_command("help")

TARGET_CATEGORY_IDS = {
    1205767730465218590,
    1205767637091753994,
    1145517559727263855,
    1145517561493082234,
    1145517563829309470,
    1148764057587945490,
    1145517567876800592,
    1145517569336422470,
    1145517610176368670,
    1145517572024979596,
    1148764123920867559,
}

ORDER_CHANNEL_ID = 1145517576642887791

line_messages = {}


@bot.event
async def on_ready():
    print(f"{bot.user.name} has started line timer!")
    # Start the scheduled task
    purge_and_send_line.start()
    # Start the background task
    update_voice_channel_counts.start()


@tasks.loop(minutes=30)
async def purge_and_send_line():
    channel = bot.get_channel(ORDER_CHANNEL_ID)
    if channel:
        # Purge all messages in the channel
        await channel.purge(limit=None)

        # Send the line image
        await send_line(channel)


@bot.event
async def on_message(message):
    if message.author.bot:
        return  # Ignore messages from other bots to avoid loops

    if message.channel.id == ORDER_CHANNEL_ID:
        # Delete the message if it's not from the bot
        if message.author != bot.user:
            await message.delete()
        return

    if message.channel.id in TARGET_CATEGORY_IDS:
        print(
            f"Received message in TARGET_CATEGORY_ID channel {message.channel.id}: {message.content}"
        )
        await send_line(message.channel)
        return  # Return after processing line message, avoid processing commands for this case

    await bot.process_commands(
        message
    )  # Process commands after handling custom logic


@bot.event
async def on_message_delete(message):
    # Check if the deleted message is the one that the bot sent as line
    line_message_id = line_messages.get(message.channel.id)
    if line_message_id == message.id:
        try:
            line_message = await message.channel.fetch_message(line_message_id)
            if line_message:
                await line_message.delete()
        except discord.NotFound:
            pass
        del line_messages[message.channel.id]
    else:
        # Check if the deleted message was sent by a user in the TARGET_CATEGORY_IDS
        if message.author.bot:
            return

        if message.channel.id in TARGET_CATEGORY_IDS:
            # Check if the bot sent a line message after the deleted user message
            if line_messages.get(message.channel.id):
                try:
                    line_message = await message.channel.fetch_message(
                        line_messages[message.channel.id]
                    )
                    if line_message:
                        await line_message.delete()
                        del line_messages[message.channel.id]
                except discord.NotFound:
                    pass
            else:
                # If the channel is in TARGET_CATEGORY_IDS but not in line_messages, handle it accordingly
                # For example, you can resend the line message here if desired
                pass


async def send_line(channel):
    # Check if the line image file exists in the bot's folder
    line_file = "line.png" if os.path.exists("line.png") else "line.gif"
    if not os.path.exists(line_file):
        await channel.send(
            "The line image 'line.png' or 'line.gif' is missing."
        )
        return

    with open(line_file, "rb") as f:
        picture = discord.File(f)

    filename = "line.png" if line_file == "line.png" else "line.gif"

    line_message = await channel.send(file=discord.File(f, filename=filename))
    line_messages[channel.id] = line_message.id
