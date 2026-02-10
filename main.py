import re

# 1. 토크나이저: 문자열을 의미 있는 최소 단위(Token)로 쪼갭니다.
# 기존의 복잡한 정규식 하나로 해결하려는 방식을 버리고, 단순히 조각을 내는 역할만 합니다.
def tokenize(query_str):
    # 패턴: 함수명/변수명, 숫자, 특수문자((, ), ,(콤마), =)
    token_pattern = r"([a-zA-Z_][a-zA-Z0-9_]*|[0-9]+|[(),=]|\$)"
    tokens = re.findall(token_pattern, query_str)
    return tokens

# 2. 쿼리 객체: 파싱된 결과(구문 트리)를 저장하고, 실행할 수 있는 객체입니다.
class Query:
    def __init__(self, raw_query):
        self.raw_query = raw_query
        self.tokens = tokenize(raw_query)
        self.ast = None  # Abstract Syntax Tree (추상 구문 트리)
        self.is_valid = False
        self._parse() # 생성 시 바로 파싱 시도

    def _parse(self):
        """
        토큰 리스트를 분석하여 구조화된 데이터(AST)로 만듭니다.
        재귀적(Recursive) 방식을 사용하여 중첩된 함수(Add(Mul(...)))도 처리합니다.
        """
        if not self.tokens:
            return

        self.cursor = 0
        try:
            # 파싱 시작 (변수 대입 또는 단순 함수 실행)
            self.ast = self._parse_expression()
            self.is_valid = True
        except Exception as e:
            print(f"[Syntax Error] 파싱 중 오류 발생: {e}")
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
        
        # 1. 변수 대입 패턴: $Var = ...
        if token == '$':
            var_name = self._consume()
            if self._peek() == '=':
                self._consume() # '=' 소비
                value_expr = self._parse_expression() # 우변 파싱
                return {'type': 'assign', 'name': var_name, 'value': value_expr}
            else:
                # 대입이 아니라 값을 불러오는 경우 ($Var)
                return {'type': 'variable', 'name': var_name}

        # 2. 숫자 리터럴
        if token.isdigit():
            return {'type': 'number', 'value': int(token)}

        # 3. 함수 호출 패턴: Name(Arg1, Arg2, ...)
        if self._peek() == '(':
            self._consume() # '(' 소비
            args = []
            if self._peek() != ')':
                while True:
                    args.append(self._parse_expression()) # 인자를 재귀적으로 파싱
                    if self._peek() == ',':
                        self._consume()
                    else:
                        break
            
            if self._consume() != ')':
                raise ValueError("닫는 괄호 ')'가 없습니다.")
            
            return {'type': 'call', 'name': token, 'args': args}
        
        # 4. 단순 문자열/식별자 (예: exit)
        return {'type': 'identifier', 'name': token}

    def execute(self, context_variables, context_functions):
        """
        파싱된 트리를 바탕으로 실제 로직을 수행합니다.
        context_variables: 변수 저장소 (Dictionary)
        context_functions: 실행 가능한 함수 저장소 (Dictionary)
        """
        if not self.is_valid:
            print("실행 불가: 유효하지 않은 쿼리입니다.")
            return None

        return self._evaluate(self.ast, context_variables, context_functions)

    def _evaluate(self, node, vars, funcs):
        if node['type'] == 'number':
            return node['value']
        
        elif node['type'] == 'variable':
            # 변수 값 조회
            if node['name'] in vars:
                return vars[node['name']]
            else:
                print(f"[Error] 정의되지 않은 변수: ${node['name']}")
                return 0

        elif node['type'] == 'assign':
            # 변수 할당 실행
            value = self._evaluate(node['value'], vars, funcs)
            vars[node['name']] = value
            return value

        elif node['type'] == 'call':
            # 함수 실행
            func_name = node['name']
            if func_name in funcs:
                # 인자들을 먼저 모두 계산(Evaluate)한 뒤 함수에 전달
                arg_values = [self._evaluate(arg, vars, funcs) for arg in node['args']]
                return funcs[func_name](*arg_values)
            else:
                print(f"[Error] 알 수 없는 함수: {func_name}")
                return None
        
        elif node['type'] == 'identifier':
            return node['name']

# 3. 쿼리 시스템 (Context): 변수와 함수를 관리하는 주체
class QuerySystem:
    def __init__(self):
        self.variables = {}
        # 시스템에서 사용할 함수들을 등록합니다.
        self.functions = {
            'Add': lambda a, b: a + b,
            'Sub': lambda a, b: a - b,
            'Mul': lambda a, b: a * b,
            'Print': lambda x: print(f">> Output: {x}"),
            'GetInfo': lambda: "Mechanical Engineering Query System v1.0"
        }

    def run(self, raw_query):
        # 쿼리 객체 생성 (파싱)
        q = Query(raw_query)
        
        # 쿼리 실행 (재사용 가능)
        result = q.execute(self.variables, self.functions)
        
        # 결과가 있으면 출력 (할당문이나 Print함수가 아닌 경우)
        if result is not None and q.ast['type'] not in ['assign', 'call']:
             print(f"=> {result}")

# 4. 메인 실행 루프
if __name__ == "__main__":
    system = QuerySystem()
    print("쿼리 시스템이 시작되었습니다. (종료: exit)")
    print("사용 예시: Add(10, 20) 또는 $x = Mul(5, 5) 또는 Print($x)")

    while True:
        try:
            user_input = input("Query> ")
            if user_input.strip() == "exit":
                break
            
            if not user_input:
                continue

            # ';' 기준으로 여러 명령어가 들어올 경우 처리
            commands = user_input.split(';')
            for cmd in commands:
                if cmd.strip():
                    system.run(cmd.strip())

        except Exception as e:
            print(f"시스템 오류 발생: {e}")