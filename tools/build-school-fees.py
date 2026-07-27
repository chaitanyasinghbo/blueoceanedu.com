#!/usr/bin/env python3
"""Regenerate the data block in school-fees.js from the fees CSV.

The CSV is the source of truth for every fee on a lead row. This script is how
that stays true: edit the CSV, run this, and the site picks up the new figures.
Nothing is rounded, banded, or adjusted on the way through. A cell reading NA
becomes 0 in the data and ships to the sheet as blank.

    python3 tools/build-school-fees.py

Only the block between the generated markers in school-fees.js is rewritten.
The matching logic around it is hand-written and is never touched.

Pass --check to verify the file is already in sync without writing, which is
the useful form after editing the CSV to see whether a rebuild is pending.
"""

import argparse
import csv
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
CSV_PATH = ROOT / 'Indian_Schools_Fees_Complete_Reviewed_2026.csv'
JS_PATH = ROOT / 'school-fees.js'

BEGIN = '  /* --- generated:begin --- */'
END = '  /* --- generated:end --- */'

# One school sits in "Paud, Pune district". That is a district description, not
# a city, and it has no business in a dropdown a parent reads.
CITY_FIX = {'Paud, Pune district': 'Pune'}


def parse_fee(value):
    """A published figure in whole rupees, or 0 where the source says NA."""
    value = (value or '').strip()
    if not value or value.upper() == 'NA':
        return 0
    digits = re.sub(r'[^\d]', '', value)
    return int(digits) if digits else 0


def read_csv():
    with CSV_PATH.open(encoding='utf-8-sig') as handle:
        rows = list(csv.DictReader(handle))

    records = []
    for row in rows:
        name = row['School Name'].strip()
        city = row['City'].strip()
        records.append((
            name,
            CITY_FIX.get(city, city),
            parse_fee(row['IB Fees (INR/year)']),
            parse_fee(row['Normal Fees (INR/year)']),
        ))

    if not records:
        sys.exit('No rows found in %s' % CSV_PATH.name)

    duplicates = {n for n, _, _, _ in records if [r[0] for r in records].count(n) > 1}
    if duplicates:
        # Two rows with one name make the dropdown ambiguous and the exact
        # match arbitrary. Worth stopping for rather than shipping.
        sys.exit('Duplicate school names in the CSV: %s' % ', '.join(sorted(duplicates)))

    cities = sorted({c for _, c, _, _ in records})
    records.sort(key=lambda r: (r[1], r[0]))
    return cities, records


def render(cities, records):
    city_lines = ',\n'.join('    %s' % json.dumps(c, ensure_ascii=False) for c in cities)
    school_lines = '\n'.join(
        '    [%s, %d, %d, %d],' % (json.dumps(n, ensure_ascii=False), cities.index(c), ib, gen)
        for n, c, ib, gen in records
    )
    return (
        '%s\n\n'
        '  var CITIES = [\n%s\n  ];\n\n'
        '  /* [name, cityIndex, ibFee, generalFee] */\n'
        '  var SCHOOLS = [\n%s\n  ];\n\n'
        '%s'
    ) % (BEGIN, city_lines, school_lines, END)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true',
                        help='exit non-zero if school-fees.js is out of date')
    args = parser.parse_args()

    cities, records = read_csv()
    current = JS_PATH.read_text(encoding='utf-8')

    start = current.find(BEGIN)
    stop = current.find(END)
    if start == -1 or stop == -1:
        sys.exit('Markers not found in %s. Restore them before rebuilding.' % JS_PATH.name)

    updated = current[:start] + render(cities, records) + current[stop + len(END):]

    if updated == current:
        print('school-fees.js is up to date: %d schools, %d cities.'
              % (len(records), len(cities)))
        return

    if args.check:
        sys.exit('school-fees.js is out of date. Run: python3 tools/build-school-fees.py')

    JS_PATH.write_text(updated, encoding='utf-8')
    print('Wrote school-fees.js: %d schools, %d cities.' % (len(records), len(cities)))


if __name__ == '__main__':
    main()
