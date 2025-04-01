export default async function handler(req, res) {
  // Importing node-fetch dynamically since it's an ES Module
  const { default: fetch } = await import('node-fetch');

  // Get the Twitch channel ID from the query parameters
  const { channelId } = req.query;

  // Check if a channel ID is provided
  if (!channelId) {
    return res.status(400).json({
      Type: "Error",
      Result: "Channel ID is required"
    });
  }

  // Construct the Twitch URL using the channel ID
  const channelUrl = `https://www.twitch.tv/${channelId}`;

  // Fetch the M3U8 URL for the provided channel
  const result = await fetchM3u8Url(channelUrl, fetch);

  // Send the result back as a response
  return res.json({
    Type: "HTTPRequestNeeded",
    Results: [result]
  });
}

async function fetchM3u8Url(channelUrl, fetch) {
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
