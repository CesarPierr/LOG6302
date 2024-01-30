#!/usr/bin/env python

# LOG6302A - Lab1 - AST & visitor examples

# Load AST

from code_analysis import AST, ASTReader

reader = ASTReader()
ast = reader.read_ast("../example/example_1.php.ast.json")
ast_2 = reader.read_ast("../example/example_2.php.ast.json")

# Access AST information

'''
ast.get_root()       # Return the root node ID
ast.get_type(45)     # Return the type of node 45
ast.get_image(45)    # Return the image of node 45
ast.get_children(45) # Return the list of children
ast.get_parent(45)   # Return the list of parents
ast.get_position(45) # Return the position in source file as an
                     # array [line_begin, line_end, column_begin, column_end, token_begin, token_end]
'''

root = ast.get_root()
print(f"Root node ID is {root}")
print(f"Root type is {ast.get_type(root)}")

print(f"Node root children are {ast.get_children(root)}")
for node_id in ast.get_children(root):
    print(f"Node type of {node_id} is {ast.get_type(node_id)}")
print("\n")


# Create a visitor that returns function definition position in source file


class ASTFunctionDefinitionVisitor:
    def __init__(self):
        self.ast = None

    def visit(self, ast: AST):
        self.ast = ast
        print(f"Visit AST from file {self.ast.get_filename()}")
        self.__visit(self.ast.get_root())

    def __visit(self, node_id: int):
        if self.ast.get_type(node_id) == "FunctionStatement":
            print(f"Function '{self.ast.get_image(node_id)}' definition is from "
                  f"line {self.ast.get_position(node_id)[0]} to {self.ast.get_position(node_id)[1]}")

        for child_id in self.ast.get_children(node_id):
            self.__visit(child_id)


visitor = ASTFunctionDefinitionVisitor()
visitor.visit(ast)
visitor.visit(ast_2)
print("\n")


# Create a visitor that returns function call position in source file

class ASTFunctionCallVisitor:
    def __init__(self):
        self.ast = None

    def visit(self, ast: AST):
        self.ast = ast
        print(f"Visit AST from file {self.ast.get_filename()}")
        self.__visit(self.ast.get_root())

    def __visit(self, node_id: int):
        if self.ast.get_type(node_id) == "FunctionCall":
            print(f"Function '{self.ast.get_image(node_id)}' is called "
                  f"at line {self.ast.get_position(node_id)[0]}")

        for child_id in self.ast.get_children(node_id):
            self.__visit(child_id)


visitor = ASTFunctionCallVisitor()
visitor.visit(ast)
visitor.visit(ast_2)
