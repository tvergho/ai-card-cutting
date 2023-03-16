import json
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("file", type=str, help="path to a hub json file")
parser.add_argument("--print_json", action="store_true", help="print as json")
parser.add_argument("--cap", type=int, help="cap the number of cards printed", default=None)
args = parser.parse_args()

if args.file.endswith(".json"):
  with open(args.file, "r") as f:
    data = json.load(f)

    if args.cap is not None:
      data = data[:args.cap]

    for card in data:
      print(card["tag"])
      print(card["text"].replace("\n", " "))
      if args.print_json:
        print(json.dumps(card["underlines"]))
      else:
        print(", ".join(card["underlines"]))
      print("\n")
else:
  print("Must be a json file")
