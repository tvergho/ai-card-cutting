# Cut Cards with AI

This is in beta. It will work for fine about 60 percent of cards, overhighlight about 20 percent, underhighlight/highlight randomly about 15 percent, and freeze/crash Word on the rest. It works better on highlighting manually pre-underlined cards. It also tends to freeze or take a long time on long cards.

You may get better results with more data, or training a higher-quality model (which costs more).
## How to Use
### Setup
1. Install [Python](https://www.python.org/downloads/macos/) for Mac. Would recommend version 3.10 or lower.
2. Install dependencies:
```
pip install -r requirements.txt
```
3. Install [conda](https://docs.anaconda.com/anaconda/install/mac-os/).
4. Clone this git repository. You need to keep this on a consistent location on your computer for inference to continue to work.

### Process Your Data
1. First, generate the training data from a collection of cards. This was tested on roughly 500 samples of consistent formatting and style. 200-1000 should be used for optimal results (more is better). Put your cards in documents in the `data` folder.
  - Optionally use the pre-generated .jsonl files in the `data` folder, in which case you can skip directly to the fine-tuning stage.
  - The model will automatically split up long cards for you (just as it does during inference).
2. Run the following command to generate data files for each model:
```
python parse.py data -o underlines.jsonl --field underlines
python parse.py data -o highlights.jsonl --field highlights --input_field underlines
python parse.py data -o emphasis.jsonl --field emphasis --input_field underlines
```
3. Normalize the files with the `openai` tool:
```
openai tools fine_tunes.prepare_data -f emphasis.jsonl
openai tools fine_tunes.prepare_data -f highlights.jsonl
openai tools fine_tunes.prepare_data -f underlines.jsonl
```
Use these newly prepared files for the fine-tuning stage.

### Fine-tune the Models
1. Put your [OpenAI API key](https://help.openai.com/en/articles/4936850-where-do-i-find-my-secret-api-key) into a file called `.env` in the root directory. It should look like this:
```
OPENAI_API_KEY=sk-your-key-here
```
2. Upload each of your files to OpenAI, and start training (repeat for each model):
```
python finetune.py file -f emphasis.jsonl
python finetune.py tune -f YOUR_FILE_ID
```
3. You can monitor the progress of your fine-tuning or retrieve file IDs using the `list` command:
```
python finetune.py list -l files
python finetune.py list -l finetunes --finetune_id YOUR_FINETUNE_ID
```
4. Replace the model IDs in `constants.py` with the IDs of your newly trained models.

You can use the utility below to calculate the cost of finetuning each of the OpenAI base models. The default (and recommended) is Babbage, which should cost less than $1 for a reasonably-sized dataset for each model. More advanced models may be more accurate, but will cost more.
```
python finetune.py cost -f emphasis.jsonl
```

### Integrate with Verbatim
1. Move (or copy) the `openaipythoninterface.scpt` file to `~/Library/Application Scripts/com.microsoft.Word/`. 
2. Open in Script Editor. Replace the path on line 16 with the path to `completion.py` in this directory.
3. Install the macros in `macros.bas` to your desired location in Word. This can either be in the Verbatim template, your normal template, or individual documents for testing.
  - You can also associate keyboard shortcuts with each macro for easy use.
4. To run a macro, put your cursor in the *tag* of a card and run the macro. A few notes:
  - It may be relatively slow on long cards, particularly for underlining. You will not be able to use Word while the macro is running.
  - The formatting macros do better on consistently formatted and cleanly cited cards. In particular, it does not do well with two-line cites or paragraphs of text between the tag and cite.
  - Though the emphasis/highlighting algorithms do their best to highlight only previously underlined words, at times earlier matches may be highlighted. This is particularly evident with acronyms (e.g. "ai" in "artificial intelligence" will often highlight the first "i" in the word "artificial", not the first letter of "intelligence").
  - Save frequently – random crashes are possible.

You can also test the models from the command line.
```
python finetune.py test -m underline
```

## To Do
- [x] Write installation instructions and requirements.txt
- [ ] Fix highlight bug where un-underlined text found earlier is highlighted
- [x] Deprecate substring_locations
- [x] Remove path specific log files