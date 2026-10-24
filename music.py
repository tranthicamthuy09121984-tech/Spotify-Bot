import discord
from yt_dlp import YoutubeDL

class MusicDiscord:
    def discord(self):
        return "Music Module Ready"

YTDL = YoutubeDL({'format': 'bestaudio/best', 'quiet': True, 'noplaylist': True})
FFMPEG = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

def setup(bot):
    @bot.tree.command(name="music_play", description="Phát nhạc nhanh")
    async def music_play(interaction: discord.Interaction, query: str):
        if not interaction.user.voice:
            return await interaction.response.send_message("❌ Vào voice trước!", ephemeral=True)
        
        await interaction.response.defer()
        vc = interaction.guild.voice_client or await interaction.user.voice.channel.connect()
        
        info = YTDL.extract_info(f"ytsearch:{query}", download=False)['entries'][0]
        
        vc.play(discord.FFmpegPCMAudio(info['url'], **FFMPEG))
        await interaction.followup.send(f"🎶 Đang phát: **{info['title']}**")

    @bot.tree.command(name="music_stop", description="Dừng nhạc")
    async def music_stop(interaction: discord.Interaction):
        vc = interaction.guild.voice_client
        if vc and vc.is_playing():
            vc.stop()
            await interaction.response.send_message("🛑 Đã dừng nhạc!")
        else:
            await interaction.response.send_message("❌ Không có nhạc!")