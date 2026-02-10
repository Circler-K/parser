import re
import queue
import os
import sys

#  변수,함수, 자료형

# 함수 함수 여러개 


# \$([A-Za-z0-9	_])+[^\$+\ ] 변수판별용 정규식
# \$([A-Za-z0-9_])+[^\$\ ]
# \$([A-Za-z0-9_])+[^\$\ ]
# \$+[A-Za-z0-9_]+
# ([a-z]+)+\(+([a-z]*)+\) 쿼리 판별 정규식
#query_regex=re.compile('([a-z]+)+\(+([a-z]*)+\)')
#query_regex=re.compile('([a-z0-9]+)\(([a-z0-9]*)\)')
#query_regex=re.compile('([a-z0-9]+)\(([a-z0-9\,\[\]])*\)')
# 메소드는 큐
# 문법오류
# 대입연산 -> 우선선위큐, 연산자별로 우선순위큐, 형태 어긋나면 에러, 
# 콤마
variables={}
queries=[]


 
def func_parse(parsed_func):
	parsed_func= re.findall('[a-zA-Z]*\(',parsed_func)
	print(parsed_func)


def GetItemList(q):
	ret=[]
	n=q.qsize()
	while n > 0:
		ret.append(q.get())
		n -= 1
	return ret

def infix_to_postfix(infix_str):
	pos=0
	
		

def postfix_to_infix(postfix_str):
	dds

def parser(input_buffer):
	global variables,queries
	
	Q=queue.PriorityQueue()
	Stack_Operand=[]
	Stack_Operator=[]


	input_str = ""
	for i in input_buffer:
		input_str += i

	# query_buffer_list=list(query_buffer_str)
	
	# if query_buffer_list.count('$')>0:
	# 	#변수를 판별해서 변수저장한다.
	# 	if re.search('\$+[A-Za-z0-9_]+\x20*\=',query_buffer_str):
	# 		p=re.compile('\$+[A-Za-z0-9_]+')
	# 		temp_var=p.match(query_buffer_str).group()
	# 		Q.put((2,temp_var))
	# 		Stack_Operand.append(temp_var)
	# 		Stack_Operator.append('=')
	# 		print(temp_var)
		
	
	
	query_regex=re.compile('([A-Za-z0-9]+)\((.*)\)')
	queries=re.findall(query_regex,input_str)

	print("==========")
	print(queries)
	for i in queries:
		#print(j)
		func_name=func_find_name(i[0])
		func_arg=func_find_param(i[1])
		Q.put((func_name,func_arg))
		Stack_Operand.append(func_name)
		Stack_Operand.append(func_arg)
		
		
		
		print(func_arg)
		
		for k in range(0,len(func_arg)):
			print(func_arg[k])
		
		
		#if re.search('\[([a-z0-9\,]*)\]',j):
		#	func_arg=re.findall('\[([a-z0-9\,]*)\]',j)
		#	for k in range(0,len(func_arg)):
		#		func_arg[k]=func_arg[k].split(',')
		#	print(func_arg)
		#	func_arg[k]=func_arg[k].split(',')		
			
	print("==========")
	
	print(Stack_Operand)
	print(Stack_Operator)
	print(GetItemList(Q))
	print(queries)
	print(input_str)
	'''
	query=raw_query
	raw_query=list(raw_query)
	if raw_query.count(';')!=0:
		# ; 있으면
		print("hi")
		print(query)
		print(query_buffer)
	else:
		# ; 없으면
		print("exec")
		print(query)
		query_buffer.append(query)
	print(raw_query)
	'''


def func_find_name(str):
	if(str[0].isdigit()):
		print("Systex Error")
		os.system("pause")
		sys.exit()
	return str

def func_find_param(str):

	regex="\".*\"|\$[A-Z][a-zA-Z0-9]*|[1-9][0-9]*|\[.*\]"
	#regex = regex + "\," + regex + "*"
	# return re.findall('[a-z0-9]+|\[[a-z0-9\,]*\]',str)
	return re.findall('[a-z0-9]+|\[[a-z0-9\,]*\]',str)
	


#parser(raw_query)
if __name__=="__main__":
	while(1):
		query_buffer = []

		raw_query=input()
		while(raw_query.count(';')==0 and raw_query!="exit;"):
			query_buffer.append(raw_query)
			raw_query=input()
			
		if(raw_query=="exit;"):
			break;
		query_buffer.append(raw_query)
		parser(query_buffer)












		'''
		re=[]
		re[\,re]


		'''