import os
import shutil

class AllPlayersDiscord:
    def discord(self):
        return "All Players Module - 10 Players Ready"

    PLAYERS = {
        "kmplayer": r"C:\Program Files\The KMPlayer\KMPlayer.exe",
        "jetaudio": r"C:\Program Files\JetAudio\JetAudio.exe",
        "gom": r"C:\Program Files\GOM\GOM Player\GOM.exe",
        "foobar2000": r"C:\Program Files\foobar2000\foobar2000.exe",
        "nct": "NhacCuaTui - Web",
        "groove": "Groove Music - Windows App",
        "mpc": r"C:\Program Files\MPC-HC\mpc-hc64.exe",
        "realplayer": r"C:\Program Files\Real\RealPlayer\RealPlay.exe",
        "aimp": r"C:\Program Files\AIMP\AIMP.exe",
        "wmp": r"C:\Program Files\Windows Media Player\wmplayer.exe",
    }

    def play_with(self, player_name, file_path):
        player_name = player_name.lower()
        
        if player_name == "nct":
            return f"🔗 Mở NhacCuaTui: https://www.nhaccuatui.com/tim-kiem?q={file_path}"
        if player_name == "groove":
            os.system(f'start mswindowsmusic:play?file={file_path}')
            return f"✅ Đang mở Groove Music với {file_path}"

        path = self.PLAYERS.get(player_name)
        if not path or not os.path.exists(path):
            # Thử tìm trong PATH
            exe = shutil.which(player_name)
            if exe:
                path = exe
            else:
                return f"❌ Chưa cài {player_name} trên PC này!"

        os.startfile(file_path) if player_name == "wmp" else os.spawnl(os.P_NOWAIT, path, f'"{file_path}"')
        return f"✅ Đang phát {os.path.basename(file_path)} bằng {player_name.upper()}"

# Cách dùng trong Discord:
# /playwith player:foobar2000 file:C:\Music\SeeTinh.mp3
# /playwith player:kmplayer file:C:\Music\SeeTinh.mp3
# /playwith player:aimp file:C:\Music\SeeTinh.mp3