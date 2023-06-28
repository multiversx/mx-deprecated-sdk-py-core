import json
from pathlib import Path
from typing import Any, Dict, List, Optional


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

        if isinstance(stack[0], str):
            # Expression contained a simple, non-generic type
            return TypeFormula(stack[0], [])
        elif isinstance(stack[0], TypeFormula):
            return stack[0]
        else:
            raise Exception(f"Unexpected item on stack: {stack[0]}")

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
ENDPOINT_PARAMETER_NAME_PLACEHOLDER = "?"
ENDPOINT_PARAMETER_DESCRIPTION_PLACEHOLDER = "N / A"


class EndpointParameterDefinition:
    def __init__(self,
                 name: str,
                 description: str,
                 type_formula: 'TypeFormula',) -> None:
        self.name: str = name
        self.description: str = description
        self.type_formula: TypeFormula = type_formula

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'EndpointParameterDefinition':
        name = data.get("name", ENDPOINT_PARAMETER_NAME_PLACEHOLDER)
        description = data.get("description", ENDPOINT_PARAMETER_DESCRIPTION_PLACEHOLDER)
        type = data["type"]
        type_formula = TypeFormula.from_expression(type)

        return EndpointParameterDefinition(name, description, type_formula)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "description": self.description,
            "type": str(self.type_formula)
        }


class EndpointModifiers:
    def __init__(self,
                 mutability: str,
                 payable_in_tokens: List[str]) -> None:
        self.mutability: str = mutability
        self.payable_in_tokens: List[str] = payable_in_tokens

    @classmethod
    def default(cls) -> 'EndpointModifiers':
        return EndpointModifiers("", [])

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'EndpointModifiers':
        mutability: str = data.get("mutability", "")
        payable_in_tokens: List[str] = data.get("payableInTokens", [])

        return EndpointModifiers(mutability, payable_in_tokens)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "mutability": self.mutability,
            "payableInTokens": self.payable_in_tokens
        }


class EndpointDefinition:
    def __init__(self,
                 name: str,
                 description: str,
                 inputs: List[EndpointParameterDefinition] = [],
                 outputs: List[EndpointParameterDefinition] = [],
                 modifiers: EndpointModifiers = EndpointModifiers.default()) -> None:
        self.name: str = name
        self.description: str = description
        self.input: List[EndpointParameterDefinition] = inputs
        self.output: List[EndpointParameterDefinition] = outputs
        self.modifiers: EndpointModifiers = modifiers

    def is_constructor(self) -> bool:
        return self.name == "constructor"

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'EndpointDefinition':
        name = data.get("name", ENDPOINT_NAME_PLACEHOLDER)
        description = data.get("description", ENDPOINT_DESCRIPTION_PLACEHOLDER)
        inputs_data = data.get("inputs", [])
        outputs_data = data.get("outputs", [])

        inputs = [EndpointParameterDefinition.from_dict(input) for input in inputs_data]
        outputs = [EndpointParameterDefinition.from_dict(output) for output in outputs_data]
        modifiers = EndpointModifiers.from_dict(data)

        return EndpointDefinition(name, description, inputs, outputs, modifiers)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "description": self.description,
            "inputs": [input.to_dict() for input in self.input],
            "outputs": [output.to_dict() for output in self.output],
            **self.modifiers.to_dict()
        }


class AbiRegistry:
    def __init__(self,
                 name: str = "",
                 constructor: Optional[EndpointDefinition] = None,
                 endpoints: List[EndpointDefinition] = [],
                 types: List[TypeFormula] = []) -> None:
        self.name: str = name
        self.constructor: Optional[EndpointDefinition] = constructor
        self.endpoints: List[EndpointDefinition] = endpoints
        self.types: List[TypeFormula] = types

    @classmethod
    def from_file(cls, file_path: Path) -> 'AbiRegistry':
        text = file_path.read_text()
        data = json.loads(text)

        return AbiRegistry.from_dict(data)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'AbiRegistry':
        name = data.get("name", "")
        constructor_data = data.get("constructor", None)
        endpoints_data = data.get("endpoints", [])
        types_data = data.get("types", [])

        constructor = EndpointDefinition.from_dict(constructor_data) if constructor_data else None
        endpoints = [EndpointDefinition.from_dict(endpoint_data) for endpoint_data in endpoints_data]
        types = [TypeFormula.from_expression(type_data) for type_data in types_data]

        return AbiRegistry(name, constructor, endpoints, types)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "constructor": self.constructor.to_dict() if self.constructor else None,
            "endpoints": [endpoint.to_dict() for endpoint in self.endpoints],
            "types": [str(type) for type in self.types]
        }


if __name__ == "__main__":
    test_vectors = [
        "i64",
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

    abi_registry = AbiRegistry.from_file(Path(__file__).parent / "testdata" / "counter.abi.json")
    print(json.dumps(abi_registry.to_dict(), indent=2))
