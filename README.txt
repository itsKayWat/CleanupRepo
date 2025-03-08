# CleanupRepo

## Overview
CleanupRepo is a universal project structure cleaner designed to help developers standardize and organize repository structures. It allows you to reorganize your project files according to predefined templates while safely archiving existing files.

## Why CleanupRepo?
- Standardize project structures across teams
- Clean up messy repositories
- Migrate projects to new organizational structures
- Set up consistent boilerplate for new projects
- Maintain structural compliance with organizational standards

## Installation
CleanupRepo requires Python 3.6+ and uses only standard library modules.


bash
Clone the repository
git clone https://github.com/yourusername/CleanupRepo.git
Make the script executable
chmod +x cleanupRepo.py
Optional: Add to your PATH for system-wide access


## Usage

### Basic Usage
bash
python3 cleanupRepo.py


This launches interactive mode with menu options.

### Command Line Options
bash
Use a structure from URL
python3 cleanupRepo.py --url https://example.com/structure.map
Use a local structure file
python3 cleanupRepo.py --file path/to/structure.map
Use an existing directory as template
python3 cleanupRepo.py --file path/to/template_directory
Create a template from current directory
python3 cleanupRepo.py --create-template [output_directory]


### Structure Files (.map)
CleanupRepo uses JSON-formatted .map files to define repository structures:

json
{
"directories": {
"src": {
"files": ["main.py", "utils.py"],
"dirs": ["modules", "config"]
},
"docs": {
"files": ["index.md"],
"dirs": ["api", "examples"]
}
},
"root_files": ["README.md", "LICENSE", "setup.py"]
}


## Example Use Case
Imagine your team has just established coding standards that specify a particular project structure. You have several repositories that need to be updated to match this standard.

1. Create a template from a model repository:
   ```bash
   python3 cleanupRepo.py --create-template
   ```

2. Review and modify the generated repository_structure.map file

3. Apply this structure to other repositories:
   ```bash
   cd /path/to/messy/repo
   python3 /path/to/cleanupRepo.py --file /path/to/repository_structure.map
   ```

CleanupRepo will:
- Create a timestamped archive of all existing files
- Reorganize the repository according to the template
- Restore specified files to their new locations

## Safety Features
- All existing files are archived before making changes
- Preview of changes before execution
- No files are deleted, only moved

## License
MIT License