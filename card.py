import hashlib
from date_test import generate_date_from_cite
import re

TAG_NAME = "Heading 4"
NORMAL_NAME = "Normal"
EMPHASIS_NAME = "Emphasis"
UNDERLINE_NAME = "Underline"
LIST_PARAGRAPH_NAME = "List Paragraph"
CITE_NAME = "13 pt Bold"

class Card():
  def __init__(self, paragraphs, additional_info={}):
    if paragraphs[0].style.name != TAG_NAME or len(paragraphs) < 2:
      raise Exception("Invalid paragraph structure")

    self.paragraphs = paragraphs
    self.tag = paragraphs[0].text.strip(", ")
    self.tag_sub = ""
    for i in range(1, len(paragraphs)):
      if not any(c.isdigit() for c in paragraphs[i].text):
        self.tag_sub += paragraphs[i].text + "\n"
      else:
        self.cite = paragraphs[i].text
        self.cite_i = i
        self.body = [p.text for p in paragraphs[i+1:] if p.style.name == NORMAL_NAME or p.style.name == LIST_PARAGRAPH_NAME]
        break

    if not self.body or len("".join(self.body)) < 25:
      raise Exception("Card is too short")

    self.cite_emphasis = []
    self.highlights = []
    self.highlighted_text = []
    self.emphasis = []
    self.emphasized_text = []
    self.underlines = []
    self.underlined_text = []
    self.card_text = ""

    self.run_text = []
    self.highlight_labels = []
    self.underline_labels = []
    self.emphasis_labels = []
    self.parse_paragraphs()

    self.additional_info = additional_info
    self.object_id = hashlib.sha256(str(self).encode()).hexdigest()
    self.cite_date = generate_date_from_cite(self.cite)

  def parse_paragraphs(self):
    j = 0

    for r in self.paragraphs[self.cite_i].runs:
      run_text = r.text.strip()
      run_index = self.paragraphs[self.cite_i].text.find(run_text, j)

      if run_index == -1:
        continue
      if CITE_NAME in r.style.name or (r.style.font.bold or r.font.bold):
        self.cite_emphasis.append((run_index, run_index + len(run_text)))
      
      j = run_index + len(run_text)

    p_index = 2

    for i in range(self.cite_i + 1, len(self.paragraphs)):
      p = self.paragraphs[i]
      runs = p.runs
      j = 0
      for r in runs:
        run_text = r.text.strip()
        run_index = p.text.find(run_text, j)

        if run_index == -1:
          continue

        if r.font.highlight_color is not None:
          self.highlights.append((p_index, run_index, run_index + len(run_text)))
          self.highlighted_text.append(run_text)
          self.highlight_labels.append(1)
        else:
          self.highlight_labels.append(0)

        if UNDERLINE_NAME in r.style.name or r.font.underline or r.style.font.underline:
          self.underlines.append((p_index, run_index, run_index + len(run_text)))
          self.underlined_text.append(run_text)
          self.underline_labels.append(1)
        else:
          self.underline_labels.append(0)

        if EMPHASIS_NAME in r.style.name:
          self.emphasis.append((p_index, run_index, run_index + len(run_text)))
          self.emphasized_text.append(run_text)
          self.emphasis_labels.append(1)
        else:
          self.emphasis_labels.append(0)
        
        self.run_text.append(run_text)
        j = run_index + len(run_text)
      
      self.card_text += p.text + "\n"
      p_index += 1
  
  def __str__(self):
    return f"{self.tag}\n{self.cite}\n{self.card_text}"

  def __repr__(self):
    return f"\n{self.tag}\n{self.cite}\n{self.card_text}"