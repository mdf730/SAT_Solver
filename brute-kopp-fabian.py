#!/usr/bin/env python2.7
import sys
import time

# Define globals
sat_num = 0
unsat_num = 0
ans_prov = 0
correct_num = 0

def try_values(temp_values, clause_num, var_num, prob_num, max_lit_num, expected):
  global sat_num
  global unsat_num
  global ans_prov
  global correct_num
  start_time = time.time() 
  for i in range(2**var_num):
    binary = "0" + str(var_num) + "b"
    assignment = format(i,binary)
    #print assignment
    satisfiable = []
    counter = 0
    tot_lit_num = 0
    for line in temp_values:
       satisfiable.append(False)
       for value in line:
          tot_lit_num = tot_lit_num + 1
          #print str(bool(int(assignment[abs(int(value))-1]))) + str(value)
          #print assignment[abs(int(value))-1]
          if int(value) < 0:
            satisfiable[counter] = satisfiable[counter] | (not bool(int(assignment[abs(int(value)) - 1]))) 
      	    #print value + " " + str(not int(assignment[abs(int(value)) - 1])) + " " + assignment[3]
          else:
            satisfiable[counter] = satisfiable[counter] | bool(int(assignment[abs(int(value)) - 1]))
       counter = counter + 1
    end_satisfy = True
    for line in satisfiable:
       end_satisfy = end_satisfy & line
    if  end_satisfy == True:
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
       output = str(prob_num) + "," + str(var_num) + "," + str(clause_num) + "," + str(max_lit_num) + "," 
       output = output + str(tot_lit_num) + "," + "S" + "," + str(agreement) + "," 
       output = output + str(round(exec_time,2))
       for i in range(var_num):
         output = output + "," + assignment[i]
       print output
       sat_num = sat_num + 1
       return

  if expected.strip() =="S":
    agreement = -1
    ans_prov = ans_prov + 1
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

cnf_name = sys.argv[1]
fs = open(cnf_name, 'r+') # open designated file

csv_name = cnf_name[0:len(cnf_name)-4] + ".csv"
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
