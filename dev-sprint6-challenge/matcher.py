import string
from time import time
from random import randrange

def isvariable(s):
	"""Function that takes a string and returns true if the 
	string passed to it begins with the underscore char and 
	false otherwise"""
	if (s[0] == "_"): return True
	else: return False

# # Test Cases:
# print "\n" 
# print isvariable('_x') # True
# print isvariable('x') # False

def dont_care(s):
	"""Takes args and checks if it is a string containing only 
	a question mark. If only question mark, returns true. otherwise
	returns false"""
	if (type(s) is str) and (s == '?'): return True
	else: return False

# # Test Cases:
# print "\n" 
# print dont_care('?') # True
# print dont_care('b') # False 

def match_element(s1, s2):
	"""Takes two args and returns true if the two string args 
	are equal or equal to ?. If one of the strings is a variable, it
	returns a dictionary with the variable as the key. Else returns 
	false"""
	if (s1 == s2) or (dont_care(s1) == True) or (dont_care(s2) == True): 
		return True
	elif (isvariable(s1) == True):
		return {s1 : s2}
	elif (isvariable(s2) == True): 
		return {s2 : s1} 
	else: return False

# print "\n" # Test Cases
# print match_element('?', '5') #should return True
# print match_element("hi", "?") #should return True
# print match_element('5', '_X') #should return {'_X': '5'}
# print match_element('_X', "hi") #should return {'_X': 'hi'}
# print match_element('5', "hi") #should return False

def searchlist(l1, l2):
	"""Recursive helper function for matchlelt. Takes in two list args. If they are equal or
	contains ?, returns true. Else returns false"""
	ct1 = len(l1)-1
	ct2 = len(l2)-1
	if l1 == [] and l2 == []:
		return True
	if dont_care(l1[ct1]):
		return True
	elif dont_care(l2[ct2]):
		return True
	elif (l1[ct1] != l2[ct2]): 
		return False
	else:
		l1 = l1[0: ct1]
		l2 = l2[0: ct2]
		return searchlist(l1, l2)

def matchlelt(l1, l2):
	"""Takes 2 args and checks if they are both lists. If either is 
	not a list, returns error message"""
	errorMessage = "Error: not a list: "
	if (type(l1) is not list):
		return errorMessage + str(l1)
	elif (type(l2) is not list):
		return errorMessage + str(l2)
	elif (searchlist(l1, l2)):
		return True
	else: return False

# print "\n" # Test Cases # REVIEW
# print matchlelt (['a', 'b', '?', 'd', 'e'], ['a', 'b', 'c', 'd', 'e'])
# print matchlelt (['a', 'b', 'f', 'd', 'e'], ['a', 'b', 'c', 'd', 'e'])    
# print matchlelt (['a', 'b', 'f', 'd', 'e'],  'e') #should return error message
# print matchlelt ('e', ['a', 'b', 'f', 'd', 'e']) #should return error message

def boundp(v, subs):
	"""Takes 2 args, a variable and a dict, checks the correct types
	and returns the value in subs that matches the variable. Else 
	returns false"""
	assert isvariable(v) == True
	assert isinstance(subs, dict)
	if v in subs.keys(): return True
	else: return False

# print "\n" # Test Cases
# print boundp('_x', {'_x':'xvalue'}) #should return True
# print boundp('_x', {'_y':'yvalue', '_x':'xvalue'}) #should return True
# print boundp('_z', {'_y':'yvalue', '_x':'xvalue'})  #should return False

def bound_to(v, subs):
	"""Takes 2 args, a vaiable and a dict, and is boundp is true,
	returns subs[v]. Else returns false"""
	if boundp(v, subs): return subs[v]
	else: return False

# print "\n" # Test Cases
# print bound_to('_x', {'_x':'xvalue'}) #should return 'xvalue'
# print bound_to('_x', {'_y':'yvalue', '_x':'xvalue'})  #should return 'xvalue'
# print bound_to('_z', {'_y':'yvalue', '_x':'xvalue'})  #should return False

