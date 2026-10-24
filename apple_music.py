import requests

class AppleMusicDiscord:
    def discord(self):
        return "Apple Music Module Ready - Guest"

    def search(self, query):
        # iTunes Search API public - không cần key, không cần login
        url = f"https://itunes.apple.com/search?term={query}&media=music&limit=1"
        try:
            res = requests.get(url, timeout=5).json()
            if res['resultCount'] > 0:
                song = res['results'][0]
                return {
                    "title": song['trackName'],
                    "artist": song['artistName'],
                    "album": song['collectionName'],
                    "url": song['trackViewUrl'],
                    "preview": song['previewUrl'], # link nghe thử 30s
                    "artwork": song['artworkUrl100']
                }
        except:
            return None
        return None