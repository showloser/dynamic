def check_line(line):
    forbidden_chars = ['/', '\\', ':', '*', '?', '"', '<', '>', '|']
    return all(char not in line for char in forbidden_chars)

def find_lines_without_chars(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
        lines_without_chars = [line.rstrip('\n') for line in lines if check_line(line)]
        return lines_without_chars

payloads = []

filename = 'payloads/payloads.txt'
lines_without_chars = find_lines_without_chars(filename)
for line in lines_without_chars:
    payloads.append(line)

import os

def rename_file_with_payloads(payloads):
    folder_path = "miscellaneous/favIconUrl_payload"
    files = os.listdir(folder_path)
    if len(files) == 0:
        print("No files found in the test folder.")
        return
    elif len(files) > 1:
        print("Multiple files found in the test folder. Please ensure there is only one file.")
        return

    old_filename = os.path.join(folder_path, files[0])
    for payload in payloads:
        input()
        new_filename = os.path.join(folder_path, payload + ".jpg")
        os.rename(old_filename, new_filename)
        print(f"File renamed to: {new_filename}")
        old_filename = new_filename



# Example usage
rename_file_with_payloads(payloads)