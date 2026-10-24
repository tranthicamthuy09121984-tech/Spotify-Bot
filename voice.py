import discord
import asyncio
from yt_dlp import YoutubeDL

# Cấu hình yt-dlp để lấy audio xịn nhất
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
    'options': '-vn'
}

ytdl = YoutubeDL(YTDL_OPTIONS)

class Voice:
    def __init__(self, bot):
        self.bot = bot
        self.queue = {}  # guild_id: [(url, title), ...]

    def get_queue(self, guild_id):
        if guild_id not in self.queue:
            self.queue[guild_id] = []
        return self.queue[guild_id]

    async def join(self, interaction):
        if not interaction.user.voice:
            await interaction.response.send_message("❌ Bạn phải vào voice trước!", ephemeral=True)
            return None
        
        channel = interaction.user.voice.channel
        vc = interaction.guild.voice_client

        if not vc:
            vc = await channel.connect()
        elif vc.channel != channel:
            await vc.move_to(channel)
        return vc

    def search(self, query):
        # Tìm nhạc
        info = ytdl.extract_info(f"ytsearch:{query}", download=False)
        if 'entries' in info:
            info = info['entries'][0]
        return {'url': info['url'], 'title': info['title'], 'webpage_url': info.get('webpage_url')}

    async def play_next(self, guild):
        q = self.get_queue(guild.id)
        vc = guild.voice_client
        if not q or not vc:
            return
        
        url, title = q.pop(0)
        source = discord.FFmpegPCMAudio(url, **FFMPEG_OPTIONS)
        
        def after_play(error):
            if error:
                print(f"Lỗi phát: {error}")
            asyncio.run_coroutine_threadsafe(self.play_next(guild), self.bot.loop)

        vc.play(source, after=after_play)
        # Gửi tin nhắn vào kênh mà người dùng gọi lệnh cuối
        # (Sen tự thêm channel send nếu muốn)

    async def play(self, interaction, query):
        await interaction.response.defer()
        vc = await self.join(interaction)
        if not vc:
            return

        # Tìm nhạc
        try:
            result = self.search(query)
        except Exception as e:
            return await interaction.followup.send(f"❌ Không tìm thấy: {e}")

        q = self.get_queue(interaction.guild.id)
        q.append((result['url'], result['title']))

        if not vc.is_playing() and not vc.is_paused():
            await self.play_next(interaction.guild)
            await interaction.followup.send(f"🎶 Đang phát: **{result['title']}**")
        else:
            await interaction.followup.send(f"✅ Đã thêm vào hàng đợi: **{result['title']}**\nVị trí #{len(q)}")

    async def skip(self, interaction):
        vc = interaction.guild.voice_client
        if vc and vc.is_playing():
            vc.stop()
            await interaction.response.send_message("⏭️ Đã skip!")
        else:
            await interaction.response.send_message("❌ Không có gì đang phát!", ephemeral=True)

    async def stop(self, interaction):
        vc = interaction.guild.voice_client
        q = self.get_queue(interaction.guild.id)
        q.clear()
        if vc:
            await vc.disconnect()
            await interaction.response.send_message("🛑 Đã dừng và rời voice!")
        else:
            await interaction.response.send_message("❌ Bot không ở trong voice!", ephemeral=True)

    async def pause(self, interaction):
        vc = interaction.guild.voice_client
        if vc and vc.is_playing():
            vc.pause()
            await interaction.response.send_message("⏸️ Đã tạm dừng!")
        else:
            await interaction.response.send_message("❌ Không có gì đang phát!")

    async def resume(self, interaction):
        vc = interaction.guild.voice_client
        if vc and vc.is_paused():
            vc.resume()
            await interaction.response.send_message("▶️ Tiếp tục phát!")
        else:
            await interaction.response.send_message("❌ Bot không bị pause!")