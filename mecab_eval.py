# coding:utf-8

import sys
import os
import argparse
import time

import pandas as pd
from tabulate import tabulate
import MeCab


parser = argparse.ArgumentParser('Output formatted analysis result of MeCab')
parser.add_argument('--input_txt', '-i', default=None, help='Input text file')
parser.add_argument('--outdir', '-o', default='.', help='Output directory')
parser.add_argument('--stdout', '-s', type=bool, default=True)
parser.add_argument('--timer', '-t', type=bool, default=False)
args = parser.parse_args()

if args.input_txt:
    with open(args.input_txt, 'r') as fp:
        txt = fp.read()
    base = os.path.basename(args.input_txt)
    fname = os.path.splitext(base)[0]
else:
    sys.stdout.write('Type input text:\n')
    txt = sys.stdin.read()
    sys.stdout.write('Tyep output file name:\n')
    fname = input()

tagger = MeCab.Tagger('-Ochasen')
tagger.parse('')
start = time.time()
node = tagger.parseToNode(txt)
elapsed = time.time() - start

cols = [
    '表層形', '品詞', '品詞細分類1', '品詞細分類2', '品詞細分類3',
    '活用形', '活用型', '原形', '読み', '発音'
]
res_tb = pd.DataFrame(columns=cols)

while node:
    res = [node.surface]
    res.extend(node.feature.split(','))
    while len(res) < len(cols):
        res.append('*')
    res = pd.Series(res, index=cols)
    res_tb = res_tb.append(res, ignore_index=True)
    node = node.next

res_tb.to_csv(os.path.join(args.outdir, fname+'.csv'))

if args.stdout:
    if args.timer:
        print('elapsed time for morphological analysis: {}sec'.format(elapsed))
    with pd.option_context('display.max_rows', None,
                           'display.max_columns', 10):
        print(tabulate(res_tb, headers='keys', tablefmt='psql'))
