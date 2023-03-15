import os
import openai
import json
from dotenv import load_dotenv
import argparse
from utils import (
  format_prompt_for_openai_completion, get_completion, create_openai_file, list_openai_files, list_finetunes, 
  create_finetune, get_finetune, calculate_fine_tuning_cost)
import readline

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# FILL THESE IN
underline_model = "curie:ft-personal-2023-01-26-03-54-27"
# highlight_model = "curie:ft-personal-2023-01-26-04-52-23"
highlight_model = "babbage:ft-personal:highlight-2023-03-14-23-57-55"
emphasis_model = "babbage:ft-personal:emphasis-2023-03-15-00-29-12"
# emphasis_model = "curie:ft-personal-2023-01-26-15-57-42"

model_name_to_id = {
  "underline": underline_model,
  "highlight": highlight_model,
  "emphasis": emphasis_model
}

if __name__=="__main__":
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
      prompt = format_prompt_for_openai_completion(tag, bodyText)
      output_arr = get_completion(prompt, model, debug=args.debug)

      if output_arr is None:
        print("No output")
      else:
        output_str = " ".join(output_arr)
        print(f"{args.model.capitalize()} text: " + output_str)
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
    assert args.list in ["files", "finetunes"], "Please specify a valid list type (files, finetunes)"
    if args.list == "files":
      list_openai_files()
    else:
      if args.finetune_id is None:
        list_finetunes()
      else:
        get_finetune(args.finetune_id)
  elif args.step == "cost":
    assert args.file is not None and os.path.isfile(args.file), "Please specify a valid file path"
    calculate_fine_tuning_cost(args.file)


# highlight_response = openai.Completion.create(
#   model=highlight_model,
#   # prompt=test.split(" \n\nInput: ")[0] + " \n\nInput: " + output_str + "\n\n###\n\nHighlighted Text:",
#   prompt=test,
#   max_tokens=int(len(test)/4),
#   temperature=0,
#   stop="\n"
# )

# highlight_choices = highlight_response.choices
# highlight_output = highlight_choices[0].text
# highlight_output_arr = json.loads(highlight_output)
# highlight_output_str = " ".join(highlight_output_arr)
# print("Highlighted text: ")
# print(highlight_output_arr)

# emphasis_response = openai.Completion.create(
#   model=emphasis_model,
#   prompt=test.split(" \n\nInput: ")[0] + " \n\nInput: " + output_str + "\n\n###\n\nHighlighted Text:",
#   max_tokens=int(len(output_str)/4),
#   temperature=0,
#   stop="\n"
# )

# emphasis_choices = emphasis_response.choices
# emphasis_output = emphasis_choices[0].text
# emphasis_output_arr = json.loads(emphasis_output)
# emphasis_output_str = " ".join(emphasis_output_arr)
# print("Emphasized text: ")
# print(emphasis_output_arr)


# response = openai.FineTune.create(training_file=file_name, model="curie")
# response = openai.FineTune.retrieve(id="ft-N59sbYVhMZZgZOIDaxKqjPlg")
# response = openai.FineTune.list()
# print(response)



# print(openai.File.list())
# openai.File.create(
#   file=open("output-emphasis.jsonl", "rb"),
#   purpose='fine-tune',
#   user_provided_filename="output-emphasis"
# )
