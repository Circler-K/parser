import re
import queue
# \$([A-Za-z0-9	_])+[^\$+\ ] 변수판별용 정규식
# \$([A-Za-z0-9_])+[^\$\ ]
# \$([A-Za-z0-9_])+[^\$\ ]
# \$+[A-Za-z0-9_]+
# ([a-z]+)+\(+([a-z]*)+\) 쿼리 판별 정규식

#$+[A-Za-z0-9_]+
#
#[a-z0-9]+([a-z0-9,,[,],]]*)
#\$+[A-Za-z0-9_]+\x20*\=
# 메소드는 큐
# 문법오류
query_buffer=[]
query_buffer_str=""
query_buffer_list=[]
variables={}
queries=[]
#q=queue.Queue()

def parser(raw_query):
	global query_buffer,query_buffer_str,variables,queries
	for i in query_buffer:
		query_buffer_str=query_buffer_str+i
	query_buffer_list=list(query_buffer_str)
	
	if query_buffer_list.count('$')>0:
		#변수를 판별해서 변수저장한다.
		p=re.compile('\$+[A-Za-z0-9_]+')
		temp_var=p.match(query_buffer_str).group()
		print(temp_var)
	
	query_regex=re.compile('([a-z]+)\(([a-z]*)\)')
	
	print("==========")
	queries=re.findall(query_regex,query_buffer_str)
	for i in queries:
		for j in i:
			print(j)
	print("==========")
	
	
	
	
	
	print(query_buffer_str)
	print(query_buffer)
	print(query_buffer_list)


#parser(raw_query)
if __name__=="__main__":
	while(1):
		raw_query=input()
		while(raw_query.count(';')==0 and raw_query!="exit"):
			query_buffer.append(raw_query)
			raw_query=input()
			
		if(raw_query=="exit"):
			break;
		query_buffer.append(raw_query)
		parser("asdf")
		query_buffer[0:]=[]
		query_buffer_str=""
		query_buffer_list[0:]=[]