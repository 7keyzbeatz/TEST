module.exports = async (req, res) => {
  // Example list of Twitch URLs (can be dynamically passed as input)
  const channels = [
    "https://www.twitch.tv/livethess03",
    "https://www.twitch.tv/pun1shers_tv"
  ];

  // Process each channel URL to extract the .m3u8 URL
  const results = await Promise.all(channels.map(channel => fetchM3u8Url(channel)));

  // Send a response back to the client
  return res.json({
    Type: "HTTPRequestNeeded",
    Results: results
  });
};

async function fetchM3u8Url(channelUrl) {
  try {
    const apiUrl = `https://pwn.sh/tools/streamapi.py?url=${channelUrl}`;
    const response = await fetch(apiUrl);

    if (!response.ok) {
      throw new Error(`Failed to fetch data for ${channelUrl}`);
    }

    const responseText = await response.text();
    const m3u8Url = extractUrl(responseText, ".m3u8");

    if (m3u8Url) {
      return {
        Type: "Direct",
        Result: m3u8Url,
        enabledDRM: false,
        requiredHeaders: false
      };
    } else {
      return {
        Type: "Error",
        Result: `No .m3u8 URL found for ${channelUrl}`,
        enabledDRM: false,
        requiredHeaders: false
      };
    }
  } catch (error) {
    return {
      Type: "Error",
      Result: `Error processing ${channelUrl}: ${error.message}`,
      enabledDRM: false,
      requiredHeaders: false
    };
  }
}

function extractUrl(inputString, keyword) {
  const matches = inputString.match(/"[^"]*\.m3u8[^"]*"/);
  return matches ? matches[0].replace(/"/g, '') : null;
}
