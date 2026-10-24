import discord

class CameraDiscord:
    def discord(self):
        return "Camera Module Ready"

def setup(bot):
    @bot.tree.command(name="camera", description="Bật/tắt camera ảo trong voice")
    async def camera(interaction: discord.Interaction):
        # Discord bot không bật cam thật được, mình làm hiệu ứng
        embed = discord.Embed(
            title="📸 Camera Discord",
            description="Bot đã bật camera ảo!",
            color=0xFF00FF
        )
        embed.add_field(name="Trạng thái", value="🟢 Đang phát video", inline=True)
        embed.add_field(name="Phòng", value=interaction.user.voice.channel.name if interaction.user.voice else "Chưa vào phòng", inline=True)
        embed.set_image(url="https://media.tenor.com/2uyENRuvV-0AAAAC/coding.gif")
        embed.set_footer(text="Được tạo bằng Pythonn 💝", icon_url="attachment://python.png")
        
        try:
            file = discord.File("python.png", filename="python.png")
            await interaction.response.send_message(embed=embed, file=file)
        except:
            await interaction.response.send_message(embed=embed)