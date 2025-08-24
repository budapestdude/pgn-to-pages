#!/usr/bin/env python3
"""
Script to rename tournament files and update their content with standardized names
"""

import json
import os
import re
import shutil
from pathlib import Path

def get_ordinal_suffix(number):
    """Get ordinal suffix for numbers (1st, 2nd, 3rd, etc.)"""
    last_digit = number % 10
    last_two_digits = number % 100
    
    if 11 <= last_two_digits <= 13:
        return f"{number}th"
    
    if last_digit == 1:
        return f"{number}st"
    elif last_digit == 2:
        return f"{number}nd"
    elif last_digit == 3:
        return f"{number}rd"
    else:
        return f"{number}th"

def standardize_tournament_name(original_name):
    """Convert tournament names to standard format"""
    standardized = original_name
    
    # Pattern: EU-chT 01st Final -> European Team Championships (1st)
    if re.match(r'EU-chT\s+(\d+)(st|nd|rd|th)\s+Final', standardized):
        number = int(re.search(r'(\d+)', standardized).group(1))
        ordinal = get_ordinal_suffix(number)
        standardized = f"European Team Championships ({ordinal})"
    
    # Pattern: EU-chT (Men) 09th -> European Team Championships (9th)
    elif re.match(r'EU-chT\s+\(Men\)\s+(\d+)(st|nd|rd|th)', standardized):
        number = int(re.search(r'(\d+)', standardized).group(1))
        ordinal = get_ordinal_suffix(number)
        standardized = f"European Team Championships ({ordinal})"
    
    # Pattern: EU-chT 22nd -> European Team Championships (22nd)
    elif re.match(r'EU-chT\s+(\d+)(st|nd|rd|th)', standardized):
        number = int(re.search(r'(\d+)', standardized).group(1))
        ordinal = get_ordinal_suffix(number)
        standardized = f"European Team Championships ({ordinal})"
    
    # Handle Unknown Tournament
    elif standardized == "Unknown Tournament":
        standardized = "European Championships (Unknown Event)"
    
    return standardized

def create_slug(name):
    """Create URL-friendly slug from tournament name"""
    # Remove parentheses and convert to lowercase
    slug = name.lower()
    # Replace special characters with spaces
    slug = re.sub(r'[^a-z0-9\s]', '', slug)
    # Replace multiple spaces with single hyphens
    slug = re.sub(r'\s+', '-', slug)
    # Remove leading/trailing hyphens
    slug = slug.strip('-')
    return slug

def main():
    tournaments_dir = Path("tournaments")
    metadata_file = tournaments_dir / "metadata.json"
    
    if not metadata_file.exists():
        print("❌ Metadata file not found!")
        return
    
    # Load tournament metadata
    with open(metadata_file, 'r') as f:
        metadata = json.load(f)
    
    # Create mapping of old to new filenames
    filename_mapping = {}
    updated_tournaments = []
    
    print("🔄 Processing tournaments...")
    
    for tournament in metadata['tournaments']:
        original_name = tournament['name']
        old_filename = tournament['filename']
        
        # Get standardized name and create slug
        standardized_name = standardize_tournament_name(original_name)
        slug = create_slug(standardized_name)
        new_filename = f"{slug}.html"
        
        # Store mapping
        filename_mapping[old_filename] = new_filename
        
        # Update tournament info
        tournament['name'] = standardized_name
        tournament['filename'] = new_filename
        tournament['original_name'] = original_name
        tournament['slug'] = slug
        
        updated_tournaments.append(tournament)
        
        print(f"  • {original_name}")
        print(f"    → {standardized_name}")
        print(f"    → {old_filename} → {new_filename}")
        print()
    
    # Update metadata
    metadata['tournaments'] = updated_tournaments
    metadata['filename_mapping'] = filename_mapping
    
    print("💾 Updating tournament files...")
    
    # Process each tournament file
    for old_filename, new_filename in filename_mapping.items():
        old_path = tournaments_dir / old_filename
        new_path = tournaments_dir / new_filename
        
        if old_path.exists():
            # Read the file
            with open(old_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Find the corresponding tournament data
            tournament_data = None
            for t in updated_tournaments:
                if t['filename'] == new_filename:
                    tournament_data = t
                    break
            
            if tournament_data:
                # Update the title and header with standardized name
                original_name = tournament_data.get('original_name', '')
                standardized_name = tournament_data['name']
                
                # Update <title> tag
                content = re.sub(
                    r'<title>[^<]*</title>',
                    f'<title>{standardized_name}</title>',
                    content
                )
                
                # Update h1 tag
                if original_name:
                    content = re.sub(
                        f'<h1>{re.escape(original_name)}</h1>',
                        f'<h1>{standardized_name}</h1>',
                        content
                    )
                
                # Update any navigation links that point to old filenames
                for old_ref, new_ref in filename_mapping.items():
                    content = content.replace(f'href="/tournaments/{old_ref}"', f'href="/tournaments/{new_ref}"')
                    content = content.replace(f'href="{old_ref}"', f'href="{new_ref}"')
            
            # Write to new file
            with open(new_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"  ✅ Created {new_filename}")
            
            # Remove old file if it's different from new file
            if old_path != new_path:
                os.remove(old_path)
                print(f"  🗑️  Removed {old_filename}")
    
    # Update index.html to use new filenames
    index_path = tournaments_dir / "index.html"
    if index_path.exists():
        with open(index_path, 'r', encoding='utf-8') as f:
            index_content = f.read()
        
        # Update links in index
        for old_filename, new_filename in filename_mapping.items():
            index_content = index_content.replace(f'href="/tournaments/{old_filename}"', f'href="/tournaments/{new_filename}"')
            index_content = index_content.replace(f'href="{old_filename}"', f'href="{new_filename}"')
        
        with open(index_path, 'w', encoding='utf-8') as f:
            f.write(index_content)
        
        print("  ✅ Updated index.html links")
    
    # Save updated metadata
    with open(metadata_file, 'w') as f:
        json.dump(metadata, f, indent=2)
    
    print("  ✅ Updated metadata.json")
    
    # Update files list
    metadata['files'] = ['index.html'] + [t['filename'] for t in updated_tournaments]
    
    with open(metadata_file, 'w') as f:
        json.dump(metadata, f, indent=2)
    
    print("\n🎉 All tournaments updated successfully!")
    print(f"📁 {len(filename_mapping)} files renamed and updated")
    print("🔗 All internal links updated")
    print("📝 Metadata updated with new structure")

if __name__ == "__main__":
    main()