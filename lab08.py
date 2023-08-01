#!/usr/bin/env python3

import collections
import pickle
import sys

class Database:
    assignments = list() # A list of assignment names
    grades = collections.defaultdict(list) # A list of grades for each student

    def new(self):
        self.assignments.clear()
        self.grades.clear()
        while True:
            student = input('Student name? ').strip()
            if student == 'END':
                break
            elif student in self.grades:
                print('There is already a student with the name', student)
            else:
                self.grades[student].clear()

    def edit(self, file_name):
        with open(file_name, 'rb') as file:
            self.assignments = pickle.load(file)
            self.grades = pickle.load(file)

    def update(self):
        assignment = input('Assignment name? ').strip()
        if assignment in self.assignments:
            print('There is already an assignment with the name', assignment)
        else:
            self.assignments.append(assignment)
            for key in self.grades:
                self.grades[key].append(int(input('Grade for {}? '.format(key))))

    def save(self, file_name):
        with open(file_name, 'wb') as file:
            pickle.dump(self.assignments, file)
            pickle.dump(self.grades, file)

    def type(self, file=sys.stdout):
        print('Number of students', len(self.grades), file=file)
        print('Number of assignments', len(self.assignments), file=file)
        print(self.assignments, file=file)
        for key in self.grades:
            print(key, self.grades[key], file=file)

    def list(self, file_name):
        with open(file_name, 'wt') as file:
            self.type(file)

def test():
    d = Database()
    # d.new()
    # d.update()
    # d.type()
    # d.save('lab08.pickle')
    # d.list('lab08.txt')
    d.edit('lab08.pickle')
    d.type()

test()
