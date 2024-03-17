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


bot = commands.Bot(command_prefix='/', intents=discord.Intents.all())
r = requests.Session()

@bot.event
async def on_ready():
    print("Bot is online.")


@bot.command()
async def generate(ctx):
    await ctx.send("Under maintenance, will be fixed soon.")


                
@bot.command()
async def updateReg(ctx):
    await ctx.send("Sent registry update request. Will be completed < 10 minutes.")
    os.system("python updateUtil.py")

@bot.command()
async def checkdns(ctx, domain):
     answers = dns.resolver.resolve(domain, 'A')

     for server in answers:
          await ctx.send(server)
      
@bot.command()
async def validdns(ctx, domain):
     answers = dns.resolver.resolve(domain, 'A')
     hi = False
     for server in answers: 
          if ('207.231.108.250' in str(server)):
               await ctx.send("Valid DNS, proceed to add.")
               hi = True
     if not hi:
        await ctx.send("Invalid DNS. Point A record to 207.231.108.250")


@bot.command()
async def byod(ctx, domain):
  answers = dns.resolver.resolve(domain, 'A')
  hi = False
  for server in answers: 
          if ('207.231.108.250' in str(server)):
               await ctx.send("Valid DNS, proceeding to add...")
               hi = True
  if not hi:
        await ctx.send("Invalid DNS. Point A record to 207.231.108.250")
  if hi:
    os.system(f"curl -H \"Content-Type: application/json\" -d '\"{domain}\"' \"http://localhost:2024/config/apps/http/servers/srv0/routes/0/match/0/host\"")
    await ctx.send("Domain Succesfully Added! (hopefully)")
    await ctx.send("https://" + domain)
    channel = bot.get_channel(1219014618362675352)
    await channel.send("New Xen Domain: https://" + domain + " | Created by: " + ctx.message.author.tag)
      
    

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
