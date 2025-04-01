const fetch = require('node-fetch'); // You need to install node-fetch if it's not already installed

module.exports = async (req, res) => {
  // Get the channel IDs from the query parameters (channel IDs only)
  const { channels } = req.query;

  // If no channel IDs are passed, return an error
  if (!channels) {
    return res.status(400).json({
      error: 'No channel IDs provided'
    });
  }

  // Parse the channel IDs (expects a comma-separated list)
  const channelIds = channels.split(',');

  // Process each channel ID to extract the .m3u8 URL
  const results = await Promise.all(channelIds.map(channelId => fetchM3u8Url(channelId)));

  // Send a response back to the client
  return res.json({
    Type: "HTTPRequestNeeded",
    Results: results
  });
};

// Function to fetch .m3u8 URL for a given channel ID
async function fetchM3u8Url(channelId) {
  try {
    // Generate the full Twitch URL using the channel ID
    const channelUrl = `https://www.twitch.tv/${channelId}`;

    // Call the external API to fetch the stream info for the channel
    const apiUrl = `https://pwn.sh/tools/streamapi.py?url=${channelUrl}`;
    const response = await fetch(apiUrl);

    if (!response.ok) {
      throw new Error(`Failed to fetch data for ${channelUrl}`);
    }

    // Get the response text
    const responseText = await response.text();
    // Extract the .m3u8 URL
    const m3u8Url = extractUrl(responseText, ".m3u8");

    // Return the result
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
      Result: `Error processing ${channelId}: ${error.message}`,
      enabledDRM: false,
      requiredHeaders: false
    };
  }
}

// Helper function to extract the URL based on the keyword (e.g., .m3u8)
function extractUrl(inputString, keyword) {
  const matches = inputString.match(/"[^"]*\.m3u8[^"]*"/);
  return matches ? matches[0].replace(/"/g, '') : null;
}
