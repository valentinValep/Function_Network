# Desc: This script will read a file and print a function network
# Auth: Valentin Lepiller
# Date: 10/05/2023
# Note: This script is not yet functional

import sys
import random
import os
import re
from pyvis.network import Network

class File:
	def __init__(self, name) -> None:
		self.name = name
		self.color = random_color()

	def __str__(self) -> str:
		return self.name

	def __repr__(self) -> str:
		return self.name

class Function:
	def __init__(self, declaration, file) -> None:
		self.name = get_name_from_declaration(declaration)
		self.file = file
		self.definition = ""
		self.children = []

	def add_child(self, child):
		self.children.append(child)

	def add_definition_line(self, line):
		self.definition += line

	def __str__(self) -> str:
		return self.name

	def __repr__(self) -> str:
		return self.name + " " + str(self.children)

	def __eq__(self, __value: object) -> bool:
		if (type(__value) == str):
			return self.name == __value
		if (type(__value) == Function):
			return self.name == __value.name

def get_name_from_declaration(declaration):
	declaration = declaration.split()
	for word in declaration:
		if ("(" in word):
			word = word.split("(")[0]
			while word[0] == '*':
				word = word[1:]
			return word
	return "UNDEFINED_FUNCTION_NAME"

def random_color():
	return f"#{random.randint(50, 255):x}{random.randint(50, 255):x}{random.randint(50, 255):x}"

def open_files():
	files_already_read = []
	files_lines = []

	for i in range(1, len(sys.argv)):
		if os.path.isdir(sys.argv[i]):
			dir = sys.argv[i]
			files = os.listdir(dir)
			for file in files:
				if dir + file in files_already_read:
					continue
				files_already_read.append(dir + file)
				file = open(dir + file, 'r')
				lines = file.readlines()
				file.close()
				files_lines.append((lines, File(file.name)))
		else:
			if sys.argv[i] in files_already_read:
				continue
			files_already_read.append(sys.argv[i])
			file = open(sys.argv[i], 'r')
			lines = file.readlines()
			file.close()
			files_lines.append((lines, File(sys.argv[i])))
	return files_lines

def create_functions(files_lines):
	functions = []

	current_function_ind = 0
	for lines, file in files_lines:
		in_function = False
		for i in range(len(lines)):
			line = lines[i]
			if line[0] == '{':
				in_function = True
				if lines[i - 1][0] == '\t':
					functions.append(Function(lines[i - 2], file))
				else:
					functions.append(Function(lines[i - 1], file))
				continue
			if line[0] == '}':
				in_function = False
				current_function_ind += 1
				continue
			if in_function:
				functions[current_function_ind].add_definition_line(line)
				continue
	return functions

def fill_functions_children(functions):
	for function in functions:
		for function2 in functions:
			if function.name in re.split(r'\W+', function2.definition):
				function2.add_child(function)

def print_functions(functions):
	for function in functions:
		print(function, function.file)
		for child in function.children:
			print("\t" + str(child))

def create_and_show_network(functions):
	net = Network(width="100%", bgcolor="#222222", font_color="white", directed =True)

	for function in functions:
		net.add_node(function.name, label=function.name, color=function.file.color, title=function.file.name)

	for function in functions:
		for child in function.children:
			net.add_edge(function.name, child.name)

	net.show("/tmp/func_tree.html", notebook=False)


def main():
	if len(sys.argv) == 1:
		print("Usage: python3 func_tree.py <files>")
		exit(1)

	files_lines = open_files()

	functions = create_functions(files_lines)
	fill_functions_children(functions)

	print_functions(functions)
	create_and_show_network(functions)

if __name__ == "__main__":
	main()
