#!/usr/bin/env python2.7
import sys
import time

# Define globals
sat_num = 0
unsat_num = 0
ans_prov = 0
correct_num = 0

# Define functions

# Try_values completes the bulk of the processing for each wff
def try_values(temp_values, clause_num, var_num, prob_num, max_lit_num, expected):
  # Declare globals
  global sat_num
  global unsat_num
  global ans_prov
  global correct_num

  start_time = time.time() 

  # iterate over every possible permutation of variables
  for i in range(2**var_num):            # generate binary number to
    binary = "0" + str(var_num) + "b"    # represent every possible
    assignment = format(i,binary)        # variable - value string
  
    satisfiable = []                     # holds each clauses truth value
 
    counter = 0
    tot_lit_num = 0

    # iterate through the wff: first the clause and then each literal in the clause
    for line in temp_values:
       satisfiable.append(False)         #False is initial value because True|[False] = True, False|[False] = False
       for value in line:                
          tot_lit_num = tot_lit_num + 1
        
          # if the variable is negated, use the opposite of the variable's value
          if int(value) < 0:
            # Once a True is found, it will be stored in satisfiable[counter] because of the 'OR'ing
            satisfiable[counter] = satisfiable[counter] | (not bool(int(assignment[abs(int(value)) - 1]))) 
          # otherwise use the value
          else:
            satisfiable[counter] = satisfiable[counter] | bool(int(assignment[abs(int(value)) - 1]))

       counter = counter + 1

    end_satisfy = True
    for line in satisfiable:
       end_satisfy = end_satisfy & line      # and together truth values of all clauses to see if all clauses are true

    if  end_satisfy == True:                 # every clause was satisfied, so wff satisfiable
       exec_time = time.time() - start_time  # end execution timer
       
       # Take care of output formatting
       if expected.strip() =="S":
         agreement = 1
         ans_prov = ans_prov + 1
         correct_num = correct_num + 1
       elif expected.strip() == "U":
         agreement = -1
         ans_prov = ans_prov + 1
       else:
         agreement = 0

       # Output csv line to csv
       output = str(prob_num) + "," + str(var_num) + "," + str(clause_num) + "," + str(max_lit_num) + "," 
       output = output + str(tot_lit_num) + "," + "S" + "," + str(agreement) + "," 
       output = output + str(round(exec_time,2))
       for i in range(var_num):
         output = output + "," + assignment[i] # outputs each variable's value when satisfied
       print output
       sat_num = sat_num + 1
       return

  # Output for an unsatisfiable wff
  if expected.strip() =="S":       # program will only reach this 
    agreement = -1                 # point if every combination of
    ans_prov = ans_prov + 1        # values (2^n) was unsatisfiable
  elif expected.strip() == "U":
    agreement = 1
    ans_prov = ans_prov + 1
    correct_num = correct_num + 1
  else:
    agreement = 0

  exec_time = time.time() - start_time

  output =  str(prob_num) + "," + str(var_num) + "," + str(clause_num) + "," + str(max_lit_num) + "," + str(tot_lit_num)
  output = output +  "," + "U" + "," + str(agreement) + "," + str(round(exec_time,2))
  unsat_num = unsat_num + 1
  print output



# Main program

cnf_name = sys.argv[1]
fs = open(cnf_name, 'r+') # open designated file

csv_name = cnf_name[0:len(cnf_name)-4] + "_brute.csv"
sys.stdout=open(csv_name,"w")    # write file to csv      

clause_num = 0
counter = 0
wff_num = 0

for line in fs:  # read in file line by line and construct list of clause which is itself a list of variables

  temp_line = line.split(' ')
  # If all clauses have been parsed from input, call the computing function
  if counter == clause_num and counter != 0:
    try_values(temp_values, clause_num, var_num, prob_num, lit_num, expected)
    counter = 0
  # If a comment line, grab values for csv output
  if temp_line[0] == 'c':
    prob_num = temp_line[1]
    lit_num = temp_line[2]
    expected = temp_line[3]
    wff_num = wff_num + 1
  # If a problem line, grab values, initialize counter
  elif temp_line[0] == 'p':
    var_num = int(temp_line[2])
    clause_num = int(temp_line[3])
    counter = 0
    temp_values = []
  else:
    ## append current clause to list of clauses for the wff
    if counter < clause_num:
      temp_values.append(temp_line[0].split(','))
      del temp_values[counter][-1]
      counter = counter + 1
# Function needs to be called for the final wff
try_values(temp_values, clause_num, var_num, prob_num, lit_num, expected)

# Print the end of csv
print sys.argv[1].strip(".cnf") + "," + "kopp-fabian" + "," + str(wff_num) + "," + str(sat_num) + "," + str(unsat_num) + "," + str(ans_prov) + "," + str(correct_num)

sys.stdout.close()  # Close the csv file
