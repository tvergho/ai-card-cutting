import torch
from transformers import T5Tokenizer, T5ForConditionalGeneration

def add_example(prompt, example):
    prompt += "\n\nExample\n\"\"\""
    prompt += example
    prompt += "\n\"\"\""
    return prompt

citation = "Giles 1-20-23 (Chris, https://www.ft.com/content/95064f87-edae-431d-8aea-f6486ad5ce23)"
input_text = "Rearrange the citation to match the format of the examples. Do not output any info in the final result which is not in the Provided Citation, including the month and date."
input_text = add_example(input_text, "\n**Talki ’21** [Valentina; Professor of Law; 2021; “International Legal Personality of Artificial Intelligence”; https://doi.org/10.3390/laws10040085; Laws, Vol. 10, No. 4]")
input_text = add_example(input_text, "\n**Kerry et al. ’21** [Cameron F. Kerry, Joshua P. Meltzer, Andrea Renda; Distinguished Fellow, Governance Studies, Center for Technology Innovation; Senior Fellow at Brookings; Senior Research Fellow and Head of Global Governance; 10/25/21; ”Strengthening Global Governance”; https://www.brookings.edu/research/strengthening-cooperation-on-ai; Brookings Institution]")
input_text = add_example(input_text, "\n**Maas ’21** [Matthijs M; April 2021; https://matthijsmaas.com/uploads/Maas; University of Copenhagen]")
input_text += f"\nProvided Citation\n\"\"\"\n{citation}\n\"\"\"\n\nRearranged Citation"
print(input_text)


# device = "mps" if torch.backends.mps.is_available() else "cpu"
# if device == "cpu" and torch.cuda.is_available():
#     device = "cuda" #if the device is cpu and cuda is available, set the device to cuda
# print(f"Using {device} device") #print the device

# tokenizer = T5Tokenizer.from_pretrained("google/flan-t5-xl")
# model = T5ForConditionalGeneration.from_pretrained("google/flan-t5-xl", device_map="auto", offload_folder="./offload", load_in_8bit=False)

# input_text = "translate English to German: How old are you?"
# input_ids = tokenizer(input_text, return_tensors="pt").input_ids.to(device)

# outputs = model.generate(input_ids, max_new_tokens=30)
# print(tokenizer.decode(outputs[0]))