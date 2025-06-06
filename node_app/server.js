const express = require('express');
const multer = require('multer');
const axios = require('axios');
const path = require('path');
const fs = require('fs');

const app = express();
const upload = multer({ dest: 'uploads/' });

app.use(express.static(path.join(__dirname, 'public')));

app.post('/upload', upload.array('files'), async (req, res) => {
  try {
    const files = req.files;
    for (const file of files) {
      const formData = new FormData();
      formData.append('file', fs.createReadStream(file.path), file.originalname);
      await axios.post('http://localhost:8000/process/', formData, {
        headers: formData.getHeaders()
      });
      fs.unlinkSync(file.path); // remove temp file
    }
    res.send('Files uploaded and forwarded for processing');
  } catch (err) {
    console.error(err);
    res.status(500).send('Error processing files');
  }
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Node app listening on port ${PORT}`);
});
