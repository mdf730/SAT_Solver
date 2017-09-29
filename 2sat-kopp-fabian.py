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
  graph = {}  # will store dependence relations between 
              # variables and their negations in a graph
 
  # make graph such that given clause (x, y), there is an edge 
  # ~x -> y and ~y -> x
  for i in range(-1*int(var_num), int(var_num) + 1):
    if i != 0:
      graph[i] = ""

  for clause in temp_values:

    temp1 = graph[-1*int(clause[0])] + clause[1] + " "
    graph[-1*int(clause[0])] = temp1

    temp2 = graph[-1*int(clause[1])] + clause[0]  + " "
    graph[-1*int(clause[1])] = temp2

  for i in range(-1*int(var_num), int(var_num) + 1):
    if i != 0:
      graph[i] = graph[i].split()

  # count total number of literals
  tot_lit_num = 0
  for i in range(-1*int(var_num), int(var_num) + 1):
    if i == 0:
      continue
    tot_lit_num = tot_lit_num + len(graph[i])

  for i in [-1*int(var_num), int(var_num)]:
    i_opp = -1 * i

    marked = []            # list of nodes that have already been checked
    frontier = []          # stack of nodes to be checked 
    frontier.append(i)     # add starting value to check for


    # Perform a DFS to see if a variable V ever has a path to ~V making it unsatisfiable
    while (frontier):        
        node = frontier.pop()
        visited = False

        # check if current node has already been visited
        for it in marked:
          if node == it:
            visited = True

        # check if current node has destination node as a neighbor
        if visited == False:
          dead_end = False
          for it in graph[node]:
            dead_end = False
            if int(it) == i_opp:
              dead_end = True
              continue
          if dead_end == True:
            break                    # breaks bring graph back one variable assignment

          marked.append(node)

          for it in graph[node]:
            frontier.append(int(it)) # add neighbor nodes to stack for later search

        if len(marked) == var_num: # all variables are assigned with no contradictions
          solution = ""
          for i in range(1,var_num + 1): # calculate value based on DFS
            if i in marked:
              solution = solution + ",1"
            else:
              solution = solution + ",0"

          exec_time = time.time() - start_time
          sat_num = sat_num + 1
          if expected.strip() =="S":
            agreement = 1
            correct_num = correct_num + 1
            ans_prov = ans_prov + 1
          elif expected.strip() == "U":
            agreement = -1
            ans_prov = ans_prov + 1
          else:
            agreement = 0

          output = str(prob_num) + "," + str(var_num) + "," + str(clause_num) + ","
          output = output + max_lit_num + "," + str(tot_lit_num) + ",S," + str(agreement) 
          output = output + "," + str(round(exec_time, 6)) + solution
          print output
          return

  # if function reaches this point, then search unsuccesful
  unsat_num = unsat_num + 1
  exec_time = time.time() - start_time
  if expected.strip() =="S":
    agreement = -1
    ans_prov = ans_prov + 1
  elif expected.strip() == "U":
    ans_prov = ans_prov + 1
    correct_num = correct_num + 2
    agreement = 1
  else:
    agreement = 0

  output = str(prob_num) + "," + str(var_num) + "," + str(clause_num) + ","
  output = output + max_lit_num + "," + str(tot_lit_num) + ",U," + str(agreement)
  output = output + "," + str(round(exec_time, 6))
  print output


# main function

cnf_name = sys.argv[1]
fs = open(cnf_name, 'r+') # open designated file

csv_name = cnf_name[0:len(cnf_name)-4] + ".csv"
sys.stdout=open(csv_name,"w")    # write file to csv 

clause_num = 0
counter = 0

# read in input for each wff and store as a list of lists where each
# sublist represents a clause
wff_num = 0
for line in fs:
  temp_line = line.split(' ')
  if counter == clause_num and counter != 0:
    try_values(temp_values, clause_num, var_num, prob_num, max_lit_num, expected)
    counter = 0
  if temp_line[0] == 'c':
    prob_num = temp_line[1]
    max_lit_num = temp_line[2]
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

try_values(temp_values, clause_num, var_num, prob_num, max_lit_num, expected)
print sys.argv[1].strip(".cnf") + "," + "kopp-fabian" + "," + str(wff_num) + "," + str(sat_num) + "," + str(unsat_num) + "," + str(ans_prov) + "," + str(correct_num)

sys.stdout.close()
