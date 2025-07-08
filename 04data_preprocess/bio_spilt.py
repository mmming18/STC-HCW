import os
import math
from pathlib import Path


def split_bio_file(input_file, output_folder, num_parts=10):
    """
    Split a BIO annotation file into multiple parts, ensuring split points are at O tags.

    Args:
        input_file: Path to the input BIO file
        output_folder: Folder to save the split files
        num_parts: Number of parts to split the file into
    """
    # Create output folder if it doesn't exist
    Path(output_folder).mkdir(parents=True, exist_ok=True)

    # Read the entire file
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    total_lines = len(lines)
    approx_lines_per_part = math.ceil(total_lines / num_parts)

    # Get the base filename without extension
    base_name = os.path.basename(input_file)
    name_without_ext = os.path.splitext(base_name)[0]

    part_idx = 0
    start_idx = 0

    while start_idx < total_lines and part_idx < num_parts:
        # Calculate the tentative end index for this part
        end_idx = min(start_idx + approx_lines_per_part, total_lines)

        # If we're not at the end of the file, find the next O tag
        if end_idx < total_lines and part_idx < num_parts - 1:
            # Look ahead for an O tag
            while end_idx < total_lines:
                line = lines[end_idx].strip()
                # Check if the line contains a tag (assuming the tag is the last part of the line)
                parts = line.split()
                if not parts:  # Empty line
                    break
                if len(parts) >= 1 and parts[-1] == 'O':
                    break
                end_idx += 1

        # Write this part to a new file
        output_file = os.path.join(output_folder, f"{part_idx + 1:02d}_{name_without_ext}.txt")
        with open(output_file, 'w', encoding='utf-8') as f:
            f.writelines(lines[start_idx:end_idx])

        # Update indices for the next part
        start_idx = end_idx
        part_idx += 1


def process_directory(input_dir, output_dir, num_parts=10):
    """
    Process all txt files in a directory, splitting each into multiple parts.

    Args:
        input_dir: Directory containing the input txt files
        output_dir: Directory to save the split files
        num_parts: Number of parts to split each file into
    """
    # Create output directory if it doesn't exist
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    # Get all txt files in the input directory
    txt_files = [f for f in os.listdir(input_dir) if f.endswith('.txt')]

    for file in txt_files:
        input_path = os.path.join(input_dir, file)
        # Create a subdirectory for each file's parts
        file_output_dir = os.path.join(output_dir, os.path.splitext(file)[0])
        split_bio_file(input_path, file_output_dir, num_parts)
        print(f"Split {file} into {num_parts} parts in {file_output_dir}")


if __name__ == "__main__":
    # You can change these paths as needed
    input_directory = "bio_output"
    output_directory = "txt_spilt3"

    process_directory(input_directory, output_directory, num_parts= 2 )
