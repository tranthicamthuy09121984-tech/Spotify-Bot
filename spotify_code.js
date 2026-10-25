// PN super - Spotify Bot JS
const SpotifyWebApi = require('spotify-web-api-node');

const spotifyApi = new SpotifyWebApi({
  clientId: 'CLIENT_ID_CUA_SEN',
  clientSecret: 'CLIENT_SECRET',
});

async function getTrack(trackId) {
  const data = await spotifyApi.clientCredentialsGrant();
  spotifyApi.setAccessToken(data.body['access_token']);
  
  const track = await spotifyApi.getTrack(trackId);
  console.log(`🎵 Đang phát: ${track.body.name} - ${track.body.artists[0].name}`);
  return track.body;
}

getTrack('4cOdK2wGLETKBW3PvgPWqT');