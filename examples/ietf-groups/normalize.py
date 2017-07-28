"""
Produces a normalized and validated list of mailing list archive URLs.

Parses URLs one-per-line from FILE_NAME, uses BigBang to normalize, attempts
to load every URL to validate. Outputs to OUT_FILE_NAME.
"""

import bigbang.mailman
import requests

FILE_NAME = 'ietf_lists.txt'
OUT_FILE_NAME = 'ietf_lists_normalized.txt'

def main():
    """Executes normalize script functionality."""
    with open(FILE_NAME, 'r') as in_file:
        changed = 0

        normalized_urls = []
        for url_line in in_file:
            url = url_line.strip()
            new_url = bigbang.mailman.normalize_archives_url(url)
            normalized_urls.append(new_url)
            if new_url != url:
                changed += 1

        print '# %d changed out of %d total' % (changed, len(normalized_urls))

        valid_urls = []
        for url in normalized_urls:
            try:
                response = requests.get(url)
                response.raise_for_status() # throws if not a good status code
                valid_urls.append(url)
            except requests.exceptions.RequestException as exception:
                print '# could not load %s with error %s' % (url, exception.message)

    with open(OUT_FILE_NAME, 'w') as out_file:
        for url in valid_urls:
            out_file.write('%s\n' % url)

if __name__ == '__main__':
    main()
