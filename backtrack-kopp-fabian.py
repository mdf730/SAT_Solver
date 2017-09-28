#!/usr/bin/env python2.7
import sys
import time


# Define globals
sat_num = 0
unsat_num = 0
ans_prov = 0
correct_num = 0

def flip(value):
	if value == 0:
		return 1
	elif value == 1:
		return 0
	else:
		return -1

def try_values(temp_values, clause_num, var_num, prob_num, lit_num, expected):
  	# Call variables as globals
  	global sat_num
  	global unsat_num
  	global ans_prov
 	global correct_num

  	print "Temp values: " + str(temp_values)
  	print "clause_num: " + str(clause_num)
  	print "var_num: " + str(var_num)
  	print "prob_num: " + str(prob_num)
  	print "lit_num: " + str(lit_num)
  	print "expected: " + str(expected)

  	# Initialize stack data structure to contain lists of (variable, value, flag)
  	# flag is 0 if one value has been tried, 1 when both values have been tried
  	stack = [(1, 0, 0)]

  	while len(stack) <= var_num:
		clauses = []
		clause_truth_values = []

		for i, line in enumerate(temp_values):
			#print line
			clauses.append(line)
			for j, variable in enumerate(line):
				assigned_vals = [x[0] for x in stack] 
				if abs(int(variable)) in assigned_vals:
					if int(variable) < 0:
						clauses[i][j] = flip(stack[abs(int(variable))-1][1])
					else:
						clauses[i][j] = stack[abs(int(variable))-1][1]

		# Identify unknown values as -1
		for i, line in enumerate(clauses):
			for j, variable in enumerate(line):
				print variable
				if variable != 0 and variable != 1:
					clauses[i][j] = -1

		clause_truth_values = verify(clauses, clause_truth_values)

		satisfied = 1
		failed = 0
		for value in clause_truth_values:
			if value == -1:
				satisfied = 0
			elif value == 0:
				failed = 1
				satisfied = 0

		if satisfied == 1:
			#print clauses
			print clause_truth_values
			print stack
			print "SUCCESS"
			return
		elif failed == 1:
			print "GO BACK"
			return
		else:
			stack.append((len(stack)+1,0,0))


def verify(clauses, clause_truth_values):
	print clauses
	for i, line in enumerate(clauses):
		clause_truth_values.append(0)
		for j, variable in enumerate(line):
			if variable == -1:
				clause_truth_values[i] = -1
			else:
				clause_truth_values[i] = clause_truth_values[i] | variable
	return clause_truth_values



  		


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
