import re

FUNC = 0
VAR = 1
OPER = 2
STRING = 3
NUM = 4
SPACE = 5

S_operation = []
S_operand = []
operation_list = {
	'^':1,
	'|':1,
	'!':1,
	'/':2,
	'%':2,
	'*':2,
	'&':2,
	'+':3,
	'-':3, 
	'<':4,
	'==':4,
	'>':4,
	'<=':4,
	'>=':4,
	'&&':5,
	'||':5,
	'=':6,
}


def oper_stack(oper):
	temp_list=[]
	if oper=='=':
		if S_operand[-1][0]==VAR:
			pass
		else:
			exit(1)
			return False
	# 기존에 있던게 우선순위가 높을때 ex) 스택 *>+
	if len(S_operation)>0 and operation_list[S_operation[-1]] < operation_list[oper]:
		temp_list.extend([OPER,S_operation[-1]])
		S_operation.pop()
		second_operand=S_operand.pop()
		first_operand=S_operand.pop()
		print(first_operand)
		print(second_operand)
		temp_list.extend([first_operand,second_operand])
		S_operand.append(temp_list)
		print(temp_list)
	elif len(S_operation)>0 and operation_list[S_operation[-1]] > operation_list[oper]:
		return
	else:
		return



def parse(txt):
	operand_flag = False
	operation_flag = False
	#  딕셔너리에 넣고 아래 각각의 항을 파싱하는 것마다  플래그 키고  
	i = 0
	result = []
	while i < len(txt):
		if txt[i].isalpha() == True:
			if operand_flag:
				return False
			operand_flag = True
			operation_flag = False
			num, result = func_parse(txt[i:])
			S_operand.append(result)
			if(num == -1):
				return False
			i += num
			# push rssult oper stack
		elif txt[i] == '$':
			if operand_flag:
				return False
			operand_flag = True
			operation_flag = False
			num, result = var_parse(txt[i:])
			S_operand.append(result)
			if num == -1:
				return False
			i += num
			#stack
		elif txt[i] == '\'' or txt[i]=='\"':
			if operand_flag:
				return False
			operand_flag = True
			operation_flag = False
			num, result = str_parse(txt[i:])
			S_operand.append(result)
			if num == -1:
				return False
			i += num
		elif txt[i].isdigit() == True:
			if operand_flag:
				return False
			operand_flag = True
			operation_flag = False
			num, result = num_parser(txt[i:])
			S_operand.append(result)
			if num == -1:
				return False
			i += num

		elif txt[i] in operation_list.keys():
			if operation_flag:
				return False
			operation_flag = True
			num ,result = operation_parse(txt[i:])
			
			oper_stack(result[1]) # 연산자 우선순위 판별

			S_operation.append(result[1])
			operand_flag = False
			i += num
		else:
			i += 1
	return result


def func_parse(txt):
	result = []
	num = func_parse_shape(txt, result)
	
	if num == -1:
		return -1, None

	for pair in result:
		# func name check valible
		if re.findall('[a-zA-Z][a-zA-Z0-9]*', pair[1])[0] != pair[1] : #TODO exist name
			return -1, None
	# func param check
		pair[2]=pair[2].split(',')
		for i in range(len(pair[2])):
			pair[2][i] = parse(pair[2][i])

	return num, result

	
def func_parse_shape(txt, result):
	if txt[0].isalpha() == False:
		# print("함수의 첫 글자는 알파벳 이여야합니다.")
		print("first char must alpa")
		return -1
	cnt = -1
	start = 0
	end = 1
	
	while cnt != 0 and end < len(txt):
		if(txt[end] == '('):
			if cnt == -1 :
				cnt = 1
				cache = txt[start : end]
				start = end + 1
			else :
				cnt += 1
		elif(txt[end] == ")"):
			cnt -= 1
		end += 1

	if(cnt == -1):
		print("() 가 없습니다.")
		return -1

	num = 0
	result.append([FUNC,cache, txt[start:end-1]])
	if end < len(txt) and txt[end] == '.':
		end += 1
		num = func_parse_shape(txt[end:], result)

		if  num == -1:
			return -1
	return num + end

		
def var_parse(txt):
	if(not(txt[0] == '$' and (txt[1].isalpha() or txt[1]=='_' ))):
		return -1, None
	i = 2
	for i in range(2, len(txt)):
		t = txt[i]
		if(not(t.isalpha() or t.isdigit() or t=='_')):
			break
	return i+1, (VAR, txt[:i])

def space_parse(txt):
	# 고려해야하는 점 문자열,  return
	pass

def operation_parse(txt):
	i = 1
	print(txt)
	if (len(txt)<2 and len(txt)>1) and txt[1] in operation_list.keys():
		i+=1

	return i,(OPER,txt[:i])


def num_parser(txt):
	# 숫자플래그, 문자열 동일
	# if txt[0]=='-' and not(txt[1].isdigit()):
	# 	return -1, None
	# elif not(txt[0].isdigit()):
	# 	return -1, None

	if not(txt[0].isdigit()):
		return -1, None
	i = 1

	dot_flag = False

	for i in range(1,len(txt)):
		t = txt[i]
		
		if t=='.' and txt[i+1].isdigit():
			if dot_flag:
				return -1, None

			else:
				dot_flag = True
				continue

		if t.isdigit() is False:
			return i,(NUM,txt[:i])

	return i+1,(NUM,txt)

def str_parse(txt):
	# print(txt)
	s_qoute_flag = False
	d_qoute_flag = False
	if txt[0] == '\'':
		s_qoute_flag = True
	elif txt[0] == '\"':
		d_qoute_flag = True
	else:
		return -1

	ch = False
	for i in range(1,len(txt)):
		if s_qoute_flag==True and txt[i]=='\'':
			ch = True
			break;
		elif d_qoute_flag == True and txt[i]=='\"':
			ch = True
			break;


	if ch is False:
		return -1,None
	# print(i, (STRING,txt[1:i-1]))
	return i+1, (STRING,txt[1:i])


def param_parse(txt):
	pass

while True:
	S_operand=[]
	S_operation=[]
	all_input = input()
	if all_input =="exit":
		exit(0)
	print(parse(all_input))
	print("====================")
	print(S_operand)
	print(S_operation)
	print("====================")
	print("",end='\n\n\n\n\n\n\n\n')
'''
$a_dd = asdf(asdf()).fdsfs().fsasdf();      
\$\_*[a-zA-Z]*\_*[a-zA-Z]*  // 변수

a = s + 90 + 3 - 5 * 3

[a-zA-Z]*\(
'''