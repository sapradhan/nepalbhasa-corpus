import jsonlines
import argparse
import conversion_utils
import os

parser = argparse.ArgumentParser(description='Convert scraped articles in devanagari script to Prachalit (Newa) script. Each json can have header and text keys that will be converted ')
parser.add_argument('--input', metavar='INPUT_JSONL', required=True, type=argparse.FileType('r'), help='input jsonl file')
parser.add_argument('--clean', metavar='INTERMEDIATE_JSONL', type=argparse.FileType('w'), help='output filename for intermediate cleaned in devanagari')
parser.add_argument('--convert', metavar='OUTPUT_JSONL', type=argparse.FileType('w'), help='output filename for converted output in Prachalit (Newa) script')

args = parser.parse_args()

count = 0;

with jsonlines.open(args.input.name) as posts, jsonlines.open(args.clean.name if args.clean else os.devnull, mode='w') as clean_deva, jsonlines.open(args.convert.name if args.convert else os.devnull, mode='w') as newa:
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


