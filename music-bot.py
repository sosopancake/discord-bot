import discord
from discord.ext import commands
import yt_dlp
import os

from flask import Flask
from threading import Thread

# 🔹 Flask 서버 (Render용)
app = Flask('')

@app.route('/')
def home():
    return "Bot is running!"

def run():
    app.run(host='0.0.0.0', port=10000)

def keep_alive():
    t = Thread(target=run)
    t.start()


# 🔹 디스코드 봇 설정
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='?', intents=intents)

# 🔹 yt-dlp 설정
ytdl = yt_dlp.YoutubeDL({
    'format': 'bestaudio',
    'noplaylist': True
})

ffmpeg_options = {
    'options': '-vn'
}


# 🎵 음악 재생
@bot.command()
async def 실행(ctx, url):
    if ctx.author.voice is None:
        await ctx.send("음성 채널에 먼저 들어가!")
        return

    channel = ctx.author.voice.channel
    vc = await channel.connect()

    info = ytdl.extract_info(url, download=False)
    url2 = info['url']

    vc.play(discord.FFmpegPCMAudio(url2, **ffmpeg_options))
    await ctx.send("재생 시작!")


# ⛔ 멈춤 + 퇴장
@bot.command()
async def 멈춰(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("멈추고 퇴장!")


# 🔥 Render용 웹서버 실행
keep_alive()

# 🔥 봇 실행 (토큰은 Render에서 환경변수로)
bot.run(os.getenv("TOKEN"))