#!/usr/bin/env python2.7
import sys
import time

def try_values(temp_values, clause_num, var_num):
  
  # make graph between all edges containg certain character and negation 
  # of character 
  graph = {}
 
  # make graph 
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

#  for i in range(-1*int(var_num), int(var_num) + 1):
#    if i == 0:
#      continue
#    print str(i) + " -->", 
#    print graph[i]

  for i in range(-1*int(var_num), int(var_num) + 1):
    if i == 0: 
      continue
    i_opp = -1 * i
    marked = []            # list of nodes that have already been checked
    frontier = []          # stack of nodes to be checked 
    frontier.append(i)     # add starting value to check for
  
    while (frontier):
      node = frontier.pop()
      visited = False

      # check if current node has already been visited
      for it in marked:
        if node == it:
          visited = True
      # check if current node has destination node as a neighbor
      if visited == False:
        for it in graph[node]:
          if int(it) == i_opp:
            print "U"
            return
        marked.append(node)
        for it in graph[node]:
          frontier.append(int(it))
  print "S"

fs = open(sys.argv[1], 'r+') # open designated file

clause_num = 0
counter = 0
for line in fs:
  temp_line = line.split(' ')
  if counter == clause_num and counter != 0:
    try_values(temp_values, clause_num, var_num)
    counter = 0
  if temp_line[0] == 'c':
    continue    

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

try_values(temp_values, clause_num, var_num)