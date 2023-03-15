import openai
import tiktoken
import json
from datetime import datetime
import asyncio
from utils_highlight import highlight_substrings
from constants import MAX_PROMPT_LENGTH
import re

encoding = tiktoken.encoding_for_model("text-babbage-001")

def num_tokens_from_string(string):
    """Returns the number of tokens in a text string."""
    num_tokens = len(encoding.encode(string))
    return int(num_tokens)

def format_prompt_for_openai_completion(tag, bodyText, underlines=None):
  if underlines is None:
    # We just pass in the card body text as input
    bodyTextArr = bodyText.split(" ")
    chunk = ""
    bodyTextChunks = []
    chunk_len = 0

    for word in bodyTextArr:
      tokens = num_tokens_from_string(word)
      if chunk_len + tokens > MAX_PROMPT_LENGTH - 100:
        bodyTextChunks.append(chunk)
        chunk = ""
        chunk_len = 0 
      chunk += word + " "
      chunk_len += tokens
    bodyTextChunks.append(chunk)
    return [f"Tag: {tag}\n\nInput: {text}\n\n###\n\nHighlighted Text:" for text in bodyTextChunks]
  else:
    try:
      underlines_arr = json.loads(underlines.strip())
      chunk = []
      bodyTextChunks = []
      chunk_len = 0
      for underline in underlines_arr:
        tokens = num_tokens_from_string(underline)
        if chunk_len + tokens + 5 > MAX_PROMPT_LENGTH - 100:
          bodyTextChunks.append(chunk)
          chunk = []
          chunk_len = 0
        chunk.append(underline)
        chunk_len += tokens + 5
      bodyTextChunks.append(chunk)
      return [f"Tag: {tag}\n\nInput: {json.dumps(chunk)}\n\n###\n\nHighlighted Text:" for chunk in bodyTextChunks]
    except Exception as e:
      print(e)
      return None

def fix_escaped_unicode(s):
    def replace(match):
        unicode_code = int(match.group(1), 16)
        return chr(unicode_code)

    # Find the improperly escaped Unicode characters and replace them
    return re.sub(r'\\u([0-9a-fA-F]{4})', replace, s)

def fix_truncated_json(json_string):
    # Add the missing closing characters
    candidates = [
        json_string,
        json_string + ']',
        json_string + '"]',
        json_string.rstrip(',') + '"]',
    ]
    
    # Try to parse each candidate as JSON and return the first valid one
    for candidate in candidates:
        try:
            parsed_json = json.loads(candidate)
            return candidate
        except json.JSONDecodeError:
            pass

    # If none of the candidates are valid JSON, return the original string
    return json_string

async def get_completion(prompt, model, debug=False):
  try:
    num_tokens_in_prompt = num_tokens_from_string(prompt)
    if num_tokens_in_prompt > MAX_PROMPT_LENGTH:
      print("Prompt too long")
      return None

    if debug:
      print("Max tokens: " + str(2048-num_tokens_in_prompt))

    response = openai.Completion.create(
      model=model,
      prompt=prompt,
      max_tokens=2048-num_tokens_in_prompt-10,
      temperature=0,
      stop=["\n", "END"]
    )
    choices = response.choices
    output = choices[0].text.strip()

    if debug:
      print(output)

    output = fix_truncated_json(output.strip())
    output_arr = json.loads(output)
    return output_arr
  except Exception as e:
    print(e)
    return None

async def get_completions_from_input(tag, bodyText, model, underlines=None, debug=False, paragraphs=[]):
  if underlines is not None:
    prompts = format_prompt_for_openai_completion(tag, bodyText, underlines)
  else:
    prompts = format_prompt_for_openai_completion(tag, bodyText, None)

  if prompts is None:
    print("Invalid input")
    return None

  results = await asyncio.gather(*[get_completion(prompt, model, debug=debug) for prompt in prompts])
  if results is None or any(map(lambda x: x is None, results)):
    print("Invalid output")
    return None

  # Flatten array
  parsed_results = [item.strip() for sublist in results for item in sublist]    

  # Remove newline characters
  parsed_results = [item.replace("\n", "") for item in parsed_results]

  output_str, loc = highlight_substrings(bodyText, parsed_results, debug=debug, paragraphs=paragraphs)
  return output_str, loc


## OpenAI API

def create_openai_file(model_name, file_path):
  try:
    response = openai.File.create(
      file=open(file_path, "rb"),
      purpose='fine-tune',
      user_provided_filename=model_name
    )
    file_id = response.id
    print(f"Successfully created file from {file_path}")
    print(f"File ID: {file_id}")
  except Exception as e:
    print(e)

def list_openai_files():
  try:
    response = openai.File.list()
    for file in response["data"]:
      if file["purpose"] == "fine-tune":
        date = str(datetime.fromtimestamp(int(file["created_at"])))
        print(f"File ID: {file['id']}, created at: {date}, filename: {file['filename']}")
  except Exception as e:
    print(e)

def create_finetune(file_id, open_ai_model, model_name):
  try:
    response = openai.FineTune.create(training_file=file_id, model=open_ai_model, n_epochs=3, suffix=model_name)
    print(f"Created fine tune for file ID {file_id} with model {open_ai_model}")
    print(f"Fine tune ID: {response.id}")
  except Exception as e:
    print(e)

def list_finetunes():
  try:
    response = openai.FineTune.list()
    for finetune in response["data"]:
      date = str(datetime.fromtimestamp(int(finetune["created_at"])))
      print(f"Fine tune ID: {finetune['id']}, created at: {date}, model: {finetune['model']}, status: {finetune['status']}")
  except Exception as e:
    print(e)

def get_finetune(finetune_id):
  try:
    response = openai.FineTune.retrieve(finetune_id)
    date = str(datetime.fromtimestamp(int(response.created_at)))
    print(f"Fine tune ID: {response.id}, created at: {date}, model: {response.model}, status: {response.status}")
    for event in response.events:
      print(event["message"])
  except Exception as e:
    print(e)

def list_models():
  try:
    response = openai.Model.list()
    for model in response["data"]:
      print(f"Model: {model['id']}")
  except Exception as e:
    print(e)



## Cost calculation

def count_tokens(file_path):
    total_tokens = 0

    with open(file_path, 'r') as f:
        for line in f:
            data = json.loads(line)
            text = data.get('prompt', '') + data.get('completion', '')
            tokens = num_tokens_from_string(text)
            total_tokens += tokens

    return total_tokens

def calculate_fine_tuning_cost(file_path):
    # Define the models and their training cost per 1K tokens
    models = {
        'Ada': 0.0004,
        'Babbage': 0.0006,
        'Curie': 0.0030,
        'Davinci': 0.0300
    }

    # Count the total tokens in the .jsonl file
    total_tokens = count_tokens(file_path)

    # Calculate the total cost for fine-tuning with each model
    costs = {}
    for model, cost_per_1k_tokens in models.items():
        cost = (total_tokens / 1000) * cost_per_1k_tokens
        costs[model] = cost

    print("Cost per epoch (default 3)")
    for model, cost in costs.items():
      print(f'{model}: ${cost:.2f}')

