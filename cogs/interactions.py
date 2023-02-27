import nextcord
#from nextcord import DMChannel
#from nextcord.utils import get
from nextcord.ext import commands
from nextcord import Embed
import time
import random
import json
from asyncio import sleep as s
import get_from_servers as asukaDB


class interactions(commands.Cog):
    def _init_(self, bot):
        self.bot = bot

    @commands.command(aliases=['purge'])
    async def clear(self, ctx, amount=6):
        """ clears a default number of 5 messages if not declared after command. """
        if not ctx.message.content.replace("$clear", "", -1) == "":
            amount = int(ctx.message.content.replace("$clear ", "", -1))
            amount += 1
        await ctx.channel.purge(limit=amount)

    @commands.command()
    async def usrinfo(self, ctx, *, target: nextcord.Member = None):
        """ Display mentioned user's info. """
        if not ctx.message.mentions:
            target = ctx.author

        embed = nextcord.Embed()
        embed.title = "User Info"
        embed.set_thumbnail(url=target.avatar_url)
        fields = [
            ("ID", target.id, False),
            ("Name", str(target), True),
            ("Bot?", target.bot, True),
            ("Top Role", target.top_role.mention, True),
            ("Status", str(target.status).title(), True),
            #("Activity", f"{target.activity.name} {str(getattr(target.activity, 'type')).title()}", True),
            ("Created At", target.created_at.strftime("%d/%m/%Y %H:%M:%S"),
             True),
            ("Joined At", target.joined_at.strftime("%d/%m/%Y %H:%M:%S"), True)
        ]
        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)
        await ctx.send(embed=embed)

    @commands.command()
    async def avatar(self, ctx, *, target: nextcord.Member = None):
        """ Display mentioned user's avatar. """
        author = ctx.author
        if not ctx.message.mentions:
            target = ctx.author

        embed = Embed()
        embed.set_image(url=target.display_avatar)
        embed.color = 0x4887c6
        embed.title = target.name + "'s Avatar"
        embed.set_footer(text="Requested by " + author.name)
        await ctx.send(embed=embed)

    @commands.command(aliases=['hi'])
    async def hello(self, ctx):
        author = ctx.message.author.name
        if (author == 'XENDAL_INC'):
            honorifics = '-Sama'
        else:
            honorifics = ' Sempai'
        if (author == 'Waleed-Kun'):
            await ctx.send('**HENTAI! LOLICON!**')
        elif (author == "Gentleman N'WAH"):
            await ctx.send('**SHUT THE FUCK UP MONKEY**')
        else:
            await ctx.send('Ohayo ' + ctx.message.author.mention + honorifics +
                           ' :heart:')

    @commands.command()
    async def reminder(self, ctx, time: int, *, msg):
        try:
            await s(int(time))
            await ctx.send(msg)
        except Exception as e:
            await ctx.send(e)

    @commands.command()
    async def daisuki(self, ctx):
        """ Return affection to my owner only. """
        master = "<@380016239310929931>"
        if ctx.message.author.name == "XENDAL_INC":
            await ctx.send("Watashi mo! " + ctx.message.author.mention +
                           "-Sama!:heart:\nhttps://tenor.com/ZOap.gif")
        else:
            await ctx.send(
                "hehe, do u really think I could accept those mere feelings when I have "
                + master + "-Sama???\nhttps://tenor.com/buIuA.gif")

    @commands.command()
    async def name(self, ctx):
        #await ctx.message.add_reaction("❤️")
        await ctx.send("Yo! My name is Asuka-chan")

    @commands.command(aliases=['slaps', 'bitchslap', 'bitchslaps'])
    async def slap(self, ctx):
        author = ctx.message.author.name
        if (author == 'XENDAL_INC'):
            honorifics = '-Sama'
        else:
            honorifics = ' Sempai'
        if ctx.message.mentions and ctx.message.author.id != ctx.message.mentions[
                0].id:
            if ctx.message.author.name == "XENDAL_INC" and str(
                    ctx.message.mentions[0].id) == '842228270400536586':
                mention = '<@'
                mention += str(ctx.message.mentions[0].id) + '>'
                embed = Embed()
                embed.title = "HIDOI!"
                embed.color = 0xdf2020
                embed.description = '*' + ctx.message.author.mention + honorifics + ' made' + mention + ' cry!*'
                embed.set_image(
                    url="https://c.tenor.com/otSAwjPqcJsAAAAC/sad-cry.gif")
                await ctx.send(embed=embed)

            else:
                mention = '<@'
                mention += str(ctx.message.mentions[0].id) + '>'
                if not str(ctx.message.mentions[0].id) == '842228270400536586':
                    slap = asukaDB.get_random_gif("slap")
                    embed = Embed()
                    embed.title = "You gave a slap!"
                    embed.color = 0xdf2020
                    embed.description = '*YOOO, ' + ctx.message.author.mention + honorifics + ' started slapping the shit out of ' + mention + '!*'
                    embed.set_image(url=slap)
                    await ctx.send(embed=embed)
                else:
                    embed = Embed()
                    embed.title = "Heh. nice try!"
                    embed.color = 0xdf2020
                    embed.description = "*" + ctx.message.author.mention + honorifics + " failed miserably to slap " + mention + "!*"
                    embed.set_image(
                        url=
                        "https://c.tenor.com/XN4eaRmwtkQAAAAC/nobara-kugisaki-nobara.gif"
                    )
                    await ctx.send(embed=embed)

        else:
            embed = Embed()
            embed.title = "Are you... ok?!"
            embed.color = 0xdf2020
            embed.description = "*" + ctx.message.author.mention + honorifics + " started slapping themselves!*"
            embed.set_image(
                url="https://c.tenor.com/IVA2Go3aoAkAAAAC/pichu-pickachu.gif")
            await ctx.send(embed=embed)

    @commands.command()
    async def kick(self, ctx):
        honorifics = " Sempai"
        author = ctx.message.author
        if ctx.message.mentions:
            mention = ctx.message.mentions[0].mention
            kick = asukaDB.get_random_gif("kick")
            embed = Embed()
            embed.title = "You gave a kick!"
            embed.color = 0xdf2020
            embed.description = '*YOOO, ' + author.mention + honorifics + ' started kicking the shit out of ' + mention + '!*'
            embed.set_image(url=kick)
            await ctx.send(embed=embed)

    @commands.command()
    async def kiss(self, ctx):
        honorifics = " Sempai"
        author = ctx.message.author
        if ctx.message.mentions:
            mention = ctx.message.mentions[0].mention
            kiss = asukaDB.get_random_gif("kiss")
            embed = Embed()
            embed.title = "You gave a kiss!"
            embed.color = 0xdf2020
            embed.description = '*Awww, ' + author.mention + honorifics + ' blew a kiss to ' + mention + '!*'
            embed.set_image(url=kiss)
            await ctx.send(embed=embed)

    @commands.command()
    async def lick(self, ctx):
        honorifics = " Sempai"
        author = ctx.message.author
        if ctx.message.mentions:
            mention = ctx.message.mentions[0].mention
            lick = asukaDB.get_random_gif("lick")
            embed = Embed()
            embed.title = "You gave a lick!"
            embed.color = 0xdf2020
            embed.description = '*Ewww, ' + author.mention + honorifics + ' licked ' + mention + ' like a puppy!*'
            embed.set_image(url=lick)
            await ctx.send(embed=embed)

    @commands.command(
        aliases=['hit', 'hits', 'jab', 'jabs', 'fight', 'fights', 'punches'])
    async def punch(self, ctx):
        author = ctx.message.author.name
        if author == 'XENDAL_INC':
            honorifics = '-Sama'
        else:
            honorifics = ' Sempai'
        if ctx.message.mentions and ctx.message.author.id != ctx.message.mentions[
                0].id:
            if ctx.message.author.name == "XENDAL_INC" and str(
                    ctx.message.mentions[0].id) == '842228270400536586':
                embed = Embed()
                embed.description = f'HIDOI {ctx.author.mention}{honorifics} :broken_heart:\n'
                embed.set_image(url='https://tenor.com/xNYJ.gif')
                await ctx.send(embed=embed)
            else:
                with open('db/gifs/punch.json', 'r') as f:
                    gif = json.load(f)
                if not str(ctx.message.mentions[0].id) == '842228270400536586':
                    mention = '<@'
                    mention += str(ctx.message.mentions[0].id) + '>'
                    punch = random.choice(gif['punch'])
                    embed = Embed()
                    embed.description = f'SUGOI!!!, {ctx.message.author.mention}{honorifics} started punching {mention}\n'
                    embed.set_image(url=punch['link'])
                    await ctx.send(embed=embed)
                else:
                    embed = Embed()
                    embed.description = f'Heh, nice try{ctx.message.author.mention}{honorifics}~\n'
                    embed.set_image(url='https://tenor.com/bBKj0.gif')
                    await ctx.send(embed=embed)
        else:
            embed = Embed()
            embed.description = f'{ctx.message.author.mention}{honorifics} started punching themselves\n'
            embed.set_image(url='https://tenor.com/bnBiy.gif')
            await ctx.send(embed=embed)

    @commands.command(aliases=['hugs', 'cuddle', 'cuddling', 'brohug'])
    async def hug(self, ctx):
        author = ctx.message.author.name
        if (author == 'XENDAL_INC'):
            honorifics = '-Sama'
        else:
            honorifics = ' Sempai'
        if ctx.message.mentions and ctx.message.author.id != ctx.message.mentions[
                0].id:
            if ctx.message.author.name == "XENDAL_INC" and str(
                    ctx.message.mentions[0].id) == '842228270400536586':
                await ctx.send(
                    ctx.author.mention + honorifics +
                    ' b-Baka! s-stop... pls :heart:\nhttps://tenor.com/blkN3.gif'
                )

            else:

                with open('db/gifs/hug.json', 'r') as f:
                    gif = json.load(f)
                if not str(ctx.message.mentions[0].id) == '842228270400536586':
                    mention = '<@'
                    mention += str(ctx.message.mentions[0].id) + '>'
                    if "brohug" not in ctx.message.content:
                        hug = random.choice(gif['hug'])
                        await ctx.send(ctx.message.author.mention +
                                       honorifics + ' started hugging ' +
                                       mention + '\n' + hug['link'])
                    else:
                        hug = gif['hug'][4]
                        await ctx.send(ctx.message.author.mention +
                                       honorifics + ' started bro hugging ' +
                                       mention + '\n' + hug['link'])
                else:
                    await ctx.send(
                        'Heh, that is so creepy that u are ridiculing yourself'
                        + ctx.message.author.mention + honorifics +
                        '~\nhttps://tenor.com/blITm.gif')

        else:
            await ctx.send(
                ctx.message.author.mention + honorifics +
                ' started hugging themselves :smirk:\nhttps://tenor.com/bCzqL.gif'
            )

    @commands.command()
    async def tadaima(self, ctx):
        author = ctx.message.author.name
        if (author == 'XENDAL_INC'):
            honorifics = '-Sama!'
        else:
            honorifics = ' Sempai!'
        await ctx.send('Welcome back ' + ctx.message.author.mention +
                       honorifics + ' :heart:')
        time.sleep(2)
        await ctx.send('Would u like your dinner?')
        time.sleep(2)
        await ctx.send('Or bath?')
        time.sleep(2)
        await ctx.send('Or...')
        time.sleep(3)
        await ctx.send('Asuka-chan?')

    @commands.command()
    async def explosion(self, ctx):
        await ctx.send('Darkness blacker than black \nand darker than dark,')
        time.sleep(3)
        await ctx.send('I beseech thee, combine with my deep crimson.')
        time.sleep(3)
        await ctx.send('The time of awakening cometh.')
        time.sleep(3)
        await ctx.send('Justice, fallen upon the infallible boundary,')
        time.sleep(3)
        await ctx.send('appear now as an intangible distortion!')
        time.sleep(3)
        await ctx.send('This is the mightiest means of attack known to man,')
        time.sleep(3)
        await ctx.send('the ultimate attack magic!')
        time.sleep(3)
        await ctx.send('**EXPLOSION!!**')
        time.sleep(3)
        await ctx.send(
            'https://media1.tenor.com/images/a5200ff8939402e4e2bbda3a8107d2b1/tenor.gif?itemid=7559840'
        )


def setup(bot):
    bot.add_cog(interactions(bot))
