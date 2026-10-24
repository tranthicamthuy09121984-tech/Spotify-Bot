# Khi dùng PC mới có thể sử dụng tệp này
class WindowsMediaPlayerDiscord:
    def discord(self):
        return "Windows Media Player Module - Local Only"

    def play_local(self, file_path):
        # Chỉ chạy được trên máy tính Windows của Sen, không chạy được trên Render
        try:
            import os
            os.startfile(file_path) # Mở bằng WMP mặc định
            return f"Đang mở {file_path} bằng Windows Media Player"
        except Exception as e:
            return f"Lỗi WMP: {e}"

def setup(bot):
    import discord
    @bot.tree.command(name="wmp", description="Mở nhạc local bằng Windows Media Player (chỉ host Windows)")
    async def wmp_cmd(interaction: discord.Interaction, file: str):
        # Ví dụ: /wmp C:\Music\nhac.mp3
        wmp = WindowsMediaPlayerDiscord()
        result = wmp.play_local(file)
        await interaction.response.send_message(result)