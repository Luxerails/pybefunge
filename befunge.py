# befunge.py by Luxerails - Befunge Interpreter
# Usage: befunge.py befunge-code.txt
# 55+"!yojnE",,,,,,,@

from random import random as rand
import sys

def interpret(map):
	# Split the map
	if '\r\n' in map: map = map.split('\r\n')
	elif '\r' in map and '\n' not in map: map = map.split('\r')
	else: map = map.split('\n')
	
	# Adjust lines length with spaces if needed
	m = max(len(_) for _ in map)
	map = [line + (' ' * (m - len(line))) for line in map]
	
	map = [list(z) for z in map]	
	width  = len(map[0])
	height = len(map)
	stack = []
	direction = 'R'
	ip = [0, 0]
	stdin = []
	string_mode = 0
	
	# Infinite loop until the program reach a @
	while True:
		ipx, ipy = ip
		inst = map[ipy][ipx]
		
		# Push current character on the stack if string mode toggled
		if string_mode and inst != '"':
			stack.append(ord(inst))
		
		# Push a digit on the stack
		if inst in '0123456789':
			stack.append(int(inst))
		
		# Add two top-stack values
		elif inst == '+':
			if len(stack) < 2:
				print "Stack Error on (%s, %s)" % (ipx, ipy)
				return False
			a = stack.pop()
			b = stack.pop()
			stack.append((a + b) % 256)
		
		# Subtract two top-stack values
		elif inst == '-':
			if len(stack) < 2:
				print "Stack Error on (%s, %s)" % (ipx, ipy)
				return False
			a = stack.pop()
			b = stack.pop()
			stack.append((b - a) % 256)
		
		# Multiply two top-stack values
		elif inst == '*':
			if len(stack) < 2:
				print "Stack Error on (%s, %s)" % (ipx, ipy)
				return False
			a = stack.pop()
			b = stack.pop()
			stack.append((a * b) % 256)
		
		# Divide two top-stack values
		elif inst == '/':
			if len(stack) < 2:
				print "Stack Error on (%s, %s)" % (ipx, ipy)
				return False
			a = stack.pop()
			b = stack.pop()
			stack.append((b / a) % 256)
		
		# Modulo two top-stack values
		elif inst == '%':
			if len(stack) < 2:
				print "Stack Error on (%s, %s)" % (ipx, ipy)
				return False
			a = stack.pop()
			b = stack.pop()
			stack.append((b % a) % 256)
		
		# Logical not the top-stack value
		elif inst == '!':
			if len(stack) < 1:
				print "Stack Error on (%s, %s)" % (ipx, ipy)
				return False
			a = stack.pop()
			if a == 0: stack.append(1)
			else: stack.append(0)
		
		# Comparison between two top-stack values
		elif inst == '`':
			if len(stack) < 2:
				print "Stack Error on (%s, %s)" % (ipx, ipy)
				return False
			a = stack.pop()
			b = stack.pop()
			if b > a: stack.append(1)
			else: stack.append(0)
		
		# Direction change
		elif inst == '>':
			direction = 'R'
		
		elif inst == '<':
			direction = 'L'
		
		elif inst == '^':
			direction = 'U'
		
		elif inst == 'v':
			direction = 'D'
		
		# Random direction
		elif inst == '?':
			a = (int(rand() * 100) % 4)
			direction = 'RLUD'[a]
		
		# Change direction according to the top-stack value, vertically or horizontally
		elif inst == '_':
			if len(stack) < 1:
				print "Stack Error on (%s, %s)" % (ipx, ipy)
				return False
			a = stack.pop()
			if a == 0: direction = 'R'
			else: direction = 'L'
		
		elif inst == '|':
			if len(stack) < 1:
				print "Stack Error on (%s, %s)" % (ipx, ipy)
				return False
			a = stack.pop()
			if a == 0: direction = 'D'
			else: direction = 'U'
		
		# Toggle string mode
		elif inst == '"':
			string_mode ^= 1
		
		# Duplicate top-stack value
		elif inst == ':':
			if len(stack) < 1:
				print "Stack Error on (%s, %s)" % (ipx, ipy)
				return False
			stack.append(stack[-1])
		
		# Invert the two top-stack values
		elif inst == '\\':
			if len(stack) < 2:
				print "Stack Error on (%s, %s)" % (ipx, ipy)
				return False
			a = stack.pop()
			b = stack.pop()
			stack.append(b)
			stack.append(a)
		
		# Pop a value from the stack
		elif inst == '$':
			if len(stack) < 1:
				print "Stack Error on (%s, %s)" % (ipx, ipy)
				return False
			stack.pop()
		
		# Output the top-stack value as a number
		elif inst == '.':
			if len(stack) < 1:
				print "Stack Error on (%s, %s)" % (ipx, ipy)
				return False
			a = stack.pop()
			sys.stdout.write(str(a) + ' ')
			sys.stdout.flush()
		
		# Output the top-stack value as a byte
		elif inst == ',':
			if len(stack) < 1:
				print "Stack Error on (%s, %s)" % (ipx, ipy)
				return False
			a = stack.pop()
			sys.stdout.write(chr(a))
			sys.stdout.flush()
		
		# Jump over the next cell
		elif inst == '#':
			if direction == 'L': ipx -= 1
			if direction == 'D': ipy += 1
			if direction == 'R': ipx += 1
			if direction == 'U': ipx -= 1
		
		# Place a byte on the map
		elif inst == 'p':
			if len(stack) < 3:
				print "Stack Error on (%s, %s)" % (ipx, ipy)
				return False
			y = stack.pop()
			x = stack.pop()
			v = stack.pop()
			if x >= width or y >= height:
				print "Out of bounds (%s, %s) on (%s, %s)" % (x, y, ipx, ipy)
				return False
			map[y][x] = chr(v)
		
		# Get a byte from the map
		elif inst == 'g':
			if len(stack) < 2:
				print "Stack Error on (%s, %s)" % (ipx, ipy)
				return False
			y = stack.pop()
			x = stack.pop()
			if x >= width or y >= height:
				print "Out of bounds (%s, %s) on (%s, %s)" % (x, y, ipx, ipy)
				return False
			stack.append(ord(map[y][x]))
		
		# Input a number
		elif inst == '&':
			a = input()
			if a > 0xff:
				print "Input number not in range (0 - 256) on (%s, %s)" % (ipx, ipy)
				return False
			stack.append(a)
		
		# Input a byte
		elif inst == '~':
			if stdin == []:
				stdin = list(raw_input())
			c = stdin.pop()
			stack.append(ord(c))
		
		# End of program
		elif inst == '@':
			break
		
		# Other characters are considered as NOPs
		else:
			pass
		
		# Move IP
		if direction == 'R':
			ip = [(ipx + 1) % width, ipy]
			
		elif direction == 'U':
			ip = [ipx, (ipy - 1) % height]
			
		elif direction == 'D':
			ip = [ipx, (ipy + 1) % height]
			
		elif direction == 'L':
			ip = [(ipx - 1) % width, ipy]
	
	return True


if __name__ == '__main__':
	if len(sys.argv) < 2:
		print "Usage: befunge.py <file>"
		sys.exit()
	
	try: map = open(sys.argv[1], 'rb').read()
	except:
		print "Couldn't open file %s :(" % sys.argv[1]
		sys.exit()
	
	interpret(map)
	
	sys.exit()

