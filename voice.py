import discord
import asyncio
from yt_dlp import YoutubeDL
import datetime
from discord.ext import commands
import os

intents = discord.Intents.all()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

ROLE_BOT = {
    'administrator': True
}

COMMAND_BOT = {
    'bot': True,
    'application_commands': True
}

YTDL_OPTIONS = {
    'format': 'bestaudio/best',
    'quiet': True,
    'no_warnings': True,
    'default_search': 'ytsearch',
    'source_address': '0.0.0.0',
    'noplaylist': True,
}

ZING_MP3_OPTIONS = {
    'format': 'bestaudio/best',
    'quiet': True,
    'no_warnings': True,
    'default_search': 'ytsearch',
    'source_address': '0.0.0.0',
    'noplaylist': True,
}

APPLE_MUSIC_OPTIONS = {
    'format': 'bestaudio/best',
    'quiet': True,
    'no_warnings': True,
    'default_search': 'ytsearch',
    'source_address': '0.0.0.0',
    'noplaylist': True,
}

WINDOWS_MEDIA_PLAYER_OPTIONS = {
    'format': 'bestaudio/best',
    'quiet': True,
    'no_warnings': True,
    'default_search': 'ytsearch',
    'source_address': '0.0.0.0',
    'noplaylist': True,
}

NCT = "NhacCuaTui"

NCT_OPTIONS = {
    'format': 'bestaudio/best',
    'quiet': True,
    'no_warnings': True,
    'default_search': 'ytsearch',
    'source_address': '0.0.0.0',
    'noplaylist': True,
}

FFMPEG_OPTIONS = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn -b:a 192k -af loudnorm=I=-16:TP=-1.5:LRA=11'
}

ytdl = YoutubeDL(YTDL_OPTIONS)

VOICE_CONFIG = {
    'voice_discord': True,
    'allow_mic': True,
    'auto_mic': True,
    'mic': True,
    'powered_by': 'Meta AI x Spotify Bot'
}

ROOM_CONFIG = {
    'auto_on': True,
    'music_24_7': True,
    'do_not_auto_exit_the_room': True,
    'no_cameras': True
}

