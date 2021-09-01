from discord import Embed
from discord.ext.commands import (BucketType, cooldown, Bot, Cog, command)
from config.main import color

# TODO : rewrite this for a better look.


class HelpCog(Cog, name="help command"):
    def __init__(self, bot: Bot):
        self.bot = bot

    @command(name='help',
             usage="(commandName)",
             description="Display the help message.",
             aliases=['h', '?'])
    @cooldown(1, 2, BucketType.member)
    async def help(self, ctx, commandName: str = None):

        commandName2 = None
        stop = False

        if commandName is not None:
            for i in self.bot.commands:
                if i.name == commandName.lower():
                    commandName2 = i
                    break
                else:
                    for j in i.aliases:
                        if j == commandName.lower():
                            commandName2 = i
                            stop = True
                            break
                        if stop:
                            break

            if commandName2 is None:
                await ctx.channel.send("No command found!")
            else:
                embed = Embed(
                    title=f"{commandName2.name.upper()} Command",
                    description=f"{commandName2.description}",
                    color=color)
                embed.set_thumbnail(url=f'{self.bot.user.avatar_url}')
                embed.add_field(
                    name=f"Name", value=f"{commandName2.name}", inline=False)
                aliases = commandName2.aliases
                aliasList = ""
                if len(aliases) > 0:
                    for alias in aliases:
                        aliasList += alias + ", "
                    aliasList = aliasList[:-2]
                    embed.add_field(name=f"Aliases", value=aliasList)
                else:
                    embed.add_field(name=f"Aliases",
                                    value="None", inline=False)

                if commandName2.usage is None:
                    embed.add_field(name=f"Usage", value=f"None", inline=False)
                else:
                    embed.add_field(
                        name=f"Usage",
                        value=f"{self.bot.command_prefix}{commandName2.name} {commandName2.usage}",
                        inline=False)

                await ctx.channel.send(embed=embed)
        else:
            embed = Embed(
                title=f"Help page",
                description=f"{self.bot.command_prefix}help (commandName), display the help list or the help data for a specific command.",
                color=color)
            embed.set_thumbnail(url=f'{self.bot.user.avatar_url}')
            for i in self.bot.commands:
                embed.add_field(name=i.name, value=i.description, inline=False)
            await ctx.channel.send(embed=embed)


def setup(bot: Bot):
    bot.remove_command("help")
    bot.add_cog(HelpCog(bot))
