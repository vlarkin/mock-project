const express = require('express');
const axios = require('axios');

const app = express();
const port = 3000;

app.get('/', async (req, res) => {
  try {
    const response = await axios.get('http://backend:5000/versions');
    const versions = response.data;

    res.send(`
      <h1>Service Versions</h1>
      <p>Backend: ${versions.backend}</p>
      <p>PostgreSQL: ${versions.postgres}</p>
      <p>Redis: ${versions.redis}</p>
      <div style="border:2px solid green;text-align:center;padding:1em 0;">Super Cool Feature #1</div>
    `);
  } catch (err) {
    res.status(500).send('Error fetching versions');
  }
});

app.listen(port, () => {
  console.log(`Frontend service running at http://frontend:${port}`);
});

