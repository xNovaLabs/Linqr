import discord
import requests
import json
import shutil
import os
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


                        await ctx.send("Enter the captcha below.")
                        await ctx.send(file=discord.File("./captcha.png"))
                        os.remove("captcha.png")

                        def check(msg):
                            return msg.author == ctx.author and msg.channel == ctx.channel
                        
                        try:
                            msg = await bot.wait_for("message", check=check, timeout=15)
                        except asyncio.TimeoutError:
                            await ctx.send("Sorry, you didn't reply in time.")
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

                        if ("Subdomains" in response.text):
                            os.system(f"curl -H \"Content-Type: application/json\" -d '\"{domain}\"' \"http://localhost:2024/config/apps/http/servers/srv0/routes/0/match/0/host\"")
                            with open("domains.txt", "w") as f:
                                 f.write("\nhttps://"+ subdomain + "." + domain + "/")
                            await ctx.send("https://" + subdomain + "." + domain + "/")
                        else:
                            await ctx.send("Captcha Invalid. Try again.")
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

            await ctx.send("Enter the captcha below.")
            await ctx.send(file=discord.File("./captcha.png"))
            os.remove("captcha.png")

            def check(msg):
                return msg.author == ctx.author and msg.channel == ctx.channel
            try:
                msg = await bot.wait_for("message", check=check, timeout=15)
            except asyncio.TimeoutError:
                await ctx.send("Sorry, you didn't reply in time.")
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

                await ctx.send("Thank you for contributing to the proxy bot, this helps us generate more links for you!")
                with open("accounts.txt", "a+") as f:
                    f.write("\n"+username+"|"+password)
                    f.close()
            else:
                await ctx.send("Invalid captcha. Please try again")
                await method()
        await method()


            


    
    




bot.run("MTE3ODg5ODczNzk5MzYyOTc2Ng.G84QDP.xn_OwF7cYP6MBlg-eJx8vI7M2ALUIbpkcjVszg")
