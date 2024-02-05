import jsonlines
import argparse
import os

import conversion_utils
import compile_utils

parser = argparse.ArgumentParser(description='Convert scraped articles in devanagari script to Prachalit (Newa) script. Each json can have header and text keys that will be converted ')

parser.add_argument('--input', metavar='INPUT_JSONL', type=argparse.FileType('r'), help='input jsonl file')

parser.add_argument('--clean', metavar='INTERMEDIATE_JSONL', type=argparse.FileType('w'), help='output filename for intermediate cleaned in devanagari')

parser.add_argument('--convert', metavar='OUTPUT_JSONL', type=argparse.FileType('w'), help='output filename for converted output in Prachalit (Newa) script')

parser.add_argument('--compile', metavar='OUTPUT_TXT', type=argparse.FileType('w'), help='output filename for cleaned and compiled text in Devanagari')

parser.add_argument('--jsonl_dir', metavar='JSONL_DIR', help='directory containing jsonl files')

args = parser.parse_args()

with jsonlines.open(args.input.name if args.input else os.devnull) as posts,\
    jsonlines.open(args.clean.name if args.clean else os.devnull, mode='w') as clean_deva,\
        jsonlines.open(args.convert.name if args.convert else os.devnull, mode='w') as newa,\
        open(args.compile.name if args.compile else os.devnull, mode='a') as compiled:
    if args.compile:
        compile_utils.compile(compiled, args.jsonl_dir)
    elif args.input:
        count = 0
        for post in posts:
            if args.clean:
                post['header'] = conversion_utils.cleanup(post.get("header", ""))
                post['text'] = conversion_utils.cleanup(post['text'])
                clean_deva.write(post)

            if args.convert:
                post['header'] = conversion_utils.convert_dev_newa(post.get("header", "")) 
                post['text'] = conversion_utils.convert_dev_newa(post['text'])
                newa.write(post)
            
            count = count + 1
            if count % 100 == 0:
                print (count, " records processed")
        
        print ("Number of posts: ", count)



