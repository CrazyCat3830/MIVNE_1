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
		self.size = 0

	"""searches for a node in the dictionary corresponding to the key

	@type key: int
	@param key: a key to be searched
	@rtype: AVLNode
	@returns: node corresponding to key
	"""
	def search(self, key):
		temp = self.root
		while temp is not None:
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
		count = 0
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
		# if the key already exists in the tree, do nothing
		if self.search(val) is not None:
			return 0
		temp = None
		parent = None
		# if the key doesn't exist already, insert it in the desired way
		if start == "root":
			temp, parent = self.root_insert(key, val)
		elif start == "max":
			temp, parent = self.max_insert(key, val)
		# fix the avl tree
		#if the parent of the parent is real, and his bf is2 or -2, rotate!
		#if there's no parent of parent, don't worry it's cool
		if parent.parent != None:
			if parent.parent.left.height - parent.parent.right.height == 2:
				#what is the bf of the left son?
				leftBf = parent.parent.left.left.height - parent.parent.left.right.height
				#do right rotation
				if leftBf == 1:
					parent.right = parent.parent
					parent.parent.left = AVLNode(None, None)
					if parent.parent.parent != None:
						rootPerant = parent.parent.parent
						if rootPerant.left == parent.parent:
							rootPerant.left = parent
						else:
							rootPerant.right = parent
						parent.parent = rootPerant
					#if parent.parent.parent == None then the parent.parent is the root and we should update the root
					else:
						parent.parent == None
						self.root = parent
					parent.right.parent = parent
					return 1

				#do left then right rotation
				if leftBf == -1:
					temp.right = parent.parent
					temp.left = parent
					parent.parent.left = AVLNode(None, None)
					parent.right = AVLNode(None, None)
					if parent.parent.parent != None:
						rootPerant = parent.parent.parent
						if rootPerant.left == parent.parent:
							rootPerant.left = temp
						else:
							rootPerant.right = temp
						temp.parent = rootPerant
					# if parent.parent.parent == None then the parent.parent is the root and we should update the root
					else:
						temp.parent == None
						self.root = temp
					temp.right.parent = temp
					temp.left.parent = temp
					return 2

			if parent.parent.left.height - parent.parent.right.height == -2:
				# what is the bf of the right son?
				rightBf = parent.parent.right.left.height - parent.parent.right.right.height
				# do right then left rotation
				if rightBf == 1:
					temp.right = parent
					temp.left = parent.parent
					parent.parent.right = AVLNode(None, None)
					parent.left = AVLNode(None, None)
					if parent.parent.parent != None:
						rootPerant = parent.parent.parent
						if rootPerant.left == parent.parent:
							rootPerant.left = temp
						else:
							rootPerant.right = temp
						temp.parent = rootPerant
					# if parent.parent.parent == None then the parent.parent is the root and we should update the root
					else:
						temp.parent == None
						self.root = temp
					temp.right.parent = temp
					temp.left.parent = temp
					return 2

				# do left rotation
				if rightBf == -1:
					parent.left = parent.parent
					parent.parent.right = AVLNode(None, None)
					if parent.parent.parent != None:
						rootPerant = parent.parent.parent
						if rootPerant.left == parent.parent:
							rootPerant.left = parent
						else:
							rootPerant.right = parent
						parent.parent = rootPerant
					# if parent.parent.parent == None then the parent.parent is the root and we should update the root
					else:
						parent.parent == None
						self.root = parent
					parent.left.parent = parent
					return 1

		return count

	def add_new_node(self, temp, key, val):
		parent = temp.parent
		new_node = AVLNode(key, val)
		if parent.key > key:
			parent.left = new_node
		else:
			parent.right = new_node
		new_node.parent = parent
		new_node_left = AVLNode(None, None)
		new_node_right = AVLNode(None, None)
		new_node.left = new_node_left
		new_node.right = new_node_right
		# children need their parent
		new_node_left.parent = new_node
		new_node_right.parent = new_node
		# fix fields
		self.fix_height(temp)
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
			pass
		# insert
		temp, parent = self.add_new_node(temp, key, val)
		return temp, parent

	def right_rotation(self, x, y):
		pass

	def left_rotation(self, x, y):
		pass
	
	"""deletes node from the dictionary

	@type node: AVLNode
	@pre: node is a real pointer to a node in self
	@rtype: int
	@returns: the number of rebalancing operation due to AVL rebalancing
	"""
	def delete(self, node):
		#self.size -= 1
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
		return None

	"""returns the number of items in dictionary 

	@rtype: int
	@returns: the number of items in dictionary 
	"""
	def size(self):
		return self.size

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
		count_bf_zero = 0
		if self.get_balance_factor() == 0:
			count_bf_zero = count_bf_zero + 1  # TODO
		return None

	def get_balance_factor(self) -> int:
		left_height = self.root.left.height if self.left else -1
		right_height = self.root.right.height if self.right else -1
		return left_height - right_height

