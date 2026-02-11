import re
import json  # AST를 예쁘게 출력하기 위해 추가

# 1. 토크나이저: 문자열을 의미 있는 최소 단위(Token)로 쪼갭니다.
def tokenize(query_str):
    print(f"\n[1. Tokenizing] 입력 문자열: \"{query_str}\"")
    token_pattern = r"([a-zA-Z_][a-zA-Z0-9_]*|[0-9]+|[(),=]|\$)"
    tokens = re.findall(token_pattern, query_str)
    print(f"   => 추출된 토큰: {tokens}")
    return tokens

# 2. 쿼리 객체
class Query:
    def __init__(self, raw_query):
        self.raw_query = raw_query
        self.tokens = tokenize(raw_query)
        self.ast = None
        self.is_valid = False
        self.cursor = 0
        
        print("\n[2. Parsing] 구문 분석 시작...")
        self._parse() 

    def _parse(self):
        if not self.tokens:
            return

        try:
            self.ast = self._parse_expression()
            self.is_valid = True
            # AST를 JSON 형식으로 예쁘게 출력
            print(f"   => [AST 생성 완료]:\n{json.dumps(self.ast, indent=4, ensure_ascii=False)}")
        except Exception as e:
            print(f"   => [Syntax Error] 파싱 중 오류 발생: {e}")
            self.is_valid = False

    def _peek(self):
        if self.cursor < len(self.tokens):
            return self.tokens[self.cursor]
        return None

    def _consume(self):
        token = self._peek()
        self.cursor += 1
        return token

    def _parse_expression(self):
        token = self._consume()
        
        # 1. 변수 대입 ($Var = ...)
        if token == '$':
            var_name = self._consume()
            if self._peek() == '=':
                self._consume() 
                value_expr = self._parse_expression()
                return {'type': 'assign', 'name': var_name, 'value': value_expr}
            else:
                return {'type': 'variable', 'name': var_name}

        # 2. 숫자 리터럴
        if token.isdigit():
            return {'type': 'number', 'value': int(token)}

        # 3. 함수 호출 (Name(Args...))
        if self._peek() == '(':
            self._consume() 
            args = []
            if self._peek() != ')':
                while True:
                    args.append(self._parse_expression())
                    if self._peek() == ',':
                        self._consume()
                    else:
                        break
            
            if self._consume() != ')':
                raise ValueError("닫는 괄호 ')'가 없습니다.")
            
            return {'type': 'call', 'name': token, 'args': args}
        
        # 4. 단순 식별자
        return {'type': 'identifier', 'name': token}

    def execute(self, context_variables, context_functions):
        print(f"\n[3. Execution] 실행 시작...")
        if not self.is_valid:
            print("   => 실행 불가: 유효하지 않은 쿼리입니다.")
            return None

        result = self._evaluate(self.ast, context_variables, context_functions)
        print(f"   => [최종 결과]: {result}")
        return result

    def _evaluate(self, node, vars, funcs):
        # 실행 로그 출력
        # print(f"   [Exec] Node 처리 중: {node['type']}")

        if node['type'] == 'number':
            return node['value']
        
        elif node['type'] == 'variable':
            val = vars.get(node['name'], 0)
            print(f"   [Read Var] ${node['name']} -> {val}")
            return val

        elif node['type'] == 'assign':
            value = self._evaluate(node['value'], vars, funcs)
            vars[node['name']] = value
            print(f"   [Assign] ${node['name']} <- {value}")
            return value

        elif node['type'] == 'call':
            func_name = node['name']
            print(f"   [Call Func] {func_name}(...) 호출 준비")
            if func_name in funcs:
                arg_values = [self._evaluate(arg, vars, funcs) for arg in node['args']]
                result = funcs[func_name](*arg_values)
                print(f"   [Return] {func_name}{tuple(arg_values)} -> {result}")
                return result
            else:
                print(f"   [Error] 알 수 없는 함수: {func_name}")
                return None
        
        elif node['type'] == 'identifier':
            return node['name']

# 3. 쿼리 시스템
class QuerySystem:
    def __init__(self):
        self.variables = {}
        self.functions = {
            'Add': lambda a, b: a + b,
            'Sub': lambda a, b: a - b,
            'Mul': lambda a, b: a * b,
            'Print': lambda x: print(f">> [System Output]: {x}"),
        }

    def run(self, raw_query):
        q = Query(raw_query)
        q.execute(self.variables, self.functions)

# 메인 실행
if __name__ == "__main__":
    system = QuerySystem()
    print("=== 디버그 모드 쿼리 시스템 ===")
    
    # 테스트 케이스 미리 실행
    print("\n--- [테스트 1: 중첩 함수] ---")
    system.run("Print(Add(10, Mul(2, 3)))")
    
    print("\n--- [테스트 2: 변수 사용] ---")
    system.run("$x = 50")
    system.run("Print(Add($x, 10))")

    while True:
        try:
            print("\n" + "="*30)
            user_input = input("Query> ")
            if user_input.strip() == "exit":
                break
            if not user_input: continue
            
            system.run(user_input)

        except Exception as e:
            print(f"시스템 오류: {e}")