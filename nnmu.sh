#!/bin/bash
#
#

python nnmu_detection.py 300 200 150
python evaluation.py 10 20 50 100 > ../data/exp1/result_evaluation.txt
