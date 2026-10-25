import os, discord
from discord.ext import commands
from flask import Flask
from threading import Thread
from all_app_music import AllPlayersDiscord
music = AllPlayersDiscord()

import discord
from discord import app_commands

# Nhớ có dòng này ở trên cùng
# bot = commands.Bot(...)

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"PN super đã sync lệnh /mic rồi!")

@app_commands.guilds(discord.Object(id=YOUR_GUILD_ID)) # Xóa dòng này nếu muốn global
@bot.tree.command(name="mic", description="Auto bật/tắt mic cho bot - PN super")
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
        await interaction.user.voice.channel.connect()
    
    # AUTO BẬT MIC QUAN TRỌNG NHẤT
    await interaction.guild.me.edit(mute=False, deafen=False)

    if mode == "on":
        await interaction.response.send_message("🎙️ `/mic` Đã auto BẬT MIC rồi Sen ơi! Yè ye!")
    else:
        await interaction.guild.me.edit(mute=True)
        await interaction.response.send_message("🔇 Đã tắt mic!")

# Auto fix khi bot bị mute
@bot.event
async def on_voice_state_update(member, before, after):
    if member == bot.user and after.channel:
        await member.edit(mute=False, deafen=False)

# Import 2 file Sen đã có
from zing_mp3 import ZingDiscord
from ytmusic import YTMusicDiscord
from voice import Voice

# Keep alive Render
app = Flask('')
@app.route('/')
def home_old():
    return 'Nguyez FF + Zing + YTMusic Online!'
@app.route('/healthz')
def healthz():
    return 'OK', 200
@app.route('/__old')
def home(): return "Nguyez FF + Zing + YTMusic Online!"
Thread(target=lambda: app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000))), daemon=True).start()

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True
bot = commands.Bot(command_prefix="/", intents=intents)

zing = ZingDiscord()
ytm = YTMusicDiscord()
voice = Voice(bot)

print(f"Zing: {zing.discord()}")
print(f"YTMusic: {ytm.discord()}")

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"Bot {bot.user} online với Zing + YTMusic!")

@bot.tree.command(name="play", description="Phát nhạc Zing MP3 + Youtube Music (không sợ bản quyền)")
async def play_cmd(interaction: discord.Interaction, query: str):
    if not interaction.user.voice:
        return await interaction.response.send_message("❌ Vào voice trước Sen ơi!", ephemeral=True)
    
    await interaction.response.defer()
    vc = interaction.guild.voice_client or await interaction.user.voice.channel.connect()

    # 1. Thử Zing trước
    result = zing.search(query)
    source_name = "Zing MP3"
    
    # 2. Nếu không có thì thử YTMusic
    if not result:
        result = ytm.search(query)
        source_name = "Youtube Music"
    
    # 3. Nếu vẫn không có thì fallback YouTube thường
    if not result:
        result = voice.search(query)
        source_name = "YouTube"

    if not result:
        return await interaction.followup.send("❌ Không tìm thấy bài này!")

    # Phát
    try:
        audio_url = result.get('stream_url') or result.get('url')
        # Nếu là Zing/YTMusic thì vẫn dùng yt-dlp để lấy audio
        from play import PlayView
        await voice.play(interaction, result['title'] + " " + result.get('artist',''))
        
        embed = discord.Embed(title=f"🎶 Đang phát từ {source_name}", description=f"**{result['title']}** - {result.get('artist','')}", color=0x00FF7F)
        await interaction.followup.send(embed=embed)
    except Exception as e:
        await interaction.followup.send(f"Lỗi phát: {e}")

bot.run(os.getenv("DISCORD_TOKEN"))