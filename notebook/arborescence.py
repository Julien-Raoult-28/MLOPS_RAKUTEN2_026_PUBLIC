import os

EXCLUDE = {".git", "__pycache__", "venv", ".venv", ".idea", ".mypy_cache"}

def generate_tree(startpath, prefix=""):
    tree_str = ""
    items = sorted([i for i in os.listdir(startpath) if i not in EXCLUDE])
    
    for index, item in enumerate(items):
        path = os.path.join(startpath, item)
        connector = "└── " if index == len(items) - 1 else "├── "
        
        tree_str += prefix + connector + item + "\n"
        
        if os.path.isdir(path):
            extension = "    " if index == len(items) - 1 else "│   "
            tree_str += generate_tree(path, prefix + extension)
    
    return tree_str


tree = generate_tree(".")
print(tree)