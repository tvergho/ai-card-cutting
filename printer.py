import json
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("file", type=str, help="path to a hub json file")
parser.add_argument("--print_json", action="store_true", help="print as json")
args = parser.parse_args()

if args.file.endswith(".json"):
  with open(args.file, "r") as f:
    data = json.load(f)
    for card in data:
      print(card["tag"])
      if args.print_json:
        print(json.dumps(card["underlines"]))
      else:
        print(", ".join(card["underlines"]))
else:
  print("Must be a json file")
