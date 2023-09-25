#!/usr/bin/env python3

import collections
import pickle
import sys

class Database:
    assignments = list() # A list of assignment names
    grades = collections.defaultdict(list) # A list of grades for each student
    modified = False # Indicates unsaved modifications

    def new(self):
        self.assignments.clear()
        self.grades.clear()
        while True:
            student = input('Student name? ').strip()
            if student.lower() == 'end':
                break
            elif student in self.grades:
                print('There is already a student with the name', student)
            else:
                self.grades[student].clear()
        self.modified = True

    def edit(self, file_name):
        with open(file_name, 'rb') as file:
            self.assignments = pickle.load(file)
            self.grades = pickle.load(file)

    def update(self):
        assert self.grades, 'There are no students in the database'
        assignment = input('Assignment name? ').strip()
        if assignment in self.assignments:
            print('There is already an assignment with the name', assignment)
        else:
            self.assignments.append(assignment)
            for key in self.grades:
                self.grades[key].append(int(input('Grade for {}? '.format(key))))
            self.modified = True

    def change(self):
        choice = input('Change assignment name, student name, or grade? ').strip().lower()
        if choice.startswith('a'):
            self.change_assignment_name()
        elif choice.startswith('s'):
            self.change_student_name()
        elif choice.startswith('g'):
            self.change_grade()
        else:
            print(choice, 'is an invalid choice')
        
    def change_assignment_name(self):
        assert self.assignments, 'There are no assignments in the database'
        old_name = input('Current assignment name? ').strip()
        if old_name in self.assignments:
            index = self.assignments.index(old_name)
            new_name = input('New assignment name? ').strip()
            if new_name in self.assignments:
                print('There is already an assignment with the name', new_name)
            else:
                self.assignments[index] = new_name
                self.modified = True
        else:
            print('There is no assignment with the name', old_name)

    def change_student_name(self):
        assert self.grades, 'There are no students in the database'
        old_name = input('Current student name? ').strip()
        if old_name in self.grades:
            new_name = input('New student name? ').strip()
            if new_name in self.grades:
                print('There is already a student with the name', new_name)
            else:
                self.grades[new_name] = self.grades[old_name]
                del self.grades[old_name]
                self.modified = True
        else:
            print('There is no student with the name', old_name)

    def change_grade(self):
        assert self.assignments, 'There are no assignments in the database'
        assert self.grades, 'There are no students in the database'
        assignment = input('Assignment name? ').strip()
        if assignment in self.assignments:
            index = self.assignments.index(assignment)
            student = input('Student name? ').strip()
            if student in self.grades:
                print('Current grade:', self.grades[student][index])
                self.grades[student][index] = int(input('New grade? '))
                self.modified = True
            else:
                print('There is no student with the name', student)
        else:
            print('There is no assignment with the name', assignment)

    def save(self, file_name):
        assert self.assignments, 'There are no assignments in the database'
        assert self.grades, 'There are no students in the database'
        with open(file_name, 'wb') as file:
            pickle.dump(self.assignments, file)
            pickle.dump(self.grades, file)
        self.modified = False

    def type(self, file=sys.stdout):
        assert self.assignments, 'There are no assignments in the database'
        assert self.grades, 'There are no students in the database'
        print('Number of students', len(self.grades), file=file)
        print('Number of assignments', len(self.assignments), file=file)
        print(self.assignments, file=file)
        for key in self.grades:
            print(key, self.grades[key], file=file)

    def list(self, file_name):
        with open(file_name, 'wt') as file:
            self.type(file)

def help(command):
    pass # TODO

def read_commands(database):
    while True:
        try:
            command = input('Command? ').strip().lower() # ignore case
            if command.startswith('n'):
                database.new()
            elif command.startswith('e'):
                database.edit('lab08.pickle')
            elif command.startswith('u'):
                database.update()
            elif command.startswith('c'):
                database.change()
            elif command.startswith('s'):
                database.save('lab08.pickle')
            elif command.startswith('t'):
                database.type()
            elif command.startswith('l'):
                database.list('lab08.txt')
            elif command.startswith('h'):
                help(command.split().pop())
            elif command.startswith('q'):
                if database.modified and bool(input('Save before quitting? ')):
                    database.save('lab08.pickle')
                    print('Database saved')
                break
            else:
                print('Unrecognized command ' + command)
        except AssertionError as e:
            print(e)

def test():
    d = Database()
    read_commands(d)
    # d.new()
    # d.update()
    # d.type()
    # d.save('lab08.pickle')
    # d.list('lab08.txt')
    # d.edit('lab08.pickle')
    # d.type()
    # d.change()
    # d.type()

test()