def iseqvariable(s):
	"""Returns true if the string begins with S_"""
	if type(s) == str and  s.find('S_') == 0: return True
	elif type(s) == list and s[0][0] == 'S' and s[0][1] == "_": return True
	else: return False

# Test Cases
# print "\n"
# print iseqvariable("S_Z") # True
# print iseqvariable(['S_', 'hi']) # True
# print iseqvariable("hi") # True
# print iseqvariable(['hi']) # True

def match1(pat, lst, pairs):
	"""Helper function for match. Takes 3 args: 2 lists and a dict. When if finds 
	a variable in pat, it puts the variable and its corresponding element in lst
	into the pairs dict. If it find that variable again, it must have the same 
	value as is already stored in the pairs dict. Else returns false"""
	ct = 0
	if pat == [] or lst == []:
		return pairs
	elif pat[ct] == lst[ct]:
		pat = pat[1:]
		lst = lst[1:]
		return match1(pat, lst, pairs)
	elif isvariable(pat[ct]) and (pat[ct] not in pairs.keys()):
		pairs[pat[ct]] = lst[ct]
		pat = pat[1:]
		lst = lst[1:]
		return match1(pat, lst, pairs)
	elif isvariable(pat[ct]) and (pat[ct] in pairs.keys()) and (lst[ct] == pairs[pat[ct]]):
		pat = pat[1:]
		lst = lst[1:]
		return match1(pat, lst, pairs)
	elif iseqvariable(pat[0]):
		return backtrack_match(pat[ct], pat[1:], lst, [], pairs)
	else:
		return False

def match(pat, lst):
	"""Explained in match1 above"""
	res = match1(pat, lst, {})
	if res == False:
		return {}
	else:
		return res

# print "\n" # Test Cases 
# print match(['a', 'b', 'c'], ['a', 'b', 'c']) #should return {}
# print match(['a', 'b', 'c'], ['a', 'b', 'd']) #should return False
# print match(['a', '_X', 'c'], ['a', 'b', 'c']) #should return {'_X': 'b'}
# print match(['a', '_X', 'c', '_X'], ['a', 'b', 'c', 'd']) #should return False
# print match(['a', '_X', 'c', '_X'], ['a', 'b', 'c', 'b']) #should return {'_X': 'b'}
# print match(['a', '_X', 'c', '_Y'], ['a', 'b', 'c', 'd']) #should return {'_Y': 'd', '_X': 'b'}


def substitute(pat, subs):
	"""Takes in two args, pat (list) and subs (dict) and replaces any symbol in
	pat that is bound to a key in subs with the value from subs. 
	Returns a new list"""
	ct = 0
	if pat == []: 
		return []
	elif isvariable(pat[ct]) and (pat[ct] in subs.keys()): # and type(subs) == dict 
		res = substitute(pat[1:], subs)
		res.insert(0, subs[pat[ct]])
		return res
	else:
		res = substitute(pat[1:], subs)
		res.insert(0, pat[0])
		return res

# print "\n" # Test Cases
# print substitute(['a', '_X', 'c', '_Y'], {'_Y': 'd', '_X': 'b'}) #should return ['a', 'b', 'c', 'd']
# print substitute(['a', '_X', 'c', '_X'], {'_X': 'b'}) #should return ['a', 'b', 'c', 'b']


def isrule(r):
	"""Takes a rule r and checks to see if it is formatted correctly 
	with a string rule and two lists for lhs and rhs"""
	if r[0] == 'rule' and (type(r[2]) == list) and (type(r[3]) == list):
		return True
	else:
		return False

# Test Case
# print "\n"
# r1 = ['rule', 1, ['my', '_X', 'thinks', 'I', 'am', '_y'], ['do', 'you', 'think', 'you', 'are', '_y', '?']]
# r2 = ['rule', 2, ['my', '_X', 'says', 'I', 'am', '_y'], ['do', 'you', 'think', 'you', 'are', '_y', '?']]
# r3 = ['rule', 3, ['I', 'feel', '_X'], ['why', 'do', 'you', 'think', 'you', 'feel', '_X', '?']]
# r4 = ['rule', 4, '_X', '_Y']
# print isrule(r1) #should return True
# print isrule(r2) #should return True
# print isrule(r3) #should return True
# print isrule(r4) #should return False

