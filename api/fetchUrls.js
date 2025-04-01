// Use dynamic import for 'node-fetch'
async function handler(req, res) {
  const { channelId } = req.query;

  if (!channelId) {
    return res.status(400).json({
      Type: "Error",
      Result: "Channel ID is required",
      enabledDRM: false,
      requiredHeaders: false,
    });
  }

  const channelUrl = `https://www.twitch.tv/${channelId}`;
  try {
    const m3u8Url = await fetchM3u8Url(channelUrl);
    if (m3u8Url) {
      return res.status(200).json({
        Type: "Direct",
        Results: [{
          Type: "Video",
          Result: m3u8Url,
          enabledDRM: false,
          requiredHeaders: false,
        }],
      });
    } else {
      return res.status(404).json({
        Type: "Error",
        Result: `No valid video stream found for ${channelUrl}`,
        enabledDRM: false,
        requiredHeaders: false,
      });
    }
  } catch (error) {
    return res.status(500).json({
      Type: "Error",
      Result: `Error processing ${channelUrl}: ${error.message}`,
      enabledDRM: false,
      requiredHeaders: false,
    });
  }
}

async function fetchM3u8Url(channelUrl) {
  // Dynamically import node-fetch
  const { default: fetch } = await import('node-fetch');
  const apiUrl = `https://pwn.sh/tools/streamapi.py?url=${channelUrl}`;
  const response = await fetch(apiUrl);
  const body = await response.text();

  // Extract all the .m3u8 URLs
  const m3u8Urls = extractUrls(body);

  // Filter out audio-only streams and choose the highest quality video stream
  const videoStreams = m3u8Urls.filter(url => !url.includes('audio'));
  
  if (videoStreams.length === 0) {
    return null; // No valid video streams found
  }

  // Find the best quality stream (highest resolution)
  // Assuming the URLs contain resolution info like '1080p', '720p', etc.
  const bestQualityUrl = selectBestQuality(videoStreams);
  
  return bestQualityUrl;
}

function extractUrls(responseText) {
  // Regular expression to extract all .m3u8 URLs
  const regex = /https?:\/\/[^ ]+\.m3u8/g;
  return responseText.match(regex) || [];
}

function selectBestQuality(urls) {
  // Example: A basic way to rank by resolution
  // You can enhance this by checking bitrate or resolution more precisely
  const qualityMap = {
    "1080p": 3,
    "720p": 2,
    "480p": 1
  };

  // Rank URLs by resolution quality
  const rankedUrls = urls.sort((a, b) => {
    const aQuality = getResolutionQuality(a);
    const bQuality = getResolutionQuality(b);
    return bQuality - aQuality;
  });

  // Return the URL with the highest resolution
  return rankedUrls[0];
}

function getResolutionQuality(url) {
  // Simple function to determine the resolution quality from the URL
  // Example: '1080p' in URL would return the number 3 for highest quality
  if (url.includes('1080p')) return 3;
  if (url.includes('720p')) return 2;
  if (url.includes('480p')) return 1;
  return 0; // Default case, lowest quality
}

module.exports = { handler };
