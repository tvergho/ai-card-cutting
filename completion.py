import argparse
import openai
import asyncio
import json
import sys
from dotenv import load_dotenv
from utils import get_completions_from_input, fix_escaped_unicode
from constants import model_name_to_id
import os
import re

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

async def main():
  parser = argparse.ArgumentParser()
  # parser.add_argument('key', metavar='<key>', type=str, help='key to use for OpenAI')
  parser.add_argument('modelName', metavar='<model_name>', type=str, help='model name to use for OpenAI (underline, highlight, emphasis)')
  parser.add_argument('--tag', type=str, help='tag of the card', metavar="tag")
  parser.add_argument('--bodyText', type=str, help='body text', metavar="bodyText")
  parser.add_argument('--underlines', type=str, help='JSON formatted underlines', metavar="underlines", default=None)
  parser.add_argument('--paragraphs', type=str, metavar="paragraphs", default="0")

  args = parser.parse_args()
  bodyText = args.bodyText
  bodyText = re.sub(r"[\r\n]+", " ", bodyText)
  bodyText = bodyText.replace('\n', ' ').replace('\r', ' ')
  bodyText = bodyText.replace('\n', ' ').replace('\r', ' ')
  bodyText = bodyText.replace('\\n', ' ').replace('\\r', ' ')

  paragraphs = args.paragraphs.split(",")
  paragraphs = [int(p) for p in paragraphs]
  paragraphs = [p for p in paragraphs if p != 0]

  with open('/Users/tylervergho/test/bodyText.log', 'w') as f:
    f.write(bodyText)

  model = model_name_to_id[args.modelName]

  if args.underlines:
    args.underlines = fix_escaped_unicode(args.underlines)
  bodyText = fix_escaped_unicode(bodyText)

  if args.modelName != "underline":
    underlines = args.underlines.split(", ")
  else:
    underlines = None

  output = await get_completions_from_input(
    args.tag, 
    bodyText, 
    model, 
    underlines=json.dumps(underlines) if underlines is not None else None, 
    debug=False,
    paragraphs=paragraphs
  )

  if output is None:
    print("No output")
    return

  output_str, loc = output

  with open('/Users/tylervergho/test/completion2.log', 'w') as f:
    f.write(str(output_str))
    
  print(loc)

if __name__ == '__main__':
  # log arguments string to file for debugging
  with open('/Users/tylervergho/test/completion.log', 'w') as f:
    f.write(sys.argv[0] + " " + sys.argv[1] + " " + sys.argv[2] + " " + sys.argv[3] + " " + sys.argv[4])

  asyncio.run(main())
