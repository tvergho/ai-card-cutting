import sys
import os
import traceback
import json
import jsonlines
from docx import Document
from card import Card, TAG_NAME

CITE_NAME = "13 pt Bold"

def parse_cites(filename):
  document = Document(filename)
  cites = []
  print("Parsing " + filename)
  print("Found " + str(len(document.paragraphs)) + " paragraphs")

  for paragraph in document.paragraphs:
    cite = paragraph.text
    for r in paragraph.runs:
      if CITE_NAME in r.style.name or (r.style.font.bold or r.font.bold):
        cite = cite.replace(r.text, "**" + r.text + "**")
    cites.append(cite)
  
  return cites

def parse_cards(filename):
  document = Document(filename)
  cards = []
  current_card = []
  print("Parsing " + filename)
  
  for paragraph in document.paragraphs:
    if paragraph.style.name == TAG_NAME:
      try:
        cards.append(Card(current_card, {}))
      except Exception as e:
        continue
      finally:
        current_card = [paragraph]
    else:
      current_card.append(paragraph)
  
  return cards

if __name__ == "__main__":
  if len(sys.argv) != 2:
    print("Usage: python3 parser.py <file.docx>")
    sys.exit(1)

  docx_name = sys.argv[1]
  if not os.path.isfile(docx_name):
    print("File not found")
    sys.exit(1)
  
  cards = parse_cards(docx_name)

  # Strip punctuation and empty strings from each card's highlighted text
  for card in cards:
    punctuation_list = [",", ".", "!", "?", ":", ";", "(", ")", "[", "]", "{", "}", "\"", "\'", "“", "”", "‘", "’"]
    # Strip punctuation from each word in list of highlighted words
    card.highlighted_text = [word.strip("".join(punctuation_list)) for word in card.highlighted_text]
    card.underlined_text = [word.strip("".join(punctuation_list)) for word in card.underlined_text]
    card.emphasized_text = [word.strip("".join(punctuation_list)) for word in card.emphasized_text]
    # Remove empty strings
    card.highlighted_text = list(filter(None, card.highlighted_text))
    card.underlined_text = list(filter(None, card.underlined_text))
    card.emphasized_text = list(filter(None, card.emphasized_text))

  # Strip \u2018 and \u2019 and \u2014 from each card's card_text, tag, and underlined_text
  for card in cards:
    card.card_text = card.card_text.replace("\u2018", "'").replace("\u2019", "'").replace("\u2014", "-")
    card.tag = card.tag.replace("\u2018", "'").replace("\u2019", "'").replace("\u2014", "-")
    card.underlined_text = [word.replace("\u2018", "'").replace("\u2019", "'").replace("\u2014", "-") for word in card.underlined_text]
    card.highlighted_text = [word.replace("\u2018", "'").replace("\u2019", "'").replace("\u2014", "-") for word in card.highlighted_text]
    card.emphasized_text = [word.replace("\u2018", "'").replace("\u2019", "'").replace("\u2014", "-") for word in card.emphasized_text]

  # json_dict = [{"prompt": f"Tag: {card.tag} \n\nInput: {' '.join(card.underlined_text)}\n###\n\nHighlighted Text:", "completion": json.dumps(card.emphasized_text) + "\n"} for card in cards]
  # json_dict = [{"prompt": f"Select text from the input for highlighting based upon the tag.\n\nTag: {card.tag}\n\nInput: {card.card_text}\n###\n\nHighlighted Text:", "completion": json.dumps(card.highlighted_text) + "<|endoftext|>"} for card in cards]
  json_dict = [{"tag": card.tag, "text": card.card_text, "highlights": json.dumps(card.highlighted_text)} for card in cards]
  json_object = json.dumps(json_dict, indent=4)

  # with open("output.txt", "w") as outfile:
  #   for item in json_dict:
  #     outfile.write(f"Select text from the input for highlighting based upon the tag.\nTag: {card.tag}\nInput: {card.card_text}Highlighted Text: " + json.dumps(card.highlighted_text))
  #     outfile.write("\n------\n")

  with jsonlines.open("validation.json", mode="w") as writer:
    writer.write_all(json_dict)