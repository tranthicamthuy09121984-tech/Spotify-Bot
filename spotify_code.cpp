// PN super - Spotify Bot C++
#include <iostream>
#include <string>
#include <curl/curl.h>

struct Track {
    std::string name = "PN super";
    std::string artist = "Meo & Sen";
};

class SpotifyBot {
private:
    std::string token = "SPOTIFY_TOKEN";
public:
    Track getTrack(std::string id) {
        CURL* curl = curl_easy_init();
        std::string url = "https://api.spotify.com/v1/tracks/" + id;
        std::cout << "🎧 [C++] Fetching: " << url << std::endl;
        // curl_easy_setopt... (gọi API thật)
        curl_easy_cleanup(curl);
        return Track();
    }
    void play(Track t) {
        std::cout << "▶️  Dang phat: " << t.name 
                  << " - Bot khong ra vo hoai nua!" << std::endl;
    }
};

int main() {
    SpotifyBot bot;
    Track t = bot.getTrack("4cOdK2wGLETKBW3PvgPWqT");
    bot.play(t);
    return 0;
}