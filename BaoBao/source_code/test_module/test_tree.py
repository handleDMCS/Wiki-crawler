from tree import TreeNode, search_tree, print_tree, split_url_to_path, get_url

# Khởi tạo cây
root = TreeNode('Root')
# child3 = TreeNode('Child3')

# child1.add_child(TreeNode('Child1.1'))
# child1.add_child(TreeNode('Child1.2'))
# child2.add_child(TreeNode('Child2.1'))
# child2.add_child(TreeNode('Child2.2'))
# child3.add_child(TreeNode('Child3.1'))
# child3.add_child(TreeNode('Child3.2'))

# root.add_child(child3)

# # In cây
# print("Tree structure:")
# print_tree(root)
"""
    Printed!
    Tree structure:
    Root
    Child1
        Child1.1
        Child1.2
    Child2
        Child2.1
        Child2.2
    Child3
        Child3.1
        Child3.2
"""

# # Tìm kiếm trong cây
# search_value = 'Child2.1'
# found_node = search_tree(root, search_value)
# if found_node:
#     print(f"\nNode with value '{search_value}' found.")
# else:
#     print(f"\nNode with value '{search_value}' not found.")

"""
    Printed!
    Node with value 'Child2.1' found.
"""

# urls = [
#     "https://funix.edu.vn/chia-se-kien-thuc/chuong-trinh-hoc/kien-thuc-cntt-co-ban",
#     "https://funix.edu.vn/chia-se-kien-thuc/huong-nghiep",
#     "https://funix.edu.vn/chia-se-kien-thuc/dang-ky-tu-van"
# ]

with open(r'D:\Projects\Wiki-crawler\BaoBao\link_folder\webs_list.txt', 'r') as file:
    urls = file.read().splitlines()

for url in urls:
    path_list = split_url_to_path(url)
    root.add_child(path_list)

# In cây
print("Cấu trúc cây:")
root.print_tree()

# Thu thập và in các URL ban đầu từ cây
collected_urls = root.collect_urls()
# print('\nCác URL đã khôi phục lại ban đầu:')
# for url in collected_urls:
#     print(url)

