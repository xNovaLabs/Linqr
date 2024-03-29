import discord
import requests
import json
import shutil
import os
import dns.resolver
from tempmail import EMail
import re
import idUtil
from lxml import etree
import asyncio
from discord.ext import tasks, commands
from bs4 import BeautifulSoup as bs
import blockUtil
import string
import random
from datetime import datetime

bot = commands.Bot(command_prefix='/', intents=discord.Intents.all())
r = requests.Session()

@bot.event
async def on_ready():
    print("Bot is online.")


@bot.command()
async def generate(ctx):
    async def goBack():
            with open("accounts.txt") as f:
                accounts = f.read().splitlines()

            account = random.choice(accounts)
            username, password = account.split("|")
            username = username.lower()


            headers = {
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
                    'Accept-Language': 'en-US,en;q=0.8',
                    'Cache-Control': 'max-age=0',
                    'Connection': 'keep-alive',
                    'Content-Type': 'application/x-www-form-urlencoded',
                    # 'Cookie': 'tz=9Ac0bCS9vl16NEKqkgUZV41l; PHPSESSID=5q5e8fvuulivu6rddn7ran5gr1; dns_cookie=Sax1DsBBobQPaIRoQ4yVGPeY; __utma=4955364.869240143.1709500076.1709500076.1710102702.2; __utmb=4955364; __utmc=4955364; bgcolor=black',
                    'Origin': 'https://freedns.afraid.org',
                    'Referer': 'https://freedns.afraid.org/zc.php?step=2',
                    'Sec-Fetch-Dest': 'document',
                    'Sec-Fetch-Mode': 'navigate',
                    'Sec-Fetch-Site': 'same-origin',
                    'Sec-Fetch-User': '?1',
                    'Sec-GPC': '1',
                    'Upgrade-Insecure-Requests': '1',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
                    'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Brave";v="122"',
                    'sec-ch-ua-mobile': '?0',
                    'sec-ch-ua-platform': '"Windows"',
                }

            params = {
                    'step': '2',
                }

            data = {
                    'username': username,
                    'password': password,
                    'remember': '1',
                    'submit': 'Login',
                    'remote': '',
                    'from': '',
                    'action': 'auth',
                }

            resp = r.post('https://freedns.afraid.org/zc.php', params=params, headers=headers, data=data)

            req = r.get("https://freedns.afraid.org/subdomain/", headers=headers)



            if ("Add a subdomain" in req.text or "5 subdomains" not in req.text):
                    headers = {
                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
                        'Accept-Language': 'en-US,en;q=0.8',
                        'Cache-Control': 'max-age=0',
                        'Connection': 'keep-alive',
                        'Content-Type': 'application/x-www-form-urlencoded',
                        # 'Cookie': 'tz=9Ac0bCS9vl16NEKqkgUZV41l; __utmz=4955364.1709500076.1.1.utmccn=(direct)|utmcsr=(direct)|utmcmd=(none); PHPSESSID=5q5e8fvuulivu6rddn7ran5gr1; dns_cookie=Sax1DsBBobQPaIRoQ4yVGPeY; __utma=4955364.869240143.1709500076.1709500076.1710102702.2; __utmb=4955364; __utmc=4955364; bgcolor=black',
                        'Origin': 'https://freedns.afraid.org',
                        'Referer': 'https://freedns.afraid.org/subdomain/edit.php',
                        'Sec-Fetch-Dest': 'document',
                        'Sec-Fetch-Mode': 'navigate',
                        'Sec-Fetch-Site': 'same-origin',
                        'Sec-Fetch-User': '?1',
                        'Sec-GPC': '1',
                        'Upgrade-Insecure-Requests': '1',
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
                        'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Brave";v="122"',
                        'sec-ch-ua-mobile': '?0',
                        'sec-ch-ua-platform': '"Windows"',
                    }

                    params = {
                        'step': '2',
                    }

                    with open('validatedDomains.json') as f:
                        data = json.load(f)


                    domain = random.choice(data)["domain"]
                    subdomain = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
                    async def anotherOne():
                        resp = r.get("https://freedns.afraid.org/securimage/securimage_show.php", stream=True)
                        with open('captcha.png', 'wb') as out_file:
                            shutil.copyfileobj(resp.raw, out_file)  

                        files = discord.File("./captcha.png", filename="captcha.png")
                        embed = discord.Embed(title="Enter the captcha below",
                                description="Please enter the captcha below. This allows us to create the domain for you and properly allocate it within our system.",
                                colour=0x930dee,
                                timestamp=datetime.now())

                        embed.set_author(name="Xenon+",
                                        url="https://xenub.com",
                                        icon_url="https://images-ext-1.discordapp.net/external/jFiWrY9F9UPppdB7iVpm5VMIjKNeVI9h_FRg_CseM40/%3Fsize%3D4096/https/cdn.discordapp.com/icons/1175543646217580704/a0cfabf748577517086a2c3c9c04eaba.png?format=webp&quality=lossless&width=348&height=348")

                        embed.set_image(url="attachment://captcha.png")

                        embed.set_footer(text="made by xenon.")

                        await ctx.send(file=files, embed=embed)
                        os.remove("captcha.png")

                        def check(msg):
                            return msg.author == ctx.author and msg.channel == ctx.channel

                        try:
                            msg = await bot.wait_for("message", check=check, timeout=15)
                        except asyncio.TimeoutError:
                            embed = discord.Embed(title="Timeout",
                                                description="Sorry, you didn't respond in time so our system has timed you out. Please re-use the command.",
                                                colour=0x930dee,
                                                timestamp=datetime.now())

                            embed.set_author(name="Xenon+",
                                            url="https://xenub.com",
                                            icon_url="https://images-ext-1.discordapp.net/external/jFiWrY9F9UPppdB7iVpm5VMIjKNeVI9h_FRg_CseM40/%3Fsize%3D4096/https/cdn.discordapp.com/icons/1175543646217580704/a0cfabf748577517086a2c3c9c04eaba.png?format=webp&quality=lossless&width=348&height=348")

                            embed.set_footer(text="made by xenon.")

                            await ctx.send(embed=embed)
                            return

                        data = {
                            'type': 'A',
                            'subdomain': subdomain,
                            'domain_id': idUtil.getID(domain=domain),
                            'address': '207.231.108.250',
                            'ttlalias': 'For our premium supporters',
                            'captcha_code': msg.content,
                            'ref': '',
                            'send': 'Save!',
                        }

                        response = r.post('https://freedns.afraid.org/subdomain/save.php', params=params, headers=headers, data=data)
                        with open("log.txt", "w") as f:
                            f.write(response.text)
                        if ("Subdomains" in response.text):
                            print("hi")
                            with open("domains.txt", "w") as f:
                                 f.write('\n'+ subdomain + "." + domain)
                                 embed = discord.Embed(title="Succesfully Created Domain",
                                    description="Congratulations, our system indicates that the domain has been created with the A record set to our server. Now, you will need to first use the /dig command to check whether the A record is correctly set. Then, you will have to use the /byod command to add the domain to Xen.",
                                    colour=0x930dee,
                                    timestamp=datetime.now())

                                 embed.set_author(name="Xenon+",
                                                url="https://xenub.com",
                                                icon_url="https://images-ext-1.discordapp.net/external/jFiWrY9F9UPppdB7iVpm5VMIjKNeVI9h_FRg_CseM40/%3Fsize%3D4096/https/cdn.discordapp.com/icons/1175543646217580704/a0cfabf748577517086a2c3c9c04eaba.png?format=webp&quality=lossless&width=348&height=348")

                                 embed.add_field(name="Domain:",
                                                value=(subdomain).lower() + "." + domain,
                                                inline=False)

                                 embed.set_footer(text="made by xenon.")
                        else:
                            embed = discord.Embed(title="Invalid Captcha!",
                                description="Please try again. Our system has detected that the captcha you have submitted was incorrect.",
                                colour=0x930dee,
                                timestamp=datetime.now())

                            embed.set_author(name="Xenon+",
                                            url="https://xenub.com",
                                            icon_url="https://images-ext-1.discordapp.net/external/jFiWrY9F9UPppdB7iVpm5VMIjKNeVI9h_FRg_CseM40/%3Fsize%3D4096/https/cdn.discordapp.com/icons/1175543646217580704/a0cfabf748577517086a2c3c9c04eaba.png?format=webp&quality=lossless&width=348&height=348")

                            embed.set_footer(text="made by xenon.")

                            await ctx.send(embed=embed)

                            await anotherOne()
                    await anotherOne()
            else:
                await goBack()

    await goBack()


                
