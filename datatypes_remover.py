import ast
import re
from typing import Optional


class TypeStripper(ast.NodeTransformer):
    def __init__(self):
        self.source_lines = []

    def visit_FunctionDef(self, node):
        # Remove return type annotation
        node.returns = None
        # Remove argument type annotations
        for arg in node.args.args + node.args.kwonlyargs:
            arg.annotation = None
        if node.args.vararg:
            node.args.vararg.annotation = None
        if node.args.kwarg:
            node.args.kwarg.annotation = None
        # Remove docstring
        if (len(node.body) > 0 and
                isinstance(node.body[0], ast.Expr) and
                isinstance(node.body[0].value, ast.Str)):
            node.body = node.body[1:]
        return self.generic_visit(node)

    def visit_AnnAssign(self, node):
        # Remove annotated variable assignments (like x: int = 5)
        if node.value:
            new_node = ast.Assign([node.target], node.value)
            ast.copy_location(new_node, node)
            return new_node
        return None

    def visit_ClassDef(self, node):
        # Remove docstring from class
        if (len(node.body) > 0 and
                isinstance(node.body[0], ast.Expr) and
                isinstance(node.body[0].value, ast.Str)):
            node.body = node.body[1:]

        # Remove Protocol or ABC bases
        node.bases = [base for base in node.bases if not isinstance(base, ast.Subscript)]
        node.bases = [base for base in node.bases if not (isinstance(base, ast.Name) and base.id in ("Protocol", "ABC"))]
        return self.generic_visit(node)

    def visit_Assign(self, node):
        # Handle TypeVar assignments like T = TypeVar('T')
        if isinstance(node.value, ast.Call) and isinstance(node.value.func, ast.Name) and node.value.func.id == 'TypeVar':
            return None  # Remove TypeVar assignments
        return self.generic_visit(node)

    def visit_Module(self, node):
        # Remove module level docstring
        if (len(node.body) > 0 and
                isinstance(node.body[0], ast.Expr) and
                isinstance(node.body[0].value, ast.Str)):
            node.body = node.body[1:]
        return self.generic_visit(node)


def remove_comments(source: str) -> str:
    # Remove single line comments and inline comments
    lines = source.split('\n')
    cleaned_lines = []
    for line in lines:
        in_string = False
        string_char = None
        result = []
        i = 0
        while i < len(line):
            char = line[i]
            if char in '"\'':
                if not in_string:
                    in_string = True
                    string_char = char
                elif char == string_char:
                    in_string = False
                result.append(char)
            elif char == '#' and not in_string:
                break
            else:
                result.append(char)
            i += 1
        cleaned_line = ''.join(result).rstrip()
        if cleaned_line:
            cleaned_lines.append(cleaned_line)
    return '\n'.join(cleaned_lines)


def fix_missing_locations(node):
    """Recursively set missing locations in the AST to a default value."""
    for child in ast.walk(node):
        if not hasattr(child, 'lineno'):
            ast.copy_location(child, node)
    return node


def remove_type_hints(source: str) -> str:
    try:
        # Parse the source code into an AST
        tree = ast.parse(source)

        # Apply the TypeStripper transformer
        transformer = TypeStripper()
        modified_tree = transformer.visit(tree)

        # Fix any missing locations in the AST
        modified_tree = fix_missing_locations(modified_tree)

        # Remove any typing imports (including TypeVar, Protocol, etc.)
        modified_tree.body = [node for node in modified_tree.body
                              if not (isinstance(node, ast.ImportFrom) and
                                      node.module in ('typing', 'collections.abc')) and
                              not (isinstance(node, ast.Import) and
                                   any(name.name in ('typing', 'collections.abc')
                                       for name in node.names))]

        # Generate modified source code
        modified_source = ast.unparse(modified_tree)

        # Remove comments
        modified_source = remove_comments(modified_source)

        # Clean up any remaining type-related syntax that AST might have missed
        modified_source = re.sub(r'\s*->\s*[^:]+:', ':', modified_source)

        # Remove empty lines
        modified_source = '\n'.join(line for line in modified_source.split('\n')
                                    if line.strip())

        return modified_source

    except Exception as e:
        return f"Error processing source code: {str(e)}"


def strip_types_from_file(input_file: str, output_file: Optional[str] = None) -> None:
    # Read an input file
    with open(input_file, 'r') as f:
        source = f.read()

    # Process the source code
    modified_source = remove_type_hints(source)

    # Write to output file or print to console
    if output_file:
        with open(output_file, 'w') as f:
            f.write(modified_source)
    else:
        print(modified_source)


# # Example usage:
# if __name__ == "__main__":
#     with open("sample.py", "r") as f:
#         example_code = f.read()
#
#     with open("output.py", "w") as f:
#         f.write(remove_type_hints(example_code))