def lhs(r):
	"""Gets the left-hand side of a rule"""
	return r[2]

def rhs(r):
	"""Gets the right-hand side of a rule"""
	return r[3]

# Test Cases
# print "\n"
# r1 = ['rule', 1, ['my', '_X', 'thinks', 'I', 'am', '_y'], ['do', 'you', 'think', 'you', 'are', '_y', '?']]
# r2 = ['rule', 2, ['my', '_X', 'says', 'I', 'am', '_y'], ['do', 'you', 'think', 'you', 'are', '_y', '?']]
# r3 = ['rule', 3, ['I', 'feel', '_X'], ['why', 'do', 'you', 'think', 'you', 'feel', '_X', '?']]
# r4 = ['rule', 4, '_X', '_Y']
# print lhs(r1) #should return ['my', '_X', 'thinks', 'I', 'am', '_y']
# print rhs(r2) #should return ['do', 'you', 'think', 'you', 'are', '_y', '?']

def apply_rule(pat, rule):
	"""Checks that the second arg is a rule and executes
	fire_rule with pat, the rhs of rule, and the correct subs
	(found using match)"""
	assert isrule(rule) == True
	return fire_rule(pat, rhs(rule), match(lhs(rule), pat))

def fire_rule(pat, rhs, subs):
	"""Checks if there are vars, if so returns the substitution.
	Otherwise returns an empty dict"""
	if subs == {}: return pat
	else: return substitute(rhs, subs)

# # Test Cases
# r1 = ['rule', 1, ['my', '_X', 'thinks', 'I', 'am', '_y'], ['do', 'you', 'think', 'you', 'are', '_y', '?']]
# r2 = ['rule', 2, ['my', '_X', 'says', 'I', 'am', '_y'], ['do', 'you', 'think', 'you', 'are', '_y', '?']]
# pattern1 = "my mother thinks I am fat"
# pattern2 = "my brother says I am crazy"
# pat = string.split(pattern1)
# response = string.join(apply_rule(pat, r1), ' ') 
# print response
# pat = string.split(pattern2)
# response = string.join(apply_rule(pat, r2), ' ') 
# print response #should return do you think you are fat ?

def backtrack_match1(sv, pat, lst, sqce, pairs):
	pairs[sv] = string.join(sqce)
	if match1(pat, lst, pairs):
		return True

def match_append(sqce, x):
	sqce.append(x)
	return sqce

def backtrack_match(sv, pat, lst, sqce, pairs):
	if not(pat):
		newstring = string.join(lst)
		pairs[sv] = newstring
		return pairs
	elif not(lst):
		return False
	elif backtrack_match1(sv, pat, lst[1:], match_append(sqce, lst[0]), pairs):
		pairs[sv] = string.join(sqce)
		return pairs
	else: 
		return backtrack_match(sv, pat, lst[1:], sqce, pairs)

# # Test cases
# print match(['my', 'S_Z', 'thinks', 'I', 'am', '_y'], ['my', 'older', 'brother', 'thinks', 'I', 'am', 'crazy'])
# # should return {'S_Z': 'older brother', '_y': 'crazy'}

def apply_rules(pat, rule_lst):
	r1 = rule_lst
	rule_found = False
	while (not(not(r1)) and not(rule_found)):
		subst = match(lhs(r1[0]), pat)
		if subst == {}:
			r1 = r1[1:]
		else:
			rule_found = True
	if rule_found == True:
		return ' '.join(substitute(rhs(r1[0]), subst))
	else: return ''

