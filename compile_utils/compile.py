import os
import json
import re


def compile(compiled, jsonl_dir):
    corpus_files = os.listdir(jsonl_dir)

    for file in corpus_files:
        with open(f"{jsonl_dir}/{file}", "r", encoding='utf-8') as raw:
            content = raw.readlines()

            for line in content:
                json_line = json.loads(line)

                text = json_line["text"]

                clean_text = text.replace("य्", "य्‌") # य् without zwnj to य् with zwnj
                clean_text = clean_text.replace("।", "। ").replace("?", " ? ")
                clean_text = clean_text.replace("\n", " ")

                # need to remove roman and special characters

                clean_text = re.sub(' +', ' ', clean_text)
                clean_text = re.sub('#\s+', '', clean_text)
                clean_text = re.sub('\n+', '\n', clean_text)

                if clean_text != "" and clean_text != "'": 
                    compiled.write(clean_text.strip() + " ")