import argparse
from datetime import datetime
import os
from pathlib import Path
import shutil

# Define extension-based category mapping
CATEGORIES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp"],
    "Documents": [".pdf", ".docx", ".doc", ".txt", ".xlsx", ".pptx", ".csv"],
    "Archives": [".zip", ".rar", ".tar", ".gz", ".7z"],
    "Media": [".mp4", ".mkv", ".avi", ".mov", ".mp3", ".wav"],
    "Code": [".py", ".js", ".html", ".css", ".cpp", ".java", ".sql"]
}

def get_category(extension):
    for category, extensions in CATEGORIES.items():
        if extension.lower() in extensions:
            return category
    return "Others"

def get_unique_destination(dest_path):
    """Handles duplicate files by appending an incremental suffix if file exists."""
    if not dest_path.exists():
        return dest_path
    
    directory = dest_path.parent
    stem = dest_path.stem
    suffix = dest_path.suffix
    
    counter = 1
    while True:
        new_name = f"{stem}_{counter}{suffix}"
        new_path = directory / new_name
        if not new_path.exists():
            return new_path
        counter += 1

def organize_directory(source_dir, dry_run=False):
    source_path = Path(source_dir)
    
    if not source_path.exists() or not source_path.is_dir():
        print(f"Error: The directory '{source_dir}' does not exist or is not a valid directory.")
        return

    print(f"\n--- Scanning Directory: {source_path.resolve()} ---")
    if dry_run:
        print("[DRY RUN MODE ENABLED - No actual file modifications will occur]\n")

    files_found = 0
    moved_count = 0

    for item in source_path.iterdir():
        if item.is_file():
            # Skip hidden files or the script itself if placed inside
            if item.name.startswith('.'):
                continue
                
            files_found += 1
            ext = item.suffix
            category = get_category(ext)
            
            target_folder = source_path / category
            target_file_path = target_folder / item.name
            
            # Handle duplicates safely
            final_target_path = get_unique_destination(target_file_path)
            
            if dry_run:
                print(f"[PREVIEW] Would move: '{item.name}' ➔ '{category}/{final_target_path.name}'")
            else:
                try:
                    target_folder.mkdir(exist_ok=True)
                    shutil.move(str(item), str(final_target_path))
                    print(f"[SUCCESS] Moved: '{item.name}' ➔ '{category}/{final_target_path.name}'")
                    moved_count += 1
                except Exception as e:
                    print(f"[ERROR] Could not move '{item.name}': {e}")

    print(f"\nScan complete. Total files processed: {files_found}")
    if not dry_run:
        print(f"Total files successfully organized: {moved_count}")

def main():
    parser = argparse.ArgumentParser(description="Automated File Organizer - CodeNova Task 3")
    parser.add_argument("path", type=str, help="Path to the target directory to organize")
    parser.add_argument("--dry-run", action="store_true", help="Perform a dry-run preview without moving files")
    
    args = parser.parse_args()
    organize_directory(args.path, dry_run=args.dry_run)

if __name__ == "__main__":
    main()