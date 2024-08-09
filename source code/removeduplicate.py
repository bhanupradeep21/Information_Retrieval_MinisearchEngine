def remove_duplicate_lines(input_file, output_file):
    print('started removing duplicates........')
    with open(input_file, 'r') as file:
        lines = file.readlines()

    unique_lines = set(lines)

    with open(output_file, 'w') as file:
        file.writelines(unique_lines)

# Example usage:
input_file_path = 'links.txt'
output_file_path = 'unique_links.txt'

remove_duplicate_lines(input_file_path, output_file_path)