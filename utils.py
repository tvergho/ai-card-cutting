import openai
import tiktoken
import json
from datetime import datetime

encoding = tiktoken.encoding_for_model("text-curie-001")

def num_tokens_from_string(string):
    """Returns the number of tokens in a text string."""
    num_tokens = len(encoding.encode(string))
    return int(num_tokens)

def format_prompt_for_openai_completion(tag, bodyText):
  return f"Tag: {tag}\n\nInput: {bodyText}\n\n###\n\nHighlighted Text:"

def get_completion(prompt, model, debug=False):
  try:
    num_tokens_in_prompt = num_tokens_from_string(prompt)
    if num_tokens_in_prompt > 1800:
      print("Prompt too long")
      return None

    print("Max tokens: " + str(min(2048-num_tokens_in_prompt, num_tokens_in_prompt)))
    response = openai.Completion.create(
      model=model,
      prompt=prompt,
      max_tokens=min(2048-num_tokens_in_prompt, num_tokens_in_prompt),
      temperature=0,
      stop=["\n", "END"]
    )
    choices = response.choices
    output = choices[0].text.strip()

    if debug:
      print(output)

    output_arr = json.loads(output.strip())
    return output_arr
  except Exception as e:
    print(e)
    return None

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
