"""
Helplang IDLE Shell
Written by: http.llamaz
Licensed under the GNU General Public License v3.0
"""

# Imports
import subprocess
import os
from os import *
import io 
from io import *

# Build 
file = open('build.egg', 'r')
lines = file.readlines()

for index, line in enumerate(lines):
    os.system(f"touch {line.strip()}")  
file.close()

# Check if in if statement
inif = 0

# IDLE Shell
os.system('clear')
print(">---<\nHeplang IDLE Shell\n>---<\n")
cmd_list = []
while True:
    command = input()
    # Compile to code
    if command == "build();":
        linenums = len(cmd_list)
        datacount = 3
        with open("build.egg") as f:
            eggfile = f.readline().rstrip()

        file = open(eggfile, 'w')
        file.writelines('#!/usr/bin/env python3\n\ndef main():')
        for x in cmd_list:
            print(f"Compiling {linenums} lines of code to file: '{eggfile}'...")
            file.writelines('\n\n')
        file.close()
        with open(f'{eggfile}', 'r') as file:
            data = file.readlines()
            for items in cmd_list:
                data[datacount] = items+'\n'
                datacount = datacount + 1
        with open(eggfile, 'w') as file:
            file.writelines( data )
            file.writelines('\n\nmain()')

        exit()
    # Debug
    if command == "list();":
        print(cmd_list)
        input()

    ###########    
    # Lexer   #
    ##########
    
    # Variables
    if command[0:3] == "let":
        equals = command.find('=')
        variable_name = command[3:equals-1] 
        end_arg = command.find(';')
        variable_data = command[equals:end_arg]
        if inif == 0:
            cmd_list.append(f'{variable_name} {variable_data}')
        if inif == 1:
            cmd_list.append(f'  {variable_name} {variable_data}')
        #print("variable declared") # Debug
    
    # Print to console (standard)
    if command[0:8] == "printc!(":
        pr_end = command.find(');')
        str_content = command[8:pr_end]
        if inif == 0:
            cmd_list.append(f' print({str_content})')
        if inif == 1:
            cmd_list.append(f'   print({str_content})')

    # Print to console (f-string)
    if command[0:9] == "fprintc!(":
        pr_end = command.find(');')
        fstr_content = command[9:pr_end]
        if inif == 0:
            cmd_list.append(f' print(f{fstr_content})')
        if inif == 1:
            cmd_list.append(f'   print(f{fstr_content})')
    
    # Take user input
    if command[0:4] == "rl!(":
        rl_end = command.find(');')
        var_name = command[4:rl_end]
        if inif == 0:
            cmd_list.append(f' {var_name} = input()')
        if inif == 1:
            cmd_list.append(f'   {var_name} = input()')

    # If statements
    if command[0:3] == "if(":
        if_data_end = command.find(');') + 1
        if_data = command[3:if_data_end-1]
        cmd_list.append(f' if {if_data}:')
        inif = 1

    # Else if
    if command[0:5] == "elif(":
        elif_data_end = command.find(');') + 1
        elif_data = command[5:elif_data_end-1]
        cmd_list.append(f' elif {elif_data}:')
    
    # End If Statements
    if command[0:2] == "};":
        inif = 0