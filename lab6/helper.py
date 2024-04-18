import os
from code_analysis import ASTReader

reader = ASTReader()
path_ast = "ast"

kits = []
for dir_kit in os.listdir(path_ast): # List all kits
    if os.path.isdir(os.path.join(path_ast, dir_kit)):
        kits.append(dir_kit)
kits = sorted(kits)


for kit in kits:
    kit_files = []
    for root, dirs, files in os.walk(os.path.join(path_ast, kit)): # Find all files for this kit
        kit_files.extend((os.path.join(root, file) for file in files))

    for file in kit_files:
        ast = reader.read_ast(file)
