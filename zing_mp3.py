import requests

class ZingDiscord:
    def discord(self):
        return "Zing MP3 Guest - No Login"

    def search(self, query):
        # Zing search public, khách vẫn search được
        try:
            url = f"https://ac.zingmp3.vn/v1/web/search/song?query={query}"
            r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}).json()
            return r['data']['items'][0]
        except:
            return None