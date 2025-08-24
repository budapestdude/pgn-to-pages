#!/usr/bin/env python3
"""
Simple Flask server to handle saving generated HTML pages
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import json
from datetime import datetime

app = Flask(__name__, static_folder='.')
CORS(app)

# Directory to store generated pages
PAGES_DIR = 'tournaments'

# Ensure the tournaments directory exists
if not os.path.exists(PAGES_DIR):
    os.makedirs(PAGES_DIR)

@app.route('/')
def index():
    """Serve the main home page"""
    return send_from_directory('.', 'home.html')

@app.route('/pgn-processor')
def pgn_processor():
    """Serve the PGN processor page"""
    return send_from_directory('.', 'pgn-to-pages-live.html')

@app.route('/euro-individual-women')
def euro_individual_women():
    """Serve the European Individual Women's Championship page"""
    return send_from_directory('.', 'euro individual women.html')

@app.route('/euro-women-teams')
def euro_women_teams():
    """Serve the European Women's Team Championship page"""
    return send_from_directory('.', 'euro women teams.html')

# All championship pages routes
@app.route('/euro-individual-open')
def euro_individual_open():
    return send_from_directory('.', 'euro-individual-open.html')

@app.route('/euro-teams-open')
def euro_teams_open():
    return send_from_directory('.', 'euro-teams-open.html')

@app.route('/euro-seniors-open')
def euro_seniors_open():
    return send_from_directory('.', 'euro-seniors-open.html')

@app.route('/euro-seniors-women')
def euro_seniors_women():
    return send_from_directory('.', 'euro-seniors-women.html')

@app.route('/euro-club-cup')
def euro_club_cup():
    return send_from_directory('.', 'euro-club-cup.html')

@app.route('/euro-club-cup-women')
def euro_club_cup_women():
    return send_from_directory('.', 'euro-club-cup-women.html')

@app.route('/euro-rapid-blitz-open')
def euro_rapid_blitz_open():
    return send_from_directory('.', 'euro-rapid-blitz-open.html')

@app.route('/euro-rapid-blitz-women')
def euro_rapid_blitz_women():
    return send_from_directory('.', 'euro-rapid-blitz-women.html')

@app.route('/euro-corporate')
def euro_corporate():
    return send_from_directory('.', 'euro-corporate.html')

@app.route('/euro-small-nations')
def euro_small_nations():
    return send_from_directory('.', 'euro-small-nations.html')

@app.route('/<path:path>')
def serve_static(path):
    """Serve static files"""
    return send_from_directory('.', path)

@app.route('/tournaments/list')
def tournament_list():
    """Serve tournament list page for Google Sheets"""
    return send_from_directory(PAGES_DIR, 'tournament-list.html')

@app.route('/tournaments/<path:path>')
def serve_tournament(path):
    """Serve tournament pages"""
    return send_from_directory(PAGES_DIR, path)

@app.route('/api/save-pages', methods=['POST'])
def save_pages():
    """Save generated HTML pages to the server"""
    try:
        data = request.json
        pages = data.get('pages', {})
        tournament_info = data.get('info', {})
        
        # Create a timestamp for this generation
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        saved_files = []
        
        # Save each page
        for filename, content in pages.items():
            # Save to tournaments directory
            filepath = os.path.join(PAGES_DIR, filename)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            saved_files.append(filename)
            
            # Also save index.html to root for easy access
            if filename == 'index.html':
                with open('tournaments_index.html', 'w', encoding='utf-8') as f:
                    f.write(content)
        
        # Save metadata about the tournaments
        metadata_file = os.path.join(PAGES_DIR, 'metadata.json')
        metadata = {
            'generated': timestamp,
            'tournaments': tournament_info,
            'files': saved_files
        }
        with open(metadata_file, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2)
        
        return jsonify({
            'success': True,
            'message': f'Successfully saved {len(saved_files)} pages',
            'files': saved_files,
            'timestamp': timestamp,
            'index_url': '/tournaments/index.html'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/list-tournaments', methods=['GET'])
def list_tournaments():
    """List all generated tournament pages"""
    try:
        metadata_file = os.path.join(PAGES_DIR, 'metadata.json')
        if os.path.exists(metadata_file):
            with open(metadata_file, 'r', encoding='utf-8') as f:
                metadata = json.load(f)
            return jsonify(metadata)
        else:
            return jsonify({
                'generated': None,
                'tournaments': [],
                'files': []
            })
    except Exception as e:
        return jsonify({
            'error': str(e)
        }), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8081))
    debug_mode = os.environ.get('FLASK_ENV', 'development') == 'development'
    
    print("Starting PGN to Pages server...")
    print(f"Server running at http://localhost:{port}")
    print(f"Upload PGN files at http://localhost:{port}/")
    print(f"View generated tournaments at http://localhost:{port}/tournaments/")
    
    app.run(debug=debug_mode, port=port, host='0.0.0.0')