@bot.command()
async def updateReg(ctx):
    await ctx.send("Sent registry update request. Will be completed < 10 minutes.")
    os.system("python updateUtil.py")

@bot.command()
async def checkdns(ctx, domain):
  try:
    
     answers = dns.resolver.resolve(domain, 'A')
     for server in answers:
          await ctx.send(server)
  except:
    await ctx.send("No DNS Records Available.")

      
@bot.command()
async def validdns(ctx, domain):
  try:
     answers = dns.resolver.resolve(domain, 'A')
     hi = False
     for server in answers: 
          if ('207.231.108.250' in str(server)):
               await ctx.send("Valid DNS, proceed to add.")
               hi = True
     if not hi:
        await ctx.send("Invalid DNS. Point A record to 207.231.108.250")
  except:
        await ctx.send("No DNS Records Available.")


@bot.command()
async def byod(ctx, domain):
  try:
    hello = False
    answers = dns.resolver.resolve(domain, 'A')
    hello = True
    hi = False
    for server in answers: 
            if ('207.231.108.250' in str(server)):
                hi = True

    if not hi:
            embed = discord.Embed(title="ERROR: Invalid DNS Record",
                                description="Our system indicates that your domain contains the wrong A record. Please point an A record towards 207.231.108.250.",
                                colour=0x930dee,
                                timestamp=datetime.now())

            embed.set_author(name="Xenon+",
                            url="https://xenub.com",
                            icon_url="https://images-ext-1.discordapp.net/external/jFiWrY9F9UPppdB7iVpm5VMIjKNeVI9h_FRg_CseM40/%3Fsize%3D4096/https/cdn.discordapp.com/icons/1175543646217580704/a0cfabf748577517086a2c3c9c04eaba.png?format=webp&quality=lossless&width=348&height=348")

            embed.set_footer(text="made by xenon.")

            await ctx.send(embed=embed)
    if hi:
      os.system(f"curl -H \"Content-Type: application/json\" -d '\"{domain}\"' \"http://localhost:2024/config/apps/http/servers/srv0/routes/0/match/0/host\"")
      embed = discord.Embed(title="Succesfully Added Domain",
                        description="Our system indicates that we have successfully process the addition of your domain. Please wait up to 5 minutes for your domain to be activated.",
                        colour=0x930dee,
                        timestamp=datetime.now())

      embed.set_author(name="Xenon+",
                    url="https://xenub.com",
                    icon_url="https://images-ext-1.discordapp.net/external/jFiWrY9F9UPppdB7iVpm5VMIjKNeVI9h_FRg_CseM40/%3Fsize%3D4096/https/cdn.discordapp.com/icons/1175543646217580704/a0cfabf748577517086a2c3c9c04eaba.png?format=webp&quality=lossless&width=348&height=348")


      embed.set_footer(text="made by xenon.")
      embed.add_field(name="Domain:",
                value=domain,
                inline=False)

      channel = bot.get_channel(1219014618362675352)
      await ctx.send(embed=embed)
      await channel.send("New Xen Domain: https://" + domain + " | Created by: " + ctx.message.author.tag)


  except:
      if not hello:
        embed = discord.Embed(title="ERROR: No DNS Records Available",
                            description="Our system indicates that there are no dns records available for your respectable domain. Please wait for a while before retrying this command.",
                            colour=0x930dee,
                            timestamp=datetime.now())

        embed.set_author(name="Xenon+",
                        url="https://xenub.com",
                        icon_url="https://images-ext-1.discordapp.net/external/jFiWrY9F9UPppdB7iVpm5VMIjKNeVI9h_FRg_CseM40/%3Fsize%3D4096/https/cdn.discordapp.com/icons/1175543646217580704/a0cfabf748577517086a2c3c9c04eaba.png?format=webp&quality=lossless&width=348&height=348")

        embed.set_footer(text="made by xenon.")

        await ctx.send(embed=embed)
      
    

