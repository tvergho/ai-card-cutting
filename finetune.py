import os
import openai
import json
from dotenv import load_dotenv
import argparse
from utils import (
  format_prompt_for_openai_completion, get_completion, create_openai_file, list_openai_files, list_finetunes, 
  create_finetune, get_finetune, calculate_fine_tuning_cost, list_models)
import readline
from utils_highlight import highlight_substrings, print_colored_text
import asyncio

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# FILL THESE IN
# underline_model = "curie:ft-personal-2023-01-26-03-54-27"
# highlight_model = "curie:ft-personal-2023-01-26-04-52-23"
# emphasis_model = "curie:ft-personal-2023-01-26-15-57-42"

underline_model = "babbage:ft-personal:underline-2023-03-15-01-23-34"
highlight_model = "babbage:ft-personal:highlight-2023-03-14-23-57-55"
emphasis_model = "babbage:ft-personal:emphasis-2023-03-15-00-29-12"

model_name_to_id = {
  "underline": underline_model,
  "highlight": highlight_model,
  "emphasis": emphasis_model
}

async def main():
  assert len(os.getenv("OPENAI_API_KEY")) > 0, "Please set your OPENAI_API_KEY in your .env file"

  parser = argparse.ArgumentParser()
  parser.add_argument("step", type=str, help="phase to run in (test, file, tune, list, cost)")
  parser.add_argument("--model", type=str, help="model to use (underline, highlight, emphasis, or custom)", default="underline")
  parser.add_argument("--debug", action="store_false", help="hide debug info")
  parser.add_argument("-f", "--file", type=str, help="path to file to upload or file ID to use for fine tuning")
  parser.add_argument("-l", "--list", type=str, help="in list mode, what to list (files, finetunes)")
  parser.add_argument("-oai", "--open_ai_model", type=str, help="OpenAI model to use for fine tuning (default: curie)", default="curie")
  parser.add_argument("--finetune_id", type=str, default=None)

  args = parser.parse_args()

  assert args.step in ["test", "file", "tune", "list", "cost"], "Please specify a valid step (test, file, tune, list, cost)"

  if args.step == "test":
    assert args.model in model_name_to_id, "Please specify a valid model (underline, highlight, emphasis)"
    model = model_name_to_id[args.model]

    while True:
      tag = input("Tag: ")
      bodyText = input("Body Text: ")
      if args.model != "underline":
        underlines = input("JSON formatted underlines: ")
        prompts = format_prompt_for_openai_completion(tag, bodyText, underlines)
      else:  
        prompts = format_prompt_for_openai_completion(tag, bodyText, None)

      if prompts is None:
        print("Invalid input")
        continue
      
      results = await asyncio.gather(*[get_completion(prompt, model, debug=args.debug) for prompt in prompts])
      if results is None or any(map(lambda x: x is None, results)):
        print("Invalid output")
        continue

      # Flatten array
      parsed_results = [item.strip() for sublist in results for item in sublist]     
      # Remove newline characters
      parsed_results = [item.replace("\n", "") for item in parsed_results]

      output_str, loc = highlight_substrings(bodyText, parsed_results)
      print_colored_text(output_str)
      if args.debug:
        print(loc)
  elif args.step == "file":
    if not args.list:
      assert args.file is not None and os.path.isfile(args.file), "Please specify a file to upload"
      model_name = os.path.basename(args.file).split(".")[0]
      create_openai_file(model_name, args.file)
    else:
      list_openai_files()
  elif args.step == "tune":
    assert args.file is not None, "Please specify a valid OpenAI file ID to use for fine tuning"
    create_finetune(args.file, args.open_ai_model, args.model)
  elif args.step == "list":
    assert args.list in ["files", "finetunes", "models"], "Please specify a valid list type (files, finetunes, models)"
    if args.list == "files":
      list_openai_files()
    elif args.list == "models":
      list_models()
    else:
      if args.finetune_id is None:
        list_finetunes()
      else:
        get_finetune(args.finetune_id)
  elif args.step == "cost":
    assert args.file is not None and os.path.isfile(args.file), "Please specify a valid file path"
    calculate_fine_tuning_cost(args.file)


if __name__=="__main__":
  loop = asyncio.get_event_loop()
  loop.run_until_complete(main())