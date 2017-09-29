#!/usr/bin/env python2.7
import sys
import time

# Define globals
sat_num = 0
unsat_num = 0
ans_prov = 0
correct_num = 0

# Method used on a list to flip a bit value, 0<->1
def flip(value):
	if value == 0:
		return 1
	elif value == 1:
		return 0
	else:
		return -1

# Similar purpose as in brute solver
def try_values(temp_values, clause_num, var_num, prob_num, lit_num, expected):
  	#Declare Globals
  	global sat_num
  	global unsat_num
  	global ans_prov
 	global correct_num

 	start_time = time.time() 
 	agreement = 0

  	#print "Temp values: " + str(temp_values)
  	#print "clause_num: " + str(clause_num)
  	#print "var_num: " + str(var_num)
  	#print "prob_num: " + str(prob_num)
  	#print "lit_num: " + str(lit_num)
  	#print "expected: " + str(expected)

  	# Initialize stack data structure to contain lists of (variable, value, flag)
  	# flag is 0 if one value has been tried, 1 when both values have been tried
  	stack = [[1, 0, 0]]

  	# Clauses will contain a copy of the current wff variables, with the known values
  	# substituted in as a 0 or 1 and unknowns substituted as -1s.
  	clauses = []

  	# This will contain a true or false value for each clause, or -1 if still undetermined
	clause_truth_values = []

	# This contains each variable that has already been assigned
	assigned_vals = []
  	while len(stack) <= var_num:
  		#print "START OF LOOP"
  		#print "  Stack:"
  		#print "  " + str(stack)
  		del clauses[:]
  		del clause_truth_values[:]
  		del assigned_vals[:]
		clauses = []
		clause_truth_values = []
		assigned_vals = []
	 	tot_lit_num = 0

		#Identify known values
		for i, line in enumerate(temp_values):
			#print line
			#print "  Temp Value for Line before append:"
			#print "  " + str(temp_values[i])
			clauses.append(line[:])
			#print "  New Clause Line:"
			#print "  " + str(clauses[i])
			for j, variable in enumerate(line):
				tot_lit_num = tot_lit_num + 1
				assigned_vals = [x[0] for x in stack] 
				if abs(int(variable)) in assigned_vals:
					if int(variable) < 0:
						clauses[i][j] = flip(stack[abs(int(variable))-1][1])
					else:
						clauses[i][j] = stack[abs(int(variable))-1][1]

		#print "  Known variables converted:"
		#print "  " + str(clauses)
		# Identify unknown values as -1
		for i, line in enumerate(clauses):
			for j, variable in enumerate(line):
				#print variable
				if variable != 0 and variable != 1:
					clauses[i][j] = -1
		#print "  Unknown variables converted:"
		#print "  " + str(clauses)

		clause_truth_values = verify(clauses, clause_truth_values)

		satisfied = 1
		failed = 0
		for value in clause_truth_values:
			if value == -1:
				satisfied = 0
			elif value == 0:
				failed = 1
				satisfied = 0

	    # Print output to .csv
		if satisfied == 1:
			#print clauses
			#print clause_truth_values
			#print stack
			#print "SUCCESS"
			exec_time = time.time() - start_time
			if expected.strip() =="S":
				agreement = 1
				ans_prov = ans_prov + 1
				correct_num = correct_num + 1
			elif expected.strip() == "U":
				agreement = -1
				ans_prov = ans_prov + 1
			else:
				agreement = 0
			output = str(prob_num) + "," + str(var_num) + "," + str(clause_num) + "," + str(lit_num) + "," + str(tot_lit_num)
			output = output +  "," + "S" + "," + str(agreement) + "," + str(round(exec_time,2))
			for i in range(var_num):
				if i < len(stack):
					output = output + "," + str(stack[i][1])
				else:
					output = output + ",?"
			print output
			sat_num = sat_num + 1
			return

		# backtrack is recursive, flipping bits and popping variables
		elif failed == 1:
			#print "GO BACK"
			if stack[len(stack)-1][2] == 0:
				stack[len(stack)-1][2] = 1
				stack[len(stack)-1][1] = flip(stack[len(stack)-1][1])
			else:
				stack = backtrack(stack)
				if stack == -1:
					exec_time = time.time() - start_time
					if expected.strip() =="S":
						agreement = -1
						ans_prov = ans_prov + 1
					elif expected.strip() == "U":
						agreement = 1
						ans_prov = ans_prov + 1
						correct_num = correct_num + 1
					else:
						agreement = 0
					output = str(prob_num) + "," + str(var_num) + "," + str(clause_num) + "," + str(lit_num) + "," + str(tot_lit_num)
					output = output +  "," + "U" + "," + str(agreement) + "," + str(round(exec_time,2))
					print output
					unsat_num = unsat_num + 1
					return
		# append the next value to the stack
		else:
			stack.append([len(stack)+1,0,0])
		#print "END OF LOOP\n"

# This pops a value from the stack. If the stack length is zero, the wff is unsatisfiable
# If the variable hasn't had both values tried, flip the value and try again
# otherwise, recursive call the function until a variable is found to flip or the stack is empty
def backtrack(stack):
	stack.pop()
	if len(stack) == 0:
		#print "UNSATISFIABLE"
		return -1
	else:
		if stack[len(stack)-1][2] == 0:
			stack[len(stack)-1][2] = 1
			stack[len(stack)-1][1] = flip(stack[len(stack)-1][1])
		else:
			stack = backtrack(stack)

	return stack

# This fills the truth values based on the contents of clauses.
def verify(clauses, clause_truth_values):
	#print clauses
	for i, line in enumerate(clauses):
		clause_truth_values.append(0)
		for j, variable in enumerate(line):
			if variable == -1:
				clause_truth_values[i] = -1
			else:
				clause_truth_values[i] = clause_truth_values[i] | variable
	#print "  Clause values computed:"
	#print "  " + str(clause_truth_values)
	return clause_truth_values


# The code below is very similar to the brute program

#MAIN 
cnf_name = sys.argv[1]
fs = open(cnf_name, 'r+') # open designated file

oldstdout = sys.stdout
csv_name = cnf_name[0:len(cnf_name)-4] + "2.csv"
sys.stdout=open(csv_name,"w")

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
    sys.stdout.close()
    sys.stdout = oldstdout
    print prob_num
    sys.stdout=open(csv_name,"a")
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

sys.stdout.close()
