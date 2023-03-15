from difflib import SequenceMatcher
import re
from termcolor import colored

# To do:
  # Batch script for long cards
  # Macros
    # Call completion.py (and parse response)
    # Factor out string parser functions
    # Test highlighting by subsequence
  # Some problems with the substring highlighter:
    # Short strings (less than 2 characters) – sometimes latches onto start of word – maybe use regular finder for that

def find_substring_index_difflib(main_string, substring, start_location=0, similarity_threshold=0.9):
    max_similarity = 0
    index = -1

    for i in range(start_location, len(main_string) - len(substring) + 1):
        current_substring = main_string[i:i + len(substring)]
        similarity = SequenceMatcher(None, current_substring, substring).ratio()

        if similarity > max_similarity:
            max_similarity = similarity
            index = i

            if max_similarity == 1:  # Perfect match found
                break

    if max_similarity >= similarity_threshold:
        return index
    else:
        return -1

def highlight_substrings(text, substrings):
    highlighted_text = ""
    start_location = 0
    substring_locations = []

    for substring in substrings:
        # match = text.find(substring, start_location)
        match = find_substring_index_difflib(text, substring, start_location=start_location)
        if match != -1:
            highlighted_text += text[start_location:match] + "<h>" + text[match:match+len(substring)] + "</h>"
            substring_locations.append((match, len(substring)))
            start_location = match + len(substring)
        else:
            print(f"Could not match {substring}")
            continue

    # Add the remaining part of the text after the last found substring
    highlighted_text += text[start_location:]

    return highlighted_text, substring_locations

def print_colored_text(input_string, color="red"):
    pattern = r"<h>(.*?)<\/h>"
    parts = re.split(pattern, input_string)
    
    for i, part in enumerate(parts):
        if i % 2 == 0:  # Regular text
            print(part, end="")
        else:  # Text inside <h></h> tags
            print(colored(part, color), end="")
    print()
