from postMessageRegex import extract_unique_strings


path = 'Extensions/h1-replacer/h1-replacer(v3)_window.addEventListernerMessage/popup.js'
start_line = 2
end_line = 6


def extract_codes_postMessage(path,start_line,end_line):
  with open(path, 'r') as file:
    lines = file.readlines()

    # Adjust line numbers to Python's zero-based indexing
    start_line -= 1
    end_line -= 1

    # Trim the lines within the specified range
    code_lines = lines[start_line:end_line+1]

    # Join the trimmed lines to form the code string
    code = ''.join(code_lines)
  return code




code = extract_codes_postMessage(path,start_line,end_line)


print(code)
# print(extract_unique_strings())