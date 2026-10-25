import os
import asyncio
import discord
from discord import app_commands
from discord.ext import commands
from yt_dlp import YoutubeDL
import datetime
from flask import Flask
from threading import Thread

# ===== Keep alive cho Render =====
app = Flask('')
@app.route('/')
def home():
    return 'Meta AI x Spotify Bot Online!'
@app.route('/healthz')
def healthz():
    return 'OK', 200
Thread(target=lambda: app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000))), daemon=True).start()

# ===== Bot setup - PHẢI ĐỂ TRƯỚC MỌI @bot.event =====
intents = discord.Intents.all()
intents.message_content = True
intents.voice_states = True
bot = commands.Bot(command_prefix="!", intents=intents)

YTDL_OPTIONS = {
    'format': 'bestaudio/best',
    'quiet': True,
    'no_warnings': True,
    'default_search': 'ytsearch',
    'source_address': '0.0.0.0',
    'noplaylist': True,
}
FFMPEG_OPTIONS = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn -b:a 192k'
}
ytdl = YoutubeDL(YTDL_OPTIONS)

class Voice:
    def __init__(self, bot):
        self.bot = bot
        self.queue = {}
    def get_queue(self, gid):
        if gid not in self.queue:
            self.queue[gid] = []
        return self.queue[gid]
    async def join(self, interaction):
        if not interaction.user.voice:
            await interaction.response.send_message("❌ Vào voice trước Sen ơi!", ephemeral=True)
            return None
        channel = interaction.user.voice.channel
        vc = interaction.guild.voice_client or await channel.connect(self_deaf=False, self_mute=False)
        if vc.channel != channel:
            await vc.move_to(channel)
        try:
            await interaction.guild.me.edit(mute=False, deafen=False)
        except:
            pass
        return vc
    def search(self, query):
        info = ytdl.extract_info(f"ytsearch:{query}", download=False)
        if 'entries' in info:
            info = info['entries'][0]
        return {'url': info['url'], 'title': info['title'], 'webpage_url': info.get('webpage_url'), 'thumbnail': info.get('thumbnail'), 'duration': info.get('duration',0)}
    async def play_next(self, guild):
        q = self.get_queue(guild.id)
        vc = guild.voice_client
        if not q or not vc: return
        url, title, thumb = q.pop(0)
        source = discord.FFmpegPCMAudio(url, **FFMPEG_OPTIONS)
        def after(e):
            coro = self.play_next(guild)
            asyncio.run_coroutine_threadsafe(coro, self.bot.loop)
        vc.play(source, after=after)
        try: await guild.me.edit(mute=False, deafen=False)
        except: pass
    async def play(self, interaction, query):
        if not interaction.response.is_done():
            await interaction.response.defer()
        vc = await self.join(interaction)
        if not vc: return
        result = self.search(query)
        q = self.get_queue(interaction.guild.id)
        q.append((result['url'], result['title'], result.get('thumbnail')))
        if not vc.is_playing():
            await self.play_next(interaction.guild)
            embed = discord.Embed(title="🎶 Đang Phát", description=f"**{result['title']}**", color=0x0064FF, timestamp=datetime.datetime.now())
            if result.get('thumbnail'): embed.set_thumbnail(url=result['thumbnail'])
            embed.set_footer(text="Powered by Meta AI x Spotify Bot", icon_url="https://upload.wikimedia.org/wikipedia/commons/a/ab/Meta-Logo.png")
            await interaction.followup.send(embed=embed)
        else:
            await interaction.followup.send(f"✅ Đã thêm vào hàng đợi: **{result['title']}**")

voice = Voice(bot)

# ===== Events =====
@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"Meta AI x Spotify Bot online! {bot.user}")

@bot.event
async def on_voice_state_update(member, before, after):
    if member == bot.user and after.channel:
        try:
            await member.edit(mute=False, deafen=False)
        except:
            pass

# ===== Slash Commands =====
@bot.tree.command(name="mic", description="Auto bật/tắt mic cho bot")
@app_commands.describe(mode="Chọn on/off")
@app_commands.choices(mode=[
    app_commands.Choice(name="Bật mic 🎙️", value="on"),
    app_commands.Choice(name="Tắt mic 🔇", value="off")
])
async def mic_slash(interaction: discord.Interaction, mode: str):
    if not interaction.user.voice:
        await interaction.response.send_message("Sen vào voice đi đã!", ephemeral=True)
        return
    if interaction.guild.voice_client is None:
        await interaction.user.voice.channel.connect(self_deaf=False, self_mute=False)
    if mode == "on":
        await interaction.guild.me.edit(mute=False, deafen=False)
        await interaction.response.send_message("🎙️ `/mic` Đã auto BẬT MIC rồi Sen ơi! Yè ye!")
    else:
        await interaction.guild.me.edit(mute=True)
        await interaction.response.send_message("🔇 Đã tắt mic!")

@bot.tree.command(name="play", description="Phát nhạc")
async def play_cmd(interaction: discord.Interaction, query: str):
    await voice.play(interaction, query)

@bot.tree.command(name="skip", description="Skip bài")
async def skip_cmd(interaction: discord.Interaction):
    vc = interaction.guild.voice_client
    if vc and vc.is_playing():
        vc.stop()
        await interaction.response.send_message("⏭️ Đã skip!")
    else:
        await interaction.response.send_message("❌ Không có gì đang phát!", ephemeral=True)

@bot.tree.command(name="stop", description="Dừng bot")
async def stop_cmd(interaction: discord.Interaction):
    q = voice.get_queue(interaction.guild.id)
    q.clear()
    vc = interaction.guild.voice_client
    if vc: await vc.disconnect()
    await interaction.response.send_message("🛑 Đã dừng!")

bot.run(os.getenv("DISCORD_TOKEN"))