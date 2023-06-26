from typing import Any, List


class TypeFormula:
    def __init__(self, name: str, type_parameters: List['TypeFormula']) -> None:
        self.name: str = name
        self.type_parameters: List[TypeFormula] = type_parameters

    @classmethod
    def from_expression(cls, expression: str) -> 'TypeFormula':
        return TypeFormulaParser().parse_expression(expression)

    def __str__(self) -> str:
        if self.type_parameters:
            type_parameters = ", ".join([str(type_parameter) for type_parameter in self.type_parameters])
            return f"{self.name}<{type_parameters}>"
        else:
            return self.name


class TypeFormulaParser:
    BEGIN_TYPE_PARAMETERS = "<"
    END_TYPE_PARAMETERS = ">"
    COMMA = ","
    PUNCTUATION = [COMMA, BEGIN_TYPE_PARAMETERS, END_TYPE_PARAMETERS]

    def parse_expression(self, expression: str) -> TypeFormula:
        tokens = self._tokenize_expression(expression)
        tokens = [token for token in tokens if token != TypeFormulaParser.COMMA]

        stack: List[Any] = []

        for token in tokens:
            if token in TypeFormulaParser.PUNCTUATION:
                if token == TypeFormulaParser.END_TYPE_PARAMETERS:
                    type_parameters: List[TypeFormula] = []

                    while stack[-1] != TypeFormulaParser.BEGIN_TYPE_PARAMETERS:
                        item = stack.pop()
                        if isinstance(item, TypeFormula):
                            type_formula = item
                        else:
                            type_formula = TypeFormula(item, [])

                        type_parameters.append(type_formula)

                    stack.pop()  # pop "<" symbol
                    type_name = stack.pop()
                    type_formula = TypeFormula(type_name, list(reversed(type_parameters)))
                    stack.append(type_formula)
                elif token == TypeFormulaParser.BEGIN_TYPE_PARAMETERS:
                    # The symbol is pushed as a simple string,
                    # as it will never be interpreted, anyway.
                    stack.append(token)
                elif token == TypeFormulaParser.COMMA:
                    # We simply ignore commas
                    pass
                else:
                    raise Exception(f"Unexpected token (punctuation): {token}")
            else:
                # It's a type name. We push it as a simple string.
                stack.append(token)

        assert len(stack) == 1
        assert isinstance(stack[0], TypeFormula)
        return stack[0]

    def _tokenize_expression(self, expression: str) -> List[str]:
        tokens: List[str] = []
        current_token = ""

        for i in range(len(expression)):
            character = expression[i]

            if not character.strip():
                pass
            elif character not in TypeFormulaParser.PUNCTUATION:
                current_token += character
            else:
                if current_token:
                    tokens.append(current_token)
                    current_token = ""
                tokens.append(character)

        if current_token:
            tokens.append(current_token)

        return tokens


ENDPOINT_NAME_PLACEHOLDER = "?"
ENDPOINT_DESCRIPTION_PLACEHOLDER = "N / A"


class EndpointParameterDefinition:
    def __init__(self,
                 type_formula: 'TypeFormula',
                 name: str = ENDPOINT_NAME_PLACEHOLDER,
                 description: str = ENDPOINT_DESCRIPTION_PLACEHOLDER) -> None:
        self.name: str = name
        self.description: str = description
        self.type_formula: TypeFormula = type_formula


class EndpointModifiers:
    def __init__(self,
                 mutability: str,
                 payable_in_tokens: List[str]) -> None:
        self.mutability: str = mutability
        self.payable_in_tokens: List[str] = payable_in_tokens

    @classmethod
    def default(cls) -> 'EndpointModifiers':
        return EndpointModifiers("", [])


class EndpointDefinition:
    def __init__(self,
                 name: str,
                 input: List[EndpointParameterDefinition] = [],
                 output: List[EndpointParameterDefinition] = [],
                 modifiers: EndpointModifiers = EndpointModifiers.default()) -> None:
        self.name: str = name
        self.input: List[EndpointParameterDefinition] = input
        self.output: List[EndpointParameterDefinition] = output
        self.modifiers: EndpointModifiers = modifiers

    def is_constructor(self) -> bool:
        return self.name == "constructor"


if __name__ == "__main__":
    test_vectors = [
        "MultiResultVec<MultiResult2<Address, u64>>",
        "tuple3<i32, bytes, Option<i64>>",
        "tuple2<i32, i32>",
        "tuple<List<u64>, List<u64>>"
    ]

    for test_vector in test_vectors:
        print(f"Test vector: {test_vector}")
        type_formula = TypeFormula.from_expression(test_vector)
        print(f"Type formula: {type_formula}")

        if str(type_formula) != test_vector:
            raise Exception(f"Type formula [{type_formula}] != [{test_vector}]")
