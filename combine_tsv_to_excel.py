#!/usr/bin/env python

import csv
import glob
import os

import xlwt

wb = xlwt.Workbook()
for filename in glob.glob("extract_summaries.dir/*.tsv"):
    (f_path, f_name) = os.path.split(filename)
    (f_short_name, f_extension) = os.path.splitext(f_name)
    if len(f_short_name) > 30:
        f_short_name = f_short_name[-30:]
    ws = wb.add_sheet(f_short_name)
    spamReader = csv.reader(open(filename, 'rb'), delimiter='\t')
    for rowx, row in enumerate(spamReader):
        for colx, value in enumerate(row):
            ws.write(rowx, colx, value)

wb.save("extract_summaries.dir/master.rpkm.xls")
