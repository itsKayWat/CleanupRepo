#!/usr/bin/env python3
import os
import shutil
import json
import argparse
import urllib.request
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional

class ProjectCleaner:
    def __init__(self):
        self.timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        self.archive_dir = f'archive_{self.timestamp}'
        
        # Default structure (can be overridden by .map file)
        self.default_structure = {
            'directories': {},
            'root_files': []
        }

    def load_structure_from_url(self, url: str) -> Dict[str, Any]:
        """Load repository structure from a URL"""
        try:
            with urllib.request.urlopen(url) as response:
                return json.loads(response.read())
        except Exception as e:
            print(f"Error loading structure from URL: {e}")
            return None

    def load_structure_from_directory(self, directory: str) -> Dict[str, Any]:
        """Create structure from a directory path"""
        try:
            directory = os.path.abspath(directory)
            if not os.path.exists(directory):
                print(f"Directory not found: {directory}")
                return None

            structure = {
                'directories': {},
                'root_files': []
            }

            # Scan directory
            for item in os.listdir(directory):
                item_path = os.path.join(directory, item)
                if os.path.isdir(item_path) and not item.startswith('.'):
                    structure['directories'][item] = {
                        'files': [],
                        'dirs': []
                    }
                    # Scan files in directory
                    for root, dirs, files in os.walk(item_path):
                        rel_path = os.path.relpath(root, item_path)
                        if rel_path == '.':
                            structure['directories'][item]['files'].extend(files)
                        else:
                            structure['directories'][item]['dirs'].append(rel_path)
                elif os.path.isfile(item_path) and not item.startswith('.'):
                    structure['root_files'].append(item)

            return structure

        except Exception as e:
            print(f"Error loading structure from directory: {e}")
            return None

    def load_structure_from_file(self, filepath: str) -> Dict[str, Any]:
        """Load repository structure from a local file"""
        try:
            # Handle both file paths and directory paths
            filepath = os.path.abspath(filepath)
            
            # If it's a directory, create structure from it
            if os.path.isdir(filepath):
                return self.load_structure_from_directory(filepath)
            
            # If it's a file, load it
            if os.path.exists(filepath):
                with open(filepath, 'r') as f:
                    return json.load(f)
            else:
                print(f"File not found: {filepath}")
                return None
                
        except Exception as e:
            print(f"Error loading structure from file: {e}")
            return None

    def create_structure_template(self, output_dir: Optional[str] = None) -> None:
        """Create a template .map file for the current directory"""
        structure = {
            'directories': {},
            'root_files': []
        }

        # Scan current directory
        for item in os.listdir('.'):
            if os.path.isdir(item) and not item.startswith('.'):
                structure['directories'][item] = {
                    'files': [],
                    'dirs': []
                }
                # Scan files in directory
                for root, dirs, files in os.walk(item):
                    rel_path = os.path.relpath(root, item)
                    if rel_path == '.':
                        structure['directories'][item]['files'].extend(files)
                    else:
                        structure['directories'][item]['dirs'].append(rel_path)
            elif os.path.isfile(item) and not item.startswith('.'):
                structure['root_files'].append(item)

        # Save template
        if output_dir:
            output_dir = os.path.abspath(output_dir)
            os.makedirs(output_dir, exist_ok=True)
            template_file = os.path.join(output_dir, 'repository_structure.map')
        else:
            template_file = 'repository_structure.map'
            
        with open(template_file, 'w') as f:
            json.dump(structure, f, indent=4)
        print(f"Created structure template: {template_file}")

    def create_clean_structure(self, structure: Dict[str, Any]) -> None:
        """Create a clean repository structure based on provided configuration"""
        print("=== Creating Clean Repository Structure ===")
        
        # Create archive directory
        os.makedirs(self.archive_dir, exist_ok=True)
        print(f"Created archive directory: {self.archive_dir}")
        
        # Move everything except .git and self to archive
        for item in os.listdir('.'):
            if (item != '.git' and 
                item != self.archive_dir and 
                item != os.path.basename(__file__) and
                not item.endswith('.map')):
                try:
                    shutil.move(item, os.path.join(self.archive_dir, item))
                except Exception as e:
                    print(f"Error moving {item}: {e}")
        
        # Create new directory structure
        for dir_name, contents in structure['directories'].items():
            os.makedirs(dir_name, exist_ok=True)
            print(f"\nCreating directory: {dir_name}")
            
            # Create subdirectories
            if 'dirs' in contents:
                for subdir in contents['dirs']:
                    subdir_path = os.path.join(dir_name, subdir)
                    os.makedirs(subdir_path, exist_ok=True)
                    print(f"  Created subdirectory: {subdir}")
            
            # Restore files
            for file in contents.get('files', []):
                src = os.path.join(self.archive_dir, dir_name, file)
                dst = os.path.join(dir_name, file)
                self._restore_file(src, dst)
        
        # Restore root files
        print("\nRestoring root level files:")
        for file in structure['root_files']:
            src = os.path.join(self.archive_dir, file)
            self._restore_file(src, file)

    def _restore_file(self, src: str, dst: str) -> None:
        """Helper method to restore a file from archive"""
        try:
            if os.path.exists(src):
                shutil.copy2(src, dst)
                print(f"  Restored: {dst}")
            else:
                print(f"  Warning: Could not find {src}")
        except Exception as e:
            print(f"  Error restoring {dst}: {e}")

    def print_final_structure(self) -> None:
        """Print the final repository structure"""
        print("\n=== Final Repository Structure ===")
        for root, dirs, files in os.walk('.'):
            if '.git' not in root and 'archive' not in root:
                level = root.replace('.', '').count(os.sep)
                indent = ' ' * 4 * level
                print(f"{indent}{os.path.basename(root) or '.'}/")
                subindent = ' ' * 4 * (level + 1)
                for f in files:
                    print(f"{subindent}{f}")

