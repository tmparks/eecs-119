#!/usr/bin/env python3

def format_text(file_name):
    width = 40
    output = ''
    with open(file_name) as file:
        for line in file:
            if line.startswith('.'):
                pass # ignore commands
            else:
                for word in line.split():
                    if len(output) > 0:
                        if len(output) + len(word) < width:
                            output += ' '
                        else: # start a new line
                            print(output)
                            output = ''
                    output += word
    if len(output) > 0:
        print(output)

format_text('lab41.txt')
