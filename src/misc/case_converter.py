from humps import camelize, decamelize


def to_camel(string: str) -> str:
    return camelize(string)


def to_snake(string: str) -> str:
    return decamelize(string)
