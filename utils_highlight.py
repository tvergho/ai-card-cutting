from difflib import SequenceMatcher
import re
from termcolor import colored

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

def merge_tags(tags):
    merged_tags = []
    i = 0
    while i < len(tags):
        current_tag = tags[i]
        if current_tag[1] == "<h>":
            # Merge adjacent or overlapping tags
            # Find the index of the next </h> tag
            while i < len(tags) - 1 and tags[i + 1][1] != "</h>":
                i += 1

            merged_tags.append((current_tag[0], "<h>"))
            merged_tags.append((tags[i + 1][0] if i+1 < len(tags) else tags[i][0], "</h>"))
        i += 1

    return merged_tags

def highlight_substrings(text, substrings, debug=False, paragraphs=[]):
    start_location = 0
    inserted_tags = []

    for substring in substrings:
        exact_match = len(substring) == 2 or len(substring) == 3
        match = text.find(substring, start_location)

        if match == -1:
            match = find_substring_index_difflib(
                text, 
                substring if not exact_match else " " + substring + " ", 
                start_location=start_location, 
                similarity_threshold=(0.9 if not exact_match else 1)
            )

        # Try again if substring >= 3 words with the whole text
        if match == -1 and len(substring.split(" ")) >= 3:
          match = find_substring_index_difflib(text, substring)
          start_location = match + len(substring)

        elif match != -1:
            match_len = len(substring) if not exact_match else len(substring) + 1
            inserted_tags.append((match, "<h>"))
            inserted_tags.append((match + match_len, "</h>"))
            start_location = match + match_len
        else:
            if debug:
                print(f"Could not match {substring}")
            continue

    # Sort the inserted_tags by index
    inserted_tags.sort()
    merged_tags = merge_tags(inserted_tags)

    # Insert the tags into the text
    highlighted_text = ""
    prev_end = 0
    for index, tag in merged_tags:
        highlighted_text += text[prev_end:index] + tag
        prev_end = index

    # Add the remaining part of the text after the last tag
    highlighted_text += text[prev_end:]

    # Convert merged_tags to substring_locations
    substring_locations = []
    for i in range(0, len(merged_tags), 2):
        substring_locations.append((merged_tags[i][0], merged_tags[i + 1][0] - merged_tags[i][0]))

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
