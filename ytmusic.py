from ytmusicapi import YTMusic

class YTMusicDiscord:
    def __init__(self):
        # Guest không cần file auth.json
        self.ytm = YTMusic() 

    def discord(self):
        return "Youtube Music Guest - No Login Needed"

    def search(self, query):
        # Search guest là được, không cần login
        results = self.ytm.search(query, filter="songs", limit=5)
        return results[0] if results else None