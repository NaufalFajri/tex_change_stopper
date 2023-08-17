import os
import re
import shutil

def main():
    # Read the list of strings from the input file
    with open('tex_change_table.txt', 'r') as strings_file:
        strings_to_replace = [line.strip() for line in strings_file.readlines()]

    # Define the root folder
    root_folder = r'mods\DE - Tex Change Stopper'  # Use r before the string to interpret it as a raw string

    # Traverse through the root folder and its subfolders
    for folder_path, _, file_names in os.walk(root_folder):
        for file_name in file_names:
            if file_name.endswith('.og'):
                og_file_path = os.path.join(folder_path, file_name)
                bin_file_path = og_file_path[:-3] + '.bin'

                # Copy and rename .og file to .bin
                shutil.copy2(og_file_path, bin_file_path)

                # Read the binary content of the .bin file
                with open(bin_file_path, 'rb') as bin_file:
                    bin_content = bin_file.read()

                # Perform replacements
                for string_to_replace in strings_to_replace:
                    # Convert the string to bytes
                    bytes_to_replace = bytes(string_to_replace, 'utf-8')
                    
                    # Create a regular expression pattern with word boundaries
                    pattern = rb'\b' + re.escape(bytes_to_replace) + rb'\b'
                    
                    # Replace occurrences with 00 bytes
                    bin_content = re.sub(pattern, b'\x00' * len(bytes_to_replace), bin_content)

                # Write the modified content back to the .bin file
                with open(bin_file_path, 'wb') as bin_file:
                    bin_file.write(bin_content)
                    
if __name__ == "__main__":
    main()