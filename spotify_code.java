// PN super - Spotify Bot Java
import se.michaelthelin.spotify.SpotifyApi;
import se.michaelthelin.spotify.model_objects.specification.Track;

public class PNSuperSpotifyBot {
    private static final String CLIENT_ID = "CLIENT_ID_CUA_SEN";
    private static final String CLIENT_SECRET = "CLIENT_SECRET";

    public static void main(String[] args) {
        SpotifyApi spotifyApi = new SpotifyApi.Builder()
                .setClientId(CLIENT_ID)
                .setClientSecret(CLIENT_SECRET)
                .build();
        try {
            var credentials = spotifyApi.clientCredentials().build().execute();
            spotifyApi.setAccessToken(credentials.getAccessToken());
            
            Track track = spotifyApi.getTrack("4cOdK2wGLETKBW3PvgPWqT").build().execute();
            System.out.println("🎵 [Java] Dang phat: " + track.getName() 
                + " - " + track.getArtists()[0].getName());
            System.out.println("✅ Bot PN super da fix loi ra vo!");
            
        } catch (Exception e) {
            System.out.println("Loi: " + e.getMessage());
        }
    }
}