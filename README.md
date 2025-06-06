# Expense Reports Bulk Processor

This project provides a simple example of how to combine a Node.js front‑end with a Django back‑end to process files in bulk. Users can drop multiple files into the web interface. The Node.js server forwards these files to the Django API for processing.

## Node App

The Node.js server serves a basic HTML page for uploading files. Uploaded files are sent to the Django service via HTTP.

```
cd node_app
npm install
node server.js
```

## Django Backend

The Django project exposes `/process/` which accepts file uploads. Basic processing logic is implemented in `uploader/views.py`.

```
cd django_backend
pip install -r requirements.txt  # contains Django
python manage.py migrate  # optional if you plan to use models
python manage.py runserver 8000
```

Once both servers are running, open `http://localhost:3000` in your browser and upload files. They will be forwarded to the Django backend for processing.

This is only a minimal demonstration and does not include authentication or real data handling. You can extend the processing logic in `uploader/views.py` to parse expense reports or store them in a database.