class Voice:
    def __init__(self, bot):
        self.bot = bot
        self.queue = {}
        self.now_playing = {}

    def get_queue(self, guild_id):
        if guild_id not in self.queue:
            self.queue[guild_id] = []
        return self.queue[guild_id]

    async def join(self, interaction):
        if not interaction.user.voice:
            embed = discord.Embed(description="❌ Bạn phải vào voice trước đã!", color=0xFF0000)
            embed.set_footer(text="Powered by Meta AI", icon_url="https://upload.wikimedia.org/wikipedia/commons/a/ab/Meta-Logo.png")
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return None
        channel = interaction.user.voice.channel
        vc = interaction.guild.voice_client
        if not vc:
            embed = discord.Embed(description=f"⚡ **Spotify Bot** đang kết nối tới `{channel.name}`...", color=0x0064FF)
            try:
                if not interaction.response.is_done():
                    await interaction.response.send_message(embed=embed, ephemeral=True, delete_after=3)
            except:
                pass
            vc = await channel.connect(self_deaf=False, self_mute=False)
        elif vc.channel != channel:
            await vc.move_to(channel)
        try:
            await interaction.guild.me.edit(mute=False, deafen=False)
        except:
            pass
        return vc

    def search(self, query):
        print(f"[Meta AI Search] Đang tìm: {query}")
        info = ytdl.extract_info(f"ytsearch:{query}", download=False)
        if 'entries' in info:
            info = info['entries'][0]
        print(f"[Meta AI Search] Tìm thấy: {info['title']}")
        return {'url': info['url'], 'title': info['title'], 'webpage_url': info.get('webpage_url'), 'thumbnail': info.get('thumbnail'), 'duration': info.get('duration', 0)}

    async def play_next(self, guild):
        q = self.get_queue(guild.id)
        vc = guild.voice_client
        if not q or not vc:
            return
        url, title, thumb = q.pop(0)
        try:
            source = discord.FFmpegPCMAudio(url, **FFMPEG_OPTIONS)
        except Exception as e:
            print(f"[Meta AI Error] FFMPEG: {e}")
            return await self.play_next(guild)
        def after_play(error):
            if error:
                print(f"[Meta AI Error] Phát lỗi: {error}")
            coro = self.play_next(guild)
            asyncio.run_coroutine_threadsafe(coro, self.bot.loop)
        self.now_playing[guild.id] = (title, thumb)
        vc.play(source, after=after_play)
        try:
            await guild.me.edit(mute=False, deafen=False)
        except:
            pass

    async def play(self, interaction, query):
        try:
            if not interaction.response.is_done():
                await interaction.response.defer()
        except:
            pass
        vc = await self.join(interaction)
        if not vc:
            return
        async with interaction.channel.typing():
            try:
                result = self.search(query)
            except Exception as e:
                embed = discord.Embed(title="❌ Meta AI Search Failed", description=f"Không tìm thấy: {e}", color=0xFF0000)
                embed.set_footer(text="Powered by Meta AI", icon_url="https://upload.wikimedia.org/wikipedia/commons/a/ab/Meta-Logo.png")
                return await interaction.followup.send(embed=embed)
            q = self.get_queue(interaction.guild.id)
            q.append((result['url'], result['title'], result.get('thumbnail')))
            if not vc.is_playing() and not vc.is_paused():
                await self.play_next(interaction.guild)
                embed = discord.Embed(title="🎶 Meta AI và Spotify Bot Đang Phát", description=f"**{result['title']}**", color=0x0064FF, timestamp=datetime.datetime.now())
                if result.get('thumbnail'):
                    embed.set_thumbnail(url=result['thumbnail'])
                embed.set_image(url="https://i.imgur.com/wv6b8aP.gif")
                embed.add_field(name="🤖 AI Engine", value="Meta Llama Search", inline=True)
                embed.add_field(name="🎙️ Smart Mic", value="Auto ON ✅", inline=True)
                embed.add_field(name="⏱️ Duration", value=f"{result.get('duration',0)//60}:{result.get('duration',0)%60:02d}", inline=True)
                embed.set_footer(text="⚡ Powered by Meta AI x Spotify Bot I /meta", icon_url="https://upload.wikimedia.org/wikipedia/commons/a/ab/Meta-Logo.png")
                await interaction.followup.send(embed=embed)
            else:
                embed = discord.Embed(title="✅ Đã Thêm Vào Hàng Đợi", description=f"**{result['title']}**", color=0x00FF7F)
                embed.add_field(name="Vị trí", value=f"#{len(q)}", inline=True)
                embed.add_field(name="Powered by", value="Meta AI x Spotify Bot", inline=True)
                if result.get('thumbnail'):
                    embed.set_thumbnail(url=result['thumbnail'])
                embed.set_footer(text="Meta AI x Spotify Bot Queue System", icon_url="https://upload.wikimedia.org/wikipedia/commons/a/ab/Meta-Logo.png")
                await interaction.followup.send(embed=embed)

    async def skip(self, interaction):
        vc = interaction.guild.voice_client
        if vc and vc.is_playing():
            vc.stop()
            embed = discord.Embed(description="⏭️ **Spotify Bot** đã skip bài! Đang phát bài tiếp...", color=0x0064FF)
            embed.set_footer(text="Powered by Meta AI", icon_url="https://upload.wikimedia.org/wikipedia/commons/a/ab/Meta-Logo.png")
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message("❌ Không có gì đang phát!", ephemeral=True)

    async def stop(self, interaction):
        q = self.get_queue(interaction.guild.id)
        q.clear()
        vc = interaction.guild.voice_client
        if vc:
            await vc.disconnect()
            embed = discord.Embed(description="🛑 **Spotify Bot** đã dừng và rời voice. Hẹn gặp lại Sen!", color=0x0064FF)
            embed.set_footer(text="Powered by Meta AI x Spotify Bot", icon_url="https://upload.wikimedia.org/wikipedia/commons/a/ab/Meta-Logo.png")
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message("❌ Bot không ở trong voice!", ephemeral=True)

    async def pause(self, interaction):
        vc = interaction.guild.voice_client
        if vc and vc.is_playing():
            vc.pause()
            await interaction.response.send_message("⏸️ **Spotify Bot** đã tạm dừng!")
        else:
            await interaction.response.send_message("❌ Không có gì đang phát!")

    async def resume(self, interaction):
        vc = interaction.guild.voice_client
        if vc and vc.is_paused():
            vc.resume()
            await interaction.response.send_message("▶️ **Spotify Bot** tiếp tục phát!")
        else:
            await interaction.response.send_message("❌ Bot không bị pause!")

voice = Voice(bot)

@bot.event
async def on_ready():
    print("Meta AI x Spotify Bot online!")
    await bot.tree.sync()

@bot.tree.command(name="play", description="Phát nhạc Meta AI")
async def play_cmd(interaction: discord.Interaction, query: str):
    await voice.play(interaction, query)

@bot.tree.command(name="skip", description="Skip bài")
async def skip_cmd(interaction: discord.Interaction):
    await voice.skip(interaction)

@bot.tree.command(name="stop", description="Dừng bot")
async def stop_cmd(interaction: discord.Interaction):
    await voice.stop(interaction)

bot.run(os.getenv("DISCORD_TOKEN"))