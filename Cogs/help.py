from discord.ext.commands.errors import CommandError
from config.embed import help_config
from config.main import color
from discord import Embed
from discord.ext.commands import Bot, Cog, Context, command, cooldown
from functions.embed_factory import create_embed
from traceback import print_exception
from sys import stderr


class HelpCog(Cog, name="Power Catalog", description="Handbook on the might of Z Butler 💪🏻"):

    def __init__(self, bot: Bot):
        self.bot = bot

    @command(name="help",
             usage="<command> | <category>",
             description="Help command for those seeking the power of Z",
             aliases=['h', '?']
             )
    async def help(self, ctx: Context, category: str = None, command: str = None):
        await ctx.message.delete()
        config = help_config()
        cogs = {x: y for (x, y) in self.bot.cogs.items()
                if x != 'Event handlers'}
        embed = create_embed(
            config=config,
            reason=None,
            no_perms_type=None,
            **cogs
        )
        await ctx.send(embed=embed)

    @help.error
    async def help_handler(self, ctx: Context, error: CommandError):
        print_exception(
            type(error), error, error.__traceback__, file=stderr)


"""
        elif category and str(category).lower() == "zeld":
            embed = Embed(color=color,
                          timestamp=ctx.message.created_at)
            embed.set_image(
                url="https://media.pp.net/attachments/697225400505598044/783140740824956958/image0.gif?width=540&height=304"
            )
            embed.description = f"\uD83D\uDCB0 `ZELD COMMANDS`\n`> help <category>` - returns all commands of that category\n`> uptime` - return how long the selfbot has been running\n`> prefix <prefix>` - changes the bot's prefix\n`> ping` - returns the bot's latency\n`> av <user>` - returns the user's pfp\n`> whois <user>` - returns user's account info\n`> tokeninfo <token>` - returns information about the token\n`> copyserver` - makes a copy of the server\n`> rainbowrole <role>` - makes the role a rainbow role (ratelimits)\n`> serverinfo` - gets information about the server\n`> serverpfp` - returns the server's icon\n`> banner` - returns the server's banner\n`> shutdown` - shutsdown the selfbot\n"
            await ctx.send(embed=embed)
        elif str(category).lower() == "account":
            embed = Embed(color=color,
                          timestamp=ctx.message.created_at)
            embed.set_image(
                url="https://media.pp.net/attachments/697225400505598044/783144406889922580/image0.gif?width=540&height=227"
            )
            embed.description = f"\uD83D\uDCB0 `ACCOUNT COMMANDS`\n`> ghost` - makes your name and pfp invisible\n`> pfpsteal <user>` - steals the users pfp\n`> setpfp <link>` - sets the image-link as your pfp\n`> hypesquad <hypesquad>` - changes your current hypesquad\n`> spoofcon <type> <name>` - spoofs your connection\n`> leavegroups` - leaves all groups that you're in\n`> cyclenick <text>` - cycles through your nickname by letter\n`> stopcyclenick` - stops cycling your nickname\n`> stream <status>` - sets your streaming status\n`> playing <status>` - sets your playing status\n`> listening <status>` - sets your listening status\n`> watching <status>` - sets your watching status\n`> stopactivity` - resets your status-activity\n`> acceptfriends` - accepts all friend requests\n`> delfriends` - removes all your friends\n`> ignorefriends` - ignores all friends requests\n`> clearblocked` - clears your block-list\n`> read` - marks all messages as read\n`> leavegc` - leaves the current groupchat\n`> adminservers` - lists all servers you have perms in\n`> slotbot <on/off>` - snipes slotbots ({self.botslotbot_sniper})\n`> giveaway <on/off>` - snipes giveaways ({self.botgiveaway_sniper})\n`> mee6 <on/off>` - auto sends messages in the specified channel ({self.botmee6}) <#{self.botmee6_channel}>\n`> yuikiss <user>` - auto sends yui kisses every minute <@{self.botyui_kiss_user}> <#{self.botyui_kiss_channel}>\n`> yuihug <user>` - auto sends yui hugs every minute <@{self.botyui_hug_user}> <#{self.botyui_hug_channel}>\n`> yuistop` - stops any running yui loops"
            await ctx.send(embed=embed)
        elif str(category).lower() == "text":
            embed = Embed(color=color,
                          timestamp=ctx.message.created_at)
            embed.set_image(
                url="https://images-ext-1.pp.net/external/F9zXdDpYU-I6szIvf-eEuKQ4pUBXOK92kgIj0Bygusw/https/media.pp.net/attachments/760116404107870228/778236394811555840/20201116_215459.gif?width=432&height=394"
            )
            embed.description = f"\uD83D\uDCB0 `TEXT COMMANDS`\n`> ZELD` - sends the ZELD logo\n`> snipe` - shows the last deleted message\n`> editsnipe` - shows the last edited message\n`> msgsniper <on/off> ({self.botmsgsniper})` - enables a message sniper for deleted messages in DMs\n`> clear` - sends a large message filled with invisible unicode\n`> del <message>` - sends a message and deletes it instantly\n`> 1337speak <message>` - talk like a hacker\n`> minesweeper` - play a game of minesweeper\n`> spam <amount>` - spams a message\n`> dm <user> <content>` - dms a user a message\n`> reverse <message>` - sends the message but in reverse-order\n`> shrug` - returns ¯\_(ツ)_/¯\n`> lenny` - returns ( ͡° ͜ʖ ͡°)\n`> fliptable` - returns (╯°□°）╯︵ ┻━┻\n`> unflip` - returns (╯°□°）╯︵ ┻━┻\n`> bold <message>` - bolds the message\n`> censor <message>` - censors the message\n`> underline <message>` - underlines the message\n`> italicize <message>` - italicizes the message\n`> strike <message>` - strikethroughs the message\n`> quote <message>` - quotes the message\n`> code <message>` - applies code formatting to the message\n`> purge <amount>` - purges the amount of messages\n`> empty` - sends an empty message\n`> tts <content>` - returns an mp4 file of your content\n`> firstmsg` - shows the first message in the channel history\n`> ascii <message>` - creates an ASCII art of your message\n`> wizz` - makes a prank message about wizzing \n`> 8ball <question>` - returns an 8ball answer\n`> slots` - play the slot machine\n`> everyone` - pings everyone through a link\n`> abc` - cyles through the alphabet\n`> 100` - cycles -100\n`> cum` - makes you cum lol?\n`> 9/11` - sends a 9/11 attack\n`> massreact <emoji>` - mass reacts with the specified emoji"
            await ctx.send(embed=embed)
        elif str(category).lower() == "Rap":
            embed = Embed(color=color,
                          timestamp=ctx.message.created_at)
            embed.set_image(
                url="https://media.pp.net/attachments/697225400505598044/790399909404082189/image0.gif?width=540&height=301"
            )
            embed.description = f"\uD83D\uDCB0 `RAP COMMANDS`\n`> play <query>` - plays the specified song if you're in a voice-channel\n`> stop` - stops the rap player\n`> skip` - skips the current song playing\n`> lyrics <song>` - shows the specified song's lyrics\n`> youtube <query>` - returns the first youtube search result of the query"
            await ctx.send(embed=embed)
        elif str(category).lower() == "image":
            embed = Embed(color=color,
                          timestamp=ctx.message.created_at)
            embed.set_image(
                url="https://images-ext-1.pp.net/external/__GnKIVffGi3PbAL_Q5p9Dt8AuL9upjYyy3q2fW_fv0/https/media.pp.net/attachments/760116404107870228/778236393863381002/20201116_215614.gif?width=432&height=265"
            )
            embed.description = f"\uD83D\uDCB0 `IMAGE MANIPULATION COMMANDS`\n`> tweet <user> <message>` makes a fake tweet\n`> magik <user>` - distorts the specified user\n`> fry <user>` - deep-fry the specified user\n`> blur <user>` - blurs the specified user\n`> pixelate <user>` - pixelates the specified user\n`> Supreme <message>` - makes a *Supreme* logo\n`> darksupreme <message>` - makes a *Dark Supreme* logo\n`> fax <text>` - makes a fax meme\n`> blurpify <user>` - blurpifies the specified user\n`> invert <user>` - inverts the specified user\n`> gay <user>` - makes the specified user gay\n`> communist <user>` - makes the specified user a communist\n`> snow <user>` - adds a snow filter to the specified user\n`> jpegify <user>` - jpegifies the specified user\n`> pornhub <logo-word 1> <logo-word 2>` - makes a PornHub logo\n`> phcomment <user> <message>` - makes a fake PornHub comment\n"
            await ctx.send(embed=embed)
        elif str(category).lower() == "nsfw":
            embed = Embed(color=color,
                          timestamp=ctx.message.created_at)
            embed.set_image(
                url="https://media.pp.net/attachments/788471921011720222/790315914687545444/image2.gif?width=540&height=304"
            )
            embed.description = f"\uD83D\uDCB0 `NSFW COMMANDS`\n`> anal` - returns anal pics\n`> erofeet` - returns erofeet pics\n`> feet` - returns sexy feet pics\n`> hentai` - returns hentai pics\n`> boobs` - returns booby pics\n`> tits` - returns titty pics\n`> blowjob` - returns blowjob pics\n`> neko` - returns neko pics\n`> lesbian` - returns lesbian pics\n`> cumslut` - returns cumslut pics\n`> pussy` - returns pussy pics\n`> waifu` - returns waifu pics"
            await ctx.send(embed=embed)
        elif str(category).lower() == "misc":
            embed = Embed(color=color,
                          timestamp=ctx.message.created_at)
            embed.set_image(
                url="https://cdn.pp.com/attachments/723250694118965300/723265016979259544/image0.gif"
            )
            embed.description = f"\uD83D\uDCB0 `MISCELLANEOUS COMMANDS`\n`> copycat <user>` - copies the users messages ({self.botcopycat})\n`> stopcopycat` - stops copycatting\n`> fakename` - makes a fakename with other members's names\n`> geoip <ip>` - looks up the ip's location\n`> pingweb <website-url>` pings a website to see if it's up\n`> anticatfish <user>` - reverse google searches the user's pfp\n`> stealemoji` - <emoji> <name> - steals the specified emoji\n`> hexcolor <hex-code>` - returns the color of the hex-code\n`> dick <user>` - returns the user's dick size\n`> bitcoin` - shows the current bitcoin exchange rate\n`> hastebin <message>` - posts your message to hastebin\n`> rolecolor <role>` - returns the role's color\n`> nitro` - generates a random nitro code\n`> feed <user>` - feeds the user\n`> tickle <user>` - tickles the user\n`> slap <user>` - slaps the user\n`> hug <user>` - hugs the user\n`> cuddle <user>` - cuddles the user\n`> smug <user>` - smugs at the user\n`> pat <user>` - pat the user\n`> kiss <user>` - kiss the user\n`> topic` - sends a conversation starter\n`> wyr` - sends a would you rather\n`> gif <query>` - sends a gif based on the query\n`> sendall <message>` - sends a message in every channel\n`> poll <msg: xyz 1: xyz 2: xyz>` - creates a poll\n`> bots` - shows all bots in the server\n`> image <query>` - returns an image\n`> hack <user>` - hacks the user\n`> token <user>` - returns the user's token\n`> cat` - returns random cat pic\n`> sadcat` - returns a random sad cat\n`> dog` - returns random dog pic\n`> fox` - returns random fox pic\n`> bird` - returns random bird pic\n"
            await ctx.send(embed=embed)
        elif str(category).lower() == "antiwizz":
            embed = Embed(color=color,
                          timestamp=ctx.message.created_at)
            embed.set_image(
                url="https://media.pp.net/attachments/788471921011720222/790315915677532170/image3.gif?width=540&height=308"
            )
            embed.description = f"\uD83D\uDCB0 `ANTI-WIZZ COMMANDS`\n`> antiraid <on/off>` - toggles anti-nuke ({self.botantiraid})\n`> whitelist <user>` - whitelists the specified user\n**NOTE** Whitelisting a user will completely exclude them from anti-nuke detections, be weary on who you whitelist.\n`> whitelisted <-g>` - see who's whitleisted and in what guild\n`> unwhitelist <user>` - unwhitelists the user\n`> clearwhitelist` - clears the whitelist hash"
            await ctx.send(embed=embed)
        elif str(category).lower() == "wizz":
            embed = Embed(color=color,
                          timestamp=ctx.message.created_at)
            embed.set_image(
                url="https://cdn.pp.com/attachments/723250694118965300/723256768742031451/image0.gif"
            )
            embed.description = f"\uD83D\uDCB0 `WIZZ COMMANDS`\n`> tokenfuck <token>` - disables the token\n`> nuke` - wizzes the server\n`> massban` - bans everyone in the server\n`> dynoban` - mass bans with dyno one message at a time\n`> masskick` - kicks everyone in the server\n`> spamroles` - spam makes 250 roles\n`> spamchannels` - spam makes 250 text channels\n`> delchannels` - deletes all channels in the server\n`> delroles` - deletes all roles in the server\n`> purgebans` - unbans everyone\n`> renamechannels <name>` - renames all channels\n`> servername <name>` - renames the server to the specified name\n`> nickall <name>` - sets all user's nicknames to the specified name\n`> changeregion <amount>` - spam changes regions in groupchats\n`> kickgc` - kicks everyone in the gc\n`> spamgcname` - spam changes the groupchat name\n`> massmention <message>` - mass mentions random people"
            await ctx.send(embed=embed)
"""


def setup(bot: Bot):
    bot.remove_command('help')
    bot.add_cog(HelpCog(bot))
