#username - dannyl
#id1      - 217416866
#name1    - Dany Liberman
#id2      - 332090224
#name2    - Liam Ichai


"""A class represnting a node in an AVL tree"""
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
		if self.search(val) is not None:
			return count
		parent = None
		if start == "root":
			# search
			temp = self.root
			while temp is not None:
				if temp.key < key:
					temp = temp.right
				else:
					temp = temp.left
			# insert
			temp, parent = self.add_new_node(temp, key, val)

		if start == "max":
			pass

		#  temp.parent = temp.height + 1
		while parent.is_real_node():
			bf = parent.left.height - parent.right.height
			pass
		return count


	def add_new_node(self, temp, key, val):
		parent = temp.parent
		new_node = AVLNode(key, val)
		if parent.key > key:
			parent.left = new_node
		else:
			parent.right = new_node
		new_node.parent = parent
		new_node.left = AVLNode(None, None)
		new_node.right = AVLNode(None, None)
		return (new_node, parent)

	"""deletes node from the dictionary

	@type node: AVLNode
	@pre: node is a real pointer to a node in self
	@rtype: int
	@returns: the number of rebalancing operation due to AVL rebalancing
	"""
	def delete(self, node):
		#self.size -= 1
		return -1

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
			count_bf_zero = count_bf_zero + 1 # TODO
		return None


	def get_balance_factor(self) -> int:
		left_height = self.left.height if self.left else 0
		right_height = self.right.height if self.right else 0
		return left_height - right_height

