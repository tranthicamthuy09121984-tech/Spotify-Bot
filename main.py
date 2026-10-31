# utf-8
import os
import discord
from discord.ext import commands
from discord import app_commands
from flask import Flask
from threading import Thread
import asyncio

# Import module của sen
from voice import Voice 

app = Flask('')
@app.route('/')
def home(): return "Nguyez FF + Zing + YTMusic Online!"
@app.route('/healthz')
def healthz(): return "OK", 200

Thread(target=lambda: app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000))), daemon=True).start()

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True
bot = commands.Bot(command_prefix="/", intents=intents)

voice_handler = Voice(bot)

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"Bot {bot.user} online! Meo!")

@bot.tree.command(name="mic", description="Tự động bật/tắt mic bot")
@app_commands.choices(mode=[
    app_commands.Choice(name="Bật mic", value="on"),
    app_commands.Choice(name="Tắt mic", value="off")
])
async def mic_slash(interaction: discord.Interaction, mode: str):
    if not interaction.user.voice:
        await interaction.response.send_message("Vào voice trước bạn ơi!", ephemeral=True)
        return
    
    vc = interaction.guild.voice_client
    if vc is None:
        vc = await interaction.user.voice.channel.connect(self_deaf=False, self_mute=False)
    
    # Đây mới là chỗ quan trọng để mở mic phát nhạc
    if mode == "on":
        await interaction.guild.me.edit(mute=False, deafen=False)
        # Đảm bảo voice client cũng không tự mute
        vc = interaction.guild.voice_client
        if vc:
            await vc.guild.change_voice_state(channel=vc.channel, self_mute=False, self_deaf=False)
        await interaction.response.send_message("Đã bật mic rồi sen ơi! 🔊", ephemeral=True)
    else:
        await interaction.guild.me.edit(mute=True, deafen=False)
        await interaction.response.send_message("Đã tắt mic!", ephemeral=True)

@bot.tree.command(name="play", description="Phát nhạc Zing MP3 + Youtube Music")
async def play_cmd(interaction: discord.Interaction, query: str):
    if not interaction.user.voice:
        return await interaction.response.send_message("Vào voice trước bạn ơi!", ephemeral=True)
    
    await interaction.response.defer()

    vc = interaction.guild.voice_client
    if vc is None:
        vc = await interaction.user.voice.channel.connect(self_deaf=False, self_mute=False)
    
    # Luôn mở mic trước khi phát
    await interaction.guild.me.edit(mute=False, deafen=False)
    await vc.guild.change_voice_state(channel=vc.channel, self_mute=False, self_deaf=False)

    try:
        # voice_handler.search của sen phải trả về url audio, không phải title
        result = await voice_handler.search_and_get_url(query)
        if not result:
            return await interaction.followup.send(f"Không tìm thấy: {query}")

        await voice_handler.play(vc, result['url'])
        await interaction.followup.send(f"Đang phát: **{result['title']}** 🎵")
    except Exception as e:
        print(e)
        await interaction.followup.send(f"Lỗi phát nhạc: {e}")

@bot.tree.command(name="stop", description="Dừng nhạc và out voice")
async def stop_cmd(interaction: discord.Interaction):
    vc = interaction.guild.voice_client
    if vc:
        await vc.disconnect()
        await interaction.response.send_message("Bye bạn, out đây!")
    else:
        await interaction.response.send_message("Bot có ở trong voice đâu!", ephemeral=True)

bot.run(os.getenv("DISCORD_TOKEN"))