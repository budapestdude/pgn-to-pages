# PGN to Pages

A web application for converting PGN (Portable Game Notation) chess files into interactive HTML tournament pages.

## Features

- **Multiple PGN Upload**: Upload and process multiple PGN files simultaneously
- **Automatic Publishing**: Tournament pages are automatically saved and published to the server
- **Interactive Tournament Pages**: Generate beautiful, interactive HTML pages for chess tournaments
- **European Championships Support**: Pre-built templates for various European chess championships
- **Export to Google Sheets**: Tournament list page formatted for easy copy/paste to spreadsheets

## Local Development

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the server:
```bash
python save_page.py
```

3. Access the application:
- Main page: http://localhost:8081/
- PGN Processor: http://localhost:8081/pgn-processor
- Tournament List: http://localhost:8081/tournaments/list

## Deployment on Railway

This application is configured for deployment on Railway.

### Quick Deploy

1. Push this repository to GitHub
2. Connect your GitHub repository to Railway
3. Railway will automatically detect the configuration and deploy

### Manual Deploy

1. Install Railway CLI:
```bash
npm install -g @railway/cli
```

2. Login to Railway:
```bash
railway login
```

3. Create a new project:
```bash
railway init
```

4. Deploy:
```bash
railway up
```

### Configuration Files

- **requirements.txt**: Python dependencies (Flask, flask-cors, gunicorn)
- **Procfile**: Specifies the web process command
- **railway.json**: Railway-specific configuration
- **runtime.txt**: Python version specification

### Environment Variables

The application automatically uses the `PORT` environment variable provided by Railway.

## Project Structure

```
PGN to Pages/
├── save_page.py              # Flask backend server
├── pgn-to-pages-live.html    # PGN processor interface
├── home.html                 # Main landing page
├── euro-*.html              # Championship-specific pages
├── tournaments/             # Generated tournament pages
│   ├── index.html
│   ├── metadata.json
│   └── *.html
├── requirements.txt         # Python dependencies
├── Procfile                # Process configuration
├── railway.json            # Railway configuration
└── runtime.txt            # Python version
```

## API Endpoints

- `POST /api/save-pages`: Save generated tournament pages
- `GET /api/list-tournaments`: List all generated tournaments
- `GET /tournaments/list`: Tournament list page for spreadsheets
- `GET /tournaments/<path>`: Serve individual tournament pages

## Usage

1. Navigate to the PGN Processor page
2. Select or drag multiple PGN files
3. Files are automatically processed and saved
4. View generated tournaments at `/tournaments/`
5. Export tournament list from `/tournaments/list`

## License

MIT