def run_eliza(inp, rule_lst):
	default_responses = ["Tell me more", "Go on", "That is ridiculous"]
	user_input = inp
	num_inputs = 0
	while user_input != "stop" and num_inputs < 10:
		num_inputs = num_inputs + 1
		user_input = string.split(user_input)
		resp = apply_rules(user_input, rule_lst)
		if resp == "":
			resp = default_responses[randrange(0,2)]
		return resp

def hi_eliza(fname):
	return "Hello, " + fname + ". This is Eliza. What do you want to talk about today?"

def stop_eliza():
	return "Your time is up. We can continue next week."

def eliza(rule_lst):
	default_responses = ["Tell me more", "Go on", "That is ridiculous"]
	fname = raw_input("Please sign in with your first name: ")
	print "Hello, " + fname + ", Eliza will be with you shortly."
	randtime = randrange(1,5)
	time1 = time()
	while time() < time1 + randtime:
		x = 1
	print "Hello, " + fname + " This is Eliza. What do you want to talk about today?"
	user_input = raw_input()
	num_inputs = 0
	while user_input != "stop" and num_inputs < 10:
		num_inputs = num_inputs + 1
		user_input = string.split(user_input)
		resp = apply_rules(user_input, rule_lst)
		if resp == "":
			resp = default_responses[randrange(0,3)]
		print resp
		user_input = raw_input()
	if user_input == "stop":
		print "I see we have touched upon a sensative topic. We can continue next week."
	else:
		print "Your time is up. We can continue next week."

def main(inp):
	r1 = ['rule', 1, ['My', '_X', 'thinks', 'I', 'am', '_Y'], ['Do', 'you', 'think', 'you', 'are', '_Y', '?']]
	r2 = ['rule', 2, ['My', '_X', 'is', 'a', '_Y'], ['What', 'do', 'you', 'mean', 'by', 'a', 'mess', '?']]
	r3 = ['rule', 3, ['Lets', 'change', 'the', '_X'], ['I', 'see', 'we', 'have', 'touched', 'on', 'a', 'touchy', '_X', '.', 'Lets', 'talk', 'about', 'another', '_X']]
	r4 = ['rule', 4, ['I', 'want', 'to', '_X', 'a', '_Y'], ['What', 'would', 'it', 'mean', 'if', 'you', 'got', 'to', '_X', 'this',  '_Y', '?']]
	r5 = ['rule', 5, ['I', 'could', 'see', 'if', 'I', 'could', '_X', '_Y'], ['Do', 'you', 'really', 'think', 'its', 'likely', 'that', 'you', 'could', '_X','_Y', '?']]
	r6 = ['rule', 6, ['I', '_X', 'to', 'start', 'to', '_Y'], ['Makes', 'sense.', 'How', 'often', 'will', 'you', '_Y', '?']]
	r7 = ['rule', 7, ['I', '_X', 'often'], ['Can', 'you', 'be', '_X', 'specific', '?']]
	r8 = ['rule', 8, ['I', 'feel', '_X'], ['Why', 'do', 'you', 'think', 'you', 'feel', '_X', '?']]
	r9 = ['rule', 9, ['I', 'want', 'to', '_X', 'this', '_Y'], ['What', 'would', 'it', 'mean', 'if', 'you', 'got', 'to', '_X', 'this',  '_Y', '?']]
	r10 = ['rule', 10, ['I', 'could', 'see', 'if', 'it', '_Y'], ['Do', 'you', 'really', 'think', 'its', 'likely', 'that', 'it', '_Y', '?']]
	r11 = ['rule', 11, ['Yes', 'I', '_X'], ['What', 'do', 'you', 'think', 'the', 'first', 'step', 'is', 'to', 'not', '_X',  '?']]
	#r12 = ['rule', 12, ['My', 'S_Z', 'thinks', 'I', 'smell', '_Y'], ['Do', 'you', 'think', 'you', 'smell', '_Y', '?']]

	rule_lst = [r1, r2, r3, r4, r5, r6, r7, r8, r9, r10, r11]
 	return run_eliza(inp, rule_lst)

# if __name__ == "__main__":
#     main()