@bot.command()
async def contribute(ctx):

        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.8',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Origin': 'https://freedns.afraid.org',
            'Referer': 'https://freedns.afraid.org/signup/?plan=starter',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1',
            'Sec-GPC': '1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
            'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Brave";v="122"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
        }

        params = {
            'step': '2',
        }

        username = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase, k=9))
        password = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase, k=9))
        email = EMail()
        
        async def method():
            resp = r.get("https://freedns.afraid.org/securimage/securimage_show.php", stream=True)
            with open('captcha.png', 'wb') as out_file:
                shutil.copyfileobj(resp.raw, out_file)  

            
            files = discord.File("./captcha.png", filename="captcha.png")
            embed = discord.Embed(title="Enter the captcha below",
                      description="Please enter the captcha below. This allows us to create the domain for you and properly allocate it within our system.",
                      colour=0x930dee,
                      timestamp=datetime.now())

            embed.set_author(name="Xenon+",
                            url="https://xenub.com",
                            icon_url="https://images-ext-1.discordapp.net/external/jFiWrY9F9UPppdB7iVpm5VMIjKNeVI9h_FRg_CseM40/%3Fsize%3D4096/https/cdn.discordapp.com/icons/1175543646217580704/a0cfabf748577517086a2c3c9c04eaba.png?format=webp&quality=lossless&width=348&height=348")

            embed.set_image(url="attachment://captcha.png")

            embed.set_footer(text="made by xenon.")

            await ctx.send(file=files, embed=embed)
            os.remove("captcha.png")

            def check(msg):
                return msg.author == ctx.author and msg.channel == ctx.channel
            try:
                msg = await bot.wait_for("message", check=check, timeout=15)
            except asyncio.TimeoutError:
                embed = discord.Embed(title="Timeout",
                                    description="Sorry, you didn't respond in time so our system has timed you out. Please re-use the command.",
                                    colour=0x930dee,
                                    timestamp=datetime.now())

                embed.set_author(name="Xenon+",
                                url="https://xenub.com",
                                icon_url="https://images-ext-1.discordapp.net/external/jFiWrY9F9UPppdB7iVpm5VMIjKNeVI9h_FRg_CseM40/%3Fsize%3D4096/https/cdn.discordapp.com/icons/1175543646217580704/a0cfabf748577517086a2c3c9c04eaba.png?format=webp&quality=lossless&width=348&height=348")

                embed.set_footer(text="made by xenon.")

                await ctx.send(embed=embed)
                return


            data = {
                'plan': 'starter',
                'firstname': ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase, k=9)),
                'lastname': ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase, k=9)),
                'username': username,
                'password': password,
                'password2': password,
                'email': email.address,
                'captcha_code': msg.content,
                'tos': '1',
                'PROCID': '',
                'TRANSPRE': '',
                'action': 'signup',
                'send': 'Send activation email',
            }

            response = r.post('https://freedns.afraid.org/signup/', params=params, headers=headers, data=data)
            if ("The process has begun!" in response.text):
                msg = email.wait_for_message()
                r.get(re.search("(?P<url>https?://[^\s]+)", msg.body).group("url"))

                embed = discord.Embed(title="Thank you for contributing to xenon!",
                      description="Your help is greatly appreciated. This command fuels the accounts for the generate command used to create new xenon links!",
                      colour=0x930dee,
                      timestamp=datetime.now())

                embed.set_author(name="Xenon+",
                                url="https://xenub.com",
                                icon_url="https://images-ext-1.discordapp.net/external/jFiWrY9F9UPppdB7iVpm5VMIjKNeVI9h_FRg_CseM40/%3Fsize%3D4096/https/cdn.discordapp.com/icons/1175543646217580704/a0cfabf748577517086a2c3c9c04eaba.png?format=webp&quality=lossless&width=348&height=348")

                embed.set_footer(text="made by xenon.")
                await ctx.send(embed=embed)
                with open("accounts.txt", "a+") as f:
                    f.write("\n"+username+"|"+password)
                    f.close()
            else:
                embed = discord.Embed(title="Invalid Captcha!",
                      description="Please try again. Our system has detected that the captcha you have submitted was incorrect.",
                      colour=0x930dee,
                      timestamp=datetime.now())

                embed.set_author(name="Xenon+",
                                url="https://xenub.com",
                                icon_url="https://images-ext-1.discordapp.net/external/jFiWrY9F9UPppdB7iVpm5VMIjKNeVI9h_FRg_CseM40/%3Fsize%3D4096/https/cdn.discordapp.com/icons/1175543646217580704/a0cfabf748577517086a2c3c9c04eaba.png?format=webp&quality=lossless&width=348&height=348")

                embed.set_footer(text="made by xenon.")

                await ctx.send(embed=embed)

                await method()
        await method()

            


    
    




bot.run("MTE3ODg5ODczNzk5MzYyOTc2Ng.G84QDP.xn_OwF7cYP6MBlg-eJx8vI7M2ALUIbpkcjVszg")
