import discord
from discord.ext import commands
import yt_dlp

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='?', intents=intents)

# 유튜브 오디오 추출 설정
ytdl_format_options = {
    'format': 'bestaudio/best',
    'noplaylist': True,
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = yt_dlp.YoutubeDL(ytdl_format_options)


# 🔹 음악 재생
@bot.command()
async def 실행(ctx, url):
    if ctx.author.voice is None:
        await ctx.send("음성 채널에 계시지 않은 것 같습니다.")
        return

    channel = ctx.author.voice.channel
    vc = await channel.connect()

    info = ytdl.extract_info(url, download=False)
    url2 = info['url']

    vc.play(discord.FFmpegPCMAudio(url2, **ffmpeg_options))
    await ctx.send("재생 시작!")


# 🔹 멈춤 + 퇴장
@bot.command()
async def 멈춰(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("음성 재생을 종료합니다.")
    else:
        await ctx.send("봇이 음성 채널에 없습니다.")


# 🔹 봇 실행
import os
bot.run(os.getenv("TOKEN"))