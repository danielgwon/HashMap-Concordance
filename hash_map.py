# TODO: check if you need to reduce capacity by one when hashing due to 0-based indexing

# hash_map.py
# ===================================================
# Implement a hash map with chaining
# ===================================================

class SLNode:
    def __init__(self, key, value):
        self.next = None
        self.key = key
        self.value = value

    def __str__(self):
        return '(' + str(self.key) + ', ' + str(self.value) + ')'


class LinkedList:
    def __init__(self) -> object:
        self.head = None
        self.size = 0

    def add_front(self, key, value):
        """Create a new node and inserts it at the front of the linked list
        Args:
            key: the key for the new node
            value: the value for the new node"""
        new_node = SLNode(key, value)
        new_node.next = self.head
        self.head = new_node
        self.size = self.size + 1

    def remove(self, key):
        """Removes node from linked list
        Args:
            key: key of the node to remove """
        if self.head is None:
            return False
        if self.head.key == key:
            self.head = self.head.next
            self.size = self.size - 1
            return True
        cur = self.head.next
        prev = self.head
        while cur is not None:
            if cur.key == key:
                prev.next = cur.next
                self.size = self.size - 1
                return True
            prev = cur
            cur = cur.next
        return False

    def contains(self, key):
        """Searches linked list for a node with a given key
        Args:
        	key: key of node
        Return:
        	node with matching key, otherwise None"""
        if self.head is not None:
            cur = self.head
            while cur is not None:
                if cur.key == key:
                    return cur
                cur = cur.next
        return None

    def replace(self, key, value):
        """
        Replaces the value in the node with the given key with the given value

        Pre-condition: there is a node with given key in the linked list
        :param key: key of node
        :param value: value to insert into the node
        :return: n/a
        """

        # navigate to the node with the given key
        cur = self.head
        while cur.key != key:
            cur = cur.next

        # replace the node's current value with the given value
        cur.value = value

    def __str__(self):
        out = '['
        if self.head != None:
            cur = self.head
            out = out + str(self.head)
            cur = cur.next
            while cur != None:
                out = out + ' -> ' + str(cur)
                cur = cur.next
        out = out + ']'
        return out


def hash_function_1(key):
    hash = 0
    for i in key:
        hash = hash + ord(i)
    return hash


def hash_function_2(key):
    hash = 0
    index = 0
    for i in key:
        hash = hash + (index + 1) * ord(i)
        index = index + 1
    return hash


class HashMap:
    """
    Creates a new hash map with the specified number of buckets.
    Args:
        capacity: the total number of buckets to be created in the hash table
        function: the hash function to use for hashing values
    """

    def __init__(self, capacity, function):
        self._buckets = []
        for i in range(capacity):
            self._buckets.append(LinkedList())
        self.capacity = capacity
        self._hash_function = function
        self.size = 0

    def clear(self):
        """
        Empties out the hash table deleting all links in the hash table.
        """
        self._buckets = []
        for i in range(self.capacity):
            self._buckets.append(LinkedList())
        self.size = 0

    def get(self, key):
        """
        Returns the value with the given key.
        Args:
            key: the value of the key to look for
        Return:
            The value associated to the key. None if the link isn't found.
        """

        # get the index of the hash table
        index = self._get_index(key)

        # save result of contains
        result = self._buckets[index].contains(key)

        # if contains is None, return None
        if result is None:
            return None

        # else, return the value of the returned node
        else:
            return result.value

    def resize_table(self, capacity):
        """
        Resizes the hash table to have a number of buckets equal to the given
        capacity. All links need to be rehashed in this function after resizing
        Args:
            capacity: the new number of buckets.
        """

        # create a new array of buckets
        new_hash_table = []
        for _ in range(capacity):
            new_hash_table.append(LinkedList())

        # check if current buckets are filled
        if self.size == 0:
            self._buckets = new_hash_table
            self.capacity = capacity

        else:
            for bucket in self._buckets:

                # if a bucket is filled, traverse through the linked list
                if bucket.head is not None:

                    # recalculate the hash for each node in the linked list using given capacity
                    cur = bucket.head
                    while cur is not None:
                        new_index = self._get_index(cur.key, capacity)

                        # add the key and value of the node to its new bucket in the new array of buckets
                        new_hash_table[new_index].add_front(cur.key, cur.value)
                        cur = cur.next

                # if a bucket is not filled, continue to the next bucket

        # update the hash map's buckets and capacity
        self._buckets = new_hash_table
        self.capacity = capacity

    def put(self, key, value):
        """
        Updates the given key-value pair in the hash table. If a link with the given
        key already exists, this will just update the value and skip traversing. Otherwise,
        it will create a new link with the given key and value and add it to the table
        bucket's linked list.

        Args:
            key: they key to use to has the entry
            value: the value associated with the entry
        """

        # calculate the hash
        index = self._get_index(key)
        bucket = self._buckets[index]

        # navigate to the hash-specified index
        # search for key with contains()
        # if contains is true, replace the value
        if self._buckets[index].contains(key):
            bucket.replace(key, value)

        # if contains is false, add_front() the new link
        else:
            bucket.add_front(key, value)
            self.size += 1

    def remove(self, key):
        """
        Removes and frees the link with the given key from the table. If no such link
        exists, this does nothing. Remember to search the entire linked list at the
        bucket.
        Args:
            key: they key to search for and remove along with its value
        """

        # get the index in the hash table using the given key
        index = self._get_index(key)

        # use the LinkedList method, remove()
        self._buckets[index].remove(key)

    def contains_key(self, key):
        """
        Searches to see if a key exists within the hash table

        Returns:
            True if the key is found False otherwise

        """

        # return False if the hash map is empty
        if self.size == 0:
            return False

        else:

            # calculate the index with the given key
            index = self._get_index(key)
            bucket = self._buckets[index]

            if bucket.contains(key):
                return True
            return False

    def empty_buckets(self):
        """
        Returns:
            The number of empty buckets in the table
        """
        # TODO: check if size is zero before checking all buckets
        empty = 0
        for bucket in self._buckets:
            if bucket.head is None:     # chain is empty
                empty += 1
        return empty

    def table_load(self):
        """
        Returns:
            the ratio of (number of links) / (number of buckets) in the table as a float.

        """
        return self.size / self.capacity

    def _get_index(self, key, capacity=None):
        """
        Used to calculate the index for a given key.
        If the capacity is not given, use HashMap's current capacity value
        :param key: key to calculate a hash with
        :param capacity: number of buckets to calculate an appropriate index
        :return: index of the appropriate bucket
        """
        if capacity is None:
            capacity = self.capacity

        return self._hash_function(key) % capacity

    def __str__(self):
        """
        Prints all the links in each of the buckets in the table.
        """

        out = ""
        index = 0
        for bucket in self._buckets:
            out = out + str(index) + ': ' + str(bucket) + '\n'
            index = index + 1
        return out
