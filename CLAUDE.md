# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

PGN to Pages is a web application for converting PGN (Portable Game Notation) chess files into interactive HTML tournament pages. It consists of a Flask backend server for file handling and static HTML/JavaScript frontend pages for PGN processing and display.

## Architecture

### Backend (Python/Flask)
- **save_page.py**: Flask server that serves HTML pages and provides API endpoints for saving/listing tournament pages
  - Runs on port 8080
  - Serves static files and provides REST API endpoints
  - Stores generated tournament pages in `tournaments/` directory

### Frontend (HTML/JavaScript)
- **pgn-to-pages-live.html**: Main PGN processor page with drag-and-drop file upload
- **home.html**: Landing page displaying European Chess Championships calendar
- **euro-*.html**: Individual championship type pages (e.g., euro-individual-open.html, euro-women-teams.html)
- **tournaments/**: Directory containing generated tournament pages with standardized naming

### Utilities
- **update_tournaments.py**: Script for renaming and standardizing tournament files
  - Converts tournament names to standardized format (e.g., "EU-chT 22nd" → "European Team Championships (22nd)")
  - Updates internal links and metadata

## Commands

### Running the Server
```bash
python3 save_page.py
```
Server will run at http://localhost:8080

### Processing Tournaments
```bash
python3 update_tournaments.py
```
Standardizes tournament names and updates all references

### Dependencies
- Flask 3.1.2
- flask-cors 6.0.1

Install with:
```bash
pip3 install Flask flask-cors
```

## API Endpoints

- `POST /api/save-pages`: Save generated tournament HTML pages
- `GET /api/list-tournaments`: List all generated tournament pages
- `GET /tournaments/list`: Serve tournament list page
- `GET /tournaments/<path>`: Serve individual tournament pages

## File Structure

Tournament pages are saved with standardized naming:
- Original: `EU-chT 22nd.html`
- Standardized: `european-team-championships-22nd.html`

Metadata is stored in `tournaments/metadata.json` containing:
- Generation timestamp
- Tournament information
- File mappings