const fetch = require('node-fetch');

module.exports = async (req, res) => {
  const UPSTASH_URL = process.env.UPSTASH_REDIS_REST_URL;
  const UPSTASH_TOKEN = process.env.UPSTASH_REDIS_REST_TOKEN;

  // Add CORS headers so Shields.io can fetch it cleanly
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Cache-Control', 's-maxage=0, stale-while-revalidate=0');

  if (!UPSTASH_URL || !UPSTASH_TOKEN) {
    return res.status(500).json({ 
      schemaVersion: 1,
      label: 'SENTINEL ERROR',
      message: 'CREDENTIALS MISSING',
      color: 'red'
    });
  }

  try {
    // Increment the view count in Redis
    const response = await fetch(`${UPSTASH_URL}/incr/portfolio_views`, {
      headers: { Authorization: `Bearer ${UPSTASH_TOKEN}` }
    });
    
    if (!response.ok) {
        throw new Error(`Upstash error: ${response.statusText}`);
    }

    const { result: count } = await response.json();

    // Return the Shields.io JSON schema
    // Tokyonight: Blue (#7aa2f7), Orange (#ff9e64)
    res.status(200).json({
      schemaVersion: 1,
      label: 'SENTINEL VIEWS',
      message: count.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ","),
      color: parseInt(count) > 1000 ? 'ff9e64' : '7aa2f7',
      labelColor: '1a1b26',
      style: 'for-the-badge'
    });
  } catch (err) {
    res.status(500).json({ 
      schemaVersion: 1,
      label: 'SENTINEL ERROR',
      message: 'DB TIMEOUT',
      color: 'red'
    });
  }
};