def main():
    parser = argparse.ArgumentParser(description='Universal Project Structure Cleaner')
    parser.add_argument('--url', help='URL to repository structure .map file')
    parser.add_argument('--file', help='Local .map file or directory path')
    parser.add_argument('--create-template', help='Create a template .map file in specified directory')
    args = parser.parse_args()

    cleaner = ProjectCleaner()

    if args.create_template:
        cleaner.create_structure_template(args.create_template)
        return

    structure = None
    
    if args.url:
        structure = cleaner.load_structure_from_url(args.url)
    elif args.file:
        structure = cleaner.load_structure_from_file(args.file)
    else:
        # Interactive mode
        print("Project Structure Cleaner")
        print("1. Use default structure")
        print("2. Load from URL")
        print("3. Load from local .map file or directory")
        print("4. Create template from current directory")
        
        choice = input("\nSelect option (1-4): ")
        
        if choice == '1':
            structure = cleaner.default_structure
        elif choice == '2':
            url = input("Enter URL to .map file: ")
            structure = cleaner.load_structure_from_url(url)
        elif choice == '3':
            path = input("Enter path to .map file or directory: ")
            structure = cleaner.load_structure_from_file(path)
        elif choice == '4':
            output_dir = input("Enter output directory (or press Enter for current directory): ").strip()
            cleaner.create_structure_template(output_dir if output_dir else None)
            print("\nTemplate created. Please edit it and run the script again.")
            return
        else:
            print("Invalid choice")
            return

    if not structure:
        print("No valid structure provided. Exiting.")
        return

    print("\nThis will reorganize your project directory.")
    print("All files will be safely moved to a timestamped archive directory first.")
    response = input("Continue? (y/n): ")
    
    if response.lower() == 'y':
        cleaner.create_clean_structure(structure)
        cleaner.print_final_structure()
        print("\nCleanup complete! Check the repository structure above.")
        print(f"All other files have been moved to {cleaner.archive_dir}")
    else:
        print("Operation cancelled")

if __name__ == "__main__":
    main() 