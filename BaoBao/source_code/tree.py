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

    def search_tree(self, value):
        if self.value == value: 
            return self
        for child in self.children:
            result = child.search_tree(value)
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

def save_tree_to_mongodb(tree, collection_tree):
    tree_dict = tree.to_dict()
    collection_tree.insert_one(tree_dict)
    print("Tree saved to MongoDB")