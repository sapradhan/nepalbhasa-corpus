## To crawl

Use [scrapy](https://github.com/scrapy/scrapy) 2.6+

    scrapy crawl -O nepalbhasatimes_raw.jsonl:jsonl nepalbhasatimes
    scrapy crawl -O nepalmandal_raw.jsonl:jsonl nepalmandal

## To cleanup and convert to Newa

    python main.py --input nepalmandal_raw.jsonl --clean nepalmandal_clean.jsonl --convert nepalmandal_newa.jsonl

## To compile into a single txt file (Devanagari only)

    python main.py --compile compiled.txt --jsonl_dir jsonl
