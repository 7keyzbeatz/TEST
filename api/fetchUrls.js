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

  // Filter out audio-only streams and choose the last video stream
  const videoStreams = m3u8Urls.filter(url => !url.includes('audio'));
  
  if (videoStreams.length === 0) {
    return null; // No valid video streams found
  }

  // Return the last stream (last in the filtered list)
  const lastStreamUrl = videoStreams[videoStreams.length - 1];
  
  return lastStreamUrl;
}

// Export the handler as the default export
export default handler;
