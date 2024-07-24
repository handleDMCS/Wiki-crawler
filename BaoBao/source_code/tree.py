from pymongo import MongoClient

class TreeNode:
    def __init__(self, value):
        self.value = value
        self.children = {}

    def add_child(self, path_list):
        if not path_list:
            return
        child_name = path_list[0]
        if child_name not in self.children:
            self.children[child_name] = TreeNode(child_name)
        self.children[child_name].add_child(path_list[1:])

    def collect_urls(self, base_url=''):
        urls = []
        if base_url:
            current_url = f"{base_url}/{self.value}"
        else:
            current_url = self.value
        if not self.children:
            urls.append(current_url.replace("Root/", ""))
        else:
            for child in self.children.values():
                urls.extend(child.collect_urls(current_url))
        return urls

    def print_tree(self, level=0):
        prefix = ' ' * (level * 2)
        print(f"{prefix}{self.value}")
        for child in self.children.values():
            child.print_tree(level + 1)
    
    def to_dict(self):
        return {
            "value": self.value,
            "children": {key: child.to_dict() for key, child in self.children.items()}
        }

def search_tree(node, value):
    if node.value == value: 
        return node
    for child in node.children:
        result = search_tree(child, value)
        if result:
            return result
    return None

def print_tree(node, level=0):
    print(' ' * level * 2 + str(node.value))
    for child in node.children:
        print_tree(child, level + 1)

def split_url_to_path(url):
    return url.strip().split('/')

def get_url(urls, last_urls):
    for url in urls:
        url.replace("Root/", "")
        last_urls.append(url)

def save_tree_to_mongodb(tree, con,  db_name, collection_name='trees'):
    client = MongoClient(con)
    db = client[db_name]
    collection = db[collection_name]
    tree_dict = tree.to_dict()
    collection.insert_one(tree_dict)
    print("Tree saved to MongoDB")