# username - dannyl
# id1      - 217416866
# name1    - Dany Liberman
# id2      - 332090224
# name2    - Liam Ichai


"""A class representing a node in an AVL tree"""
from re import search


class AVLNode(object):
	"""Constructor, you are allowed to add more fields. 
	
	@type key: int or None
	@param key: key of your node
	@type value: string
	@param value: data of your node
	"""
	def __init__(self, key, value):
		self.key = key
		self.value = value
		self.left = None
		self.right = None
		self.parent = None
		self.height = -1

	"""returns whether self is not a virtual node 

	@rtype: bool
	@returns: False if self is a virtual node, True otherwise.
	"""
	def is_real_node(self):
		return not self.height == -1


"""
A class implementing an AVL tree.
"""


class AVLTree(object):

	"""
	Constructor, you are allowed to add more fields.  

	"""
	def __init__(self):
		self.root = None
		self.max = self.root
		self._size = 0

	"""searches for a node in the dictionary corresponding to the key

	@type key: int
	@param key: a key to be searched
	@rtype: AVLNode
	@returns: node corresponding to key
	"""
	def search(self, key):
		temp = self.root
		if temp is None:
			return None
		while temp.is_real_node():
			if temp.key == key:
				return temp
			if temp.key < key:
				temp = temp.right
			else:
				temp = temp.left
		return None

	"""inserts a new node into the dictionary with corresponding key and value

	@type key: int
	@pre: key currently does not appear in the dictionary
	@param key: key of item that is to be inserted to self
	@type val: string
	@param val: the value of the item
	@param start: can be either "root" or "max"
	@rtype: int
	@returns: the number of rebalancing operation due to AVL rebalancing
	"""
	def insert(self, key, val, start="root"):
		# if the key already exists in the tree, do nothing
		if self.search(key) is not None:
			return 0
		self._size = self._size + 1
		# if tree is empty
		if self.root is None:
			self.root = AVLNode(key, val)
			self.root.height = 0
			left_child = AVLNode(None, None)
			right_child = AVLNode(None, None)
			left_child.parent = self.root
			right_child.parent = self.root
			self.root.left = left_child
			self.root.right = right_child
			return 0
		temp = None
		parent = None
		# if the key doesn't exist already, insert it in the desired way
		if start == "root":
			temp, parent = self.root_insert(key, val)
		elif start == "max":
			temp, parent = self.max_insert(key, val)
		# fix the avl tree
		child = None
		while temp is not None:
			bf = self.get_balance_factor(temp)
			child = temp.left if bf > 0 else temp.right
			child_bf = self.get_balance_factor(child)
			if bf == 2:
				if child_bf >= 0:
					self.right_rotation(temp)     # LL case
					return 1
				else:
					temp.left = self.left_rotation(child)  # LR step 1
					self.right_rotation(temp)       # LR step 2
					return 2
			elif bf == -2:
				if child_bf <= 0:
					self.left_rotation(temp)      # RR case
					return 1
				else:
					temp.right = self.right_rotation(child)  # RL step 1
					self.left_rotation(temp)          # RL step 2
					return 2
			temp = temp.parent
		return 0

	def add_new_node(self, temp, key, val):
		parent = temp.parent
		new_node = AVLNode(key, val)
		if parent.left == temp:
			parent.left = new_node
		else:
			parent.right = new_node
		new_node.parent = parent
		# Add virtual children
		new_node.left = AVLNode(None, None)
		new_node.right = AVLNode(None, None)
		new_node.left.parent = new_node
		new_node.right.parent = new_node
		# Fix heights from new node upward
		self.fix_height(new_node)
		return new_node, parent

	def fix_height(self, node):
		temp = node
		while temp is not None:
			left_height = temp.left.height if temp.left else -1
			right_height = temp.right.height if temp.right else -1
			# fix height
			temp.height = 1 + max(left_height, right_height)
			temp = temp.parent

	def root_insert(self, key, val):
		# search
		temp = self.root
		while temp.is_real_node():
			if temp.key < key:
				temp = temp.right
			else:
				temp = temp.left
		# insert
		temp, parent = self.add_new_node(temp, key, val)
		return temp, parent  # returns the new node and the parent

	def max_insert(self, key, val):
		# seach
		temp = self. max
		while temp.is_real_node():
			pass  # TODO
		# insert
		temp, parent = self.add_new_node(temp, key, val)
		return temp, parent

	# x is the unbalanced node (bf = +2), y is the new root of the rotated subtree
	def right_rotation(self, x):
		y = x.left
		x.left = y.right
		if y.right:
			y.right.parent = x
		y.right = x
		# Reconnect y to x's parent
		y.parent = x.parent
		if x.parent:
			if x.parent.left == x:
				x.parent.left = y
			else:
				x.parent.right = y
		else:
			self.root = y  # update root if x was the root
		x.parent = y
		# Fix heights from bottom up
		self.fix_height(x)
		self.fix_height(y)
		return y

	def left_rotation(self, x):
		y = x.right
		x.right = y.left
		if y.left:  # only set parent if y.left is not None
			y.left.parent = x
		y.left = x
		# Reconnect y to x's parent
		y.parent = x.parent
		if x.parent:
			if x.parent.left == x:
				x.parent.left = y
			else:
				x.parent.right = y
		x.parent = y
		# Return the new root of this subtree
		self.fix_height(x)
		self.fix_height(y)
		return y

	"""deletes node from the dictionary

	@type node: AVLNode
	@pre: node is a real pointer to a node in self
	@rtype: int
	@returns: the number of rebalancing operation due to AVL rebalancing
	"""
	def delete(self, node):
		# if the key doesn't exist in the tree, do nothing
		if self.search(node.key) is None:
			return 0
		self._size = self._size - 1
		return -1

	def BST_delete(self, node):
		is_right_son = False
		if node.parent is not None:
			is_right_son = (node.parent.right == node)
		# Case 1: no children
		if not node.right.is_real_node() and not node.left.is_real_node():
			replacement = AVLNode(None, None)
			replacement.parent = node.parent
			if node.parent is None:
				self.root = replacement
			elif is_right_son:
				node.parent.right = replacement
			else:
				node.parent.left = replacement
		# Case 2a: only right child
		elif node.right.is_real_node() and not node.left.is_real_node():
			if node.parent is None:
				self.root = node.right
			elif is_right_son:
				node.parent.right = node.right
			else:
				node.parent.left = node.right
			node.right.parent = node.parent
		# Case 2b: only left child
		elif not node.right.is_real_node() and node.left.is_real_node():
			if node.parent is None:
				self.root = node.left
			elif is_right_son:
				node.parent.right = node.left
			else:
				node.parent.left = node.left
			node.left.parent = node.parent
		# Case 3: two children
		else:
			succ = self.successor(node)
			succ_parent = succ.parent
			succ_right_child = succ.right
			# Remove successor from its original position
			if succ_parent.left == succ:
				succ_parent.left = succ_right_child
			else:
				succ_parent.right = succ_right_child
			if succ_right_child.is_real_node():
				succ_right_child.parent = succ_parent
			# Move successor to node's position
			if node.parent is None:
				self.root = succ
			elif is_right_son:
				node.parent.right = succ
			else:
				node.parent.left = succ
			succ.parent = node.parent
			#
			succ.left = node.left
			node.left.parent = succ
			succ.right = node.right
			node.right.parent = succ

	def successor(self, node):
		if node.right.is_real_node():
			return self.min(node.right)
		parent = node.parent
		while parent.is_real_node() and node == parent.right:
			node = parent
			parent = parent.parent
		return parent if parent.is_real_node() else None

	def min(self, node):
		temp = node
		while temp.left.is_real_node():
			temp = temp.left
		return temp
	"""returns an array representing dictionary 

	@rtype: list
	@returns: a sorted list according to key of touples (key, value) representing the data structure
	"""
	def avl_to_array(self):
		lst = []
		self.helper_avl_to_arr(self.root, lst)
		return lst

	def helper_avl_to_arr(self, node: AVLNode, lst: list):
		if node is None or not node.is_real_node():
			return
		if node.left.is_real_node():
			self.helper_avl_to_arr(node.left, lst)
		lst.append((node.key, node.value))
		if node.right.is_real_node():
			self.helper_avl_to_arr(node.right, lst)

	"""returns the number of items in dictionary 

	@rtype: int
	@returns: the number of items in dictionary 
	"""
	def size(self):
		return self._size

	"""returns the root of the tree representing the dictionary

	@rtype: AVLNode
	@returns: the root, None if the dictionary is empty
	"""
	def get_root(self):
		if self.root is None:
			return None
		return self.root

	"""gets amir's suggestion of balance factor

	@returns: the number of nodes which have balance factor equals to 0 devided by the total number of nodes
	"""
	def get_amir_balance_factor(self):
		# count_bf_zero = 0
		# if self.get_balance_factor() == 0:
		# 	count_bf_zero = count_bf_zero + 1  # TODO
		return None

	def get_balance_factor(self, node) -> int:
		left_height = node.left.height if node.left else -1
		right_height = node.right.height if node.right else -1
		return left_height - right_height

	"""
	DEBUG FUNCTIONS
	"""

	def print_tree(self, node=None, level=0):
		if node is None:
			node = self.root
		if not node or not node.is_real_node():
			return
		self.print_tree(node.right, level + 1)
		print("\t" * level + f"{node.key} (h={node.height})")
		self.print_tree(node.left, level + 1)
