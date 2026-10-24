import discord
from discord.ui import View, Select, Button
import random

class PlayView(View):
    def __init__(self, voice_instance):
        super().__init__(timeout=120)
        self.voice = voice_instance
        self.selected_genre = None
        self.selected_room = None
        self.selected_query = None

        # --- 1. Chọn thể loại ---
        self.genre_select = Select(
            placeholder="🎵 Chọn thể loại nhạc...",
            options=[
                discord.SelectOption(label="Lofi Chill", value="lofi chill", emoji="🌙", description="Nhạc chill học bài, ngủ"),
                discord.SelectOption(label="Rap Việt", value="rap viet hay", emoji="🎤", description="Rap Việt hot nhất"),
                discord.SelectOption(label="Remix", value="remix tiktok 2024", emoji="🔥", description="Remix quẩy banh nóc"),
                discord.SelectOption(label="Ballad", value="ballad nhẹ nhàng", emoji="💔", description="Nhạc buồn tâm trạng"),
                discord.SelectOption(label="EDM", value="edm mix", emoji="⚡", description="EDM bay lắc"),
                discord.SelectOption(label="TikTok Trending", value="nhac tiktok trending", emoji="📱", description="Nhạc TikTok đang hot"),
            ]
        )
        self.genre_select.callback = self.genre_callback
        self.add_item(self.genre_select)

        # --- 2. Nút Play xanh ---
        self.play_btn = Button(label="▶ Play", style=discord.ButtonStyle.success, emoji="🎧")
        self.play_btn.callback = self.play_callback
        self.play_btn.disabled = True
        self.add_item(self.play_btn)

    async def genre_callback(self, interaction: discord.Interaction):
        self.selected_genre = self.genre_select.values[0]
        # Tạo list nhạc mẫu theo thể loại
        queries = {
            "lofi chill": ["lo