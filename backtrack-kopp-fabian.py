#!/usr/bin/env python2.7
import sys
import time


# Define globals
sat_num = 0
unsat_num = 0
ans_prov = 0
correct_num = 0

def try_values(temp_values, clause_num, var_num, prob_num, lit_num, expected):
	pass

fs = open(sys.argv[1], 'r+') # open designated file
clause_num = 0
counter = 0
wff_num = 0
for line in fs:
  temp_line = line.split(' ')
  if counter == clause_num and counter != 0:
    try_values(temp_values, clause_num, var_num, prob_num, lit_num, expected)
    counter = 0
  if temp_line[0] == 'c':
    prob_num = temp_line[1]
    lit_num = temp_line[2]
    expected = temp_line[3]
    wff_num = wff_num + 1
  elif temp_line[0] == 'p':
    var_num = int(temp_line[2])
    clause_num = int(temp_line[3])
    counter = 0
    temp_values = []
  else:
    if counter < clause_num:
      temp_values.append(temp_line[0].split(','))
      del temp_values[counter][-1]
      counter = counter + 1
     
try_values(temp_values, clause_num, var_num, prob_num, lit_num, expected)
print sys.argv[1].strip(".cnf") + "," + "kopp-fabian" + "," + str(wff_num) + "," + str(sat_num) + "," + str(unsat_num) + "," + str(ans_prov) + "," + str(correct_num)
