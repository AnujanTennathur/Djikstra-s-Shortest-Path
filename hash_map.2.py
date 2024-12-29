# Collaborators: Jenna

from __future__ import annotations

from collections.abc import Iterable
import copy
from typing import Any, NamedTuple
from sympy import nextprime

from datastructures.array import Array
from datastructures.linked_list import LinkedList

class Pair(NamedTuple):
    """ Pair class - representing a key-value pair in the HashMap.
    
        Attributes:
            key (Any): The key of the pair.
            value (Any): The value of the pair.
    """
    key: Any
    value: Any

class HashMap:
    """ Class HashMap - representing a HashMap (dictionary) where the
        buckets are based on an Array and the chains are based on LinkedLists
            Stipulations:
            1. Must use an Array<LinkedList<Pair>> as the internal data structure from the
                Array, LinkedList and Tuple assignments.
            2. Must adhere to the docstring requirements per method, including raising
                raising appropriate exceptions where indicated.
            3. If the percentage of filled buckets passes a given or default threshold, resize the hash map
                to the next highest prime 
    """

    default_load_factor_threshold = 0.6

    def default_hash_function(key: Any, capacity: int) -> int:
        """ Default hash function for the HashMap classl, supports scalar and iterable keys.
            
            Args:
                key (Any): The key to hash.
                capacity (int): The capacity of the hash map.
                
            Returns:
                int: The hash of the key for a container containing the given capacity.
        """
        if isinstance(key, Iterable):
            return sum([hash(val) for val in key]) % capacity
        
        return hash(key) % capacity

    def __init__(self, capacity: int = 7, hash_function=default_hash_function, load_factor_threshold: float = default_load_factor_threshold) -> None:
        """ Constructor for the HashMap class.
            
            Examples: 
                >>> hashmap = HashMap(23)
                >>> hashmap['x'] = 3
                >>> hashmap['x']
                3
            
            Args:
                capacity (int): The capacity of the hashmap (number of buckets).
                hash_function (function): The hash function to override the default class 
                    hash function.
                
            Raises:
                TypeError: If the hash function is not a function.
                ValueError: If the capacity is less than 0.
                ValueError: If the load factor threshold is less than 0 or greater than 1.
        """
        if hash_function is None or not callable(hash_function):
            raise TypeError('Hash Function is not a function')
        
        self._buckets = Array(capacity)

        for i in range(capacity): 
            self._buckets[i] = LinkedList()
        
        self._hash_function = hash_function
        self._load_factor_threshold = HashMap.default_load_factor_threshold
        self._count = 0
    
    def _new_bucket_capacity(self) -> int:
        """ Private method to determine the best new bucket size based on the current count and the load factor threshold.
            Returns:
                int: The best bucket size.
        """
        return nextprime(int(self._count / self._load_factor_threshold)) 

    @staticmethod
    def from_dictionary(py_dict: dict) -> HashMap:
        """ Create a new HashMap from a Python dictionary. Base the size of the HashMap on the number of keys in the dictionary
            such that the load factor is less than 60%.

        Examples:
            >>> hashmap = HashMap.from_dictionary({'x': 3, 'y': 4})
            >>> hashmap['x']
            3
            >>> hashmap['y']
            4
        
        Args:
            py_dict (dict): The dictionary to convert.
        
        Returns:
            HashMap: The new HashMap.

        Raises:
            TypeError: If the input is not a dictionary.
        """
        if not isinstance(py_dict, dict): 
            raise TypeError("Input is not a dictionary.")
        capacity = nextprime(HashMap.default_load_factor_threshold * len(py_dict))
        hash_map = HashMap(capacity)
        for key in py_dict: 
            hash_map[key] = py_dict[key]
        
        return hash_map

    def __getitem__(self, key: Any) -> Any:
        """ Bracket operator for getting a value from the hash map. If the key is not present, raise a KeyError.

            Examples:
                >>> hashmap = HashMap(23)
                >>> hashmap['x'] = 3
                >>> hashmap['x']
                3

            Args:
                key (Any): The key to get the value of.

            Returns:
                Any: The value of the key.

            Raises:
                KeyError: If the key is not present in the hashmap.
        """
        bucket_number = self._hash_function(key, self.capacity)

        for pair in self._buckets[bucket_number]: 
            if pair.key == key: 
                return pair.value
        
        raise KeyError("Key does not exist.")
    
    def __setitem__(self, key: Any, value: Any) -> None:
        """ Bracket operator for setting a value in the hash map. If the key is already present, replace the value.
            If the load factor is greater than the threshold, resize the hash map.
            
            Examples:
                >>> hashmap = HashMap(23)
                >>> hashmap['x'] = 3
                >>> hashmap['x']
                3
                
            Args:
                key (Any): The key to set the value of. 
                value (Any): The value to set.

            Returns:
                None
            """
        if self.load_factor > self.load_factor_threshold: 
            self.resize_and_rehash(self._new_bucket_capacity(), self._hash_function)

        bucket_number = self._hash_function(key, self.capacity)

        for pair in self._buckets[bucket_number]:
            if pair.key == key: # key exists
                self._buckets[bucket_number].extract(pair)
                self._buckets[bucket_number].append(Pair(key, value))
                return

        self._buckets[bucket_number].append(Pair(key, value))
        self._count += 1     

    @property
    def capacity(self) -> int:
        """ Get the capacity of the hash map (number of buckets)
        
            Examples:
                >>> hashmap = HashMap(23)
                >>> hashmap.capacity
                23
            
            Returns:
                int: The capacity of the hash map.
        """
        return len(self._buckets)

    def __len__(self) -> int:
        """ Length operator for the hash map. Returns the count of the hash map.
        
            Examples:
                >>> hashmap = HashMap(23)
                >>> len(hashmap)
                0
                
            Returns:
                int: The count of the hash map.
        """
        return self._count

    def resize_and_rehash(self, new_table_size: int, new_hash_function) -> None:
        """ Resize the hash map to a new table size and rehash the items.
        
            Examples:
                >>> hashmap = HashMap(23)
                >>> hashmap.resize_and_rehash(7, lambda key: key % 7)
                
            Args:
                new_table_size (int): The new table size.
                new_hash_function (function): The new hash function to use.
            
            Returns:
                None
            """
        new_hash_map = HashMap(new_table_size, new_hash_function)
        
        for key, value in self.items(): 
            new_hash_map[key] = value
        
        self.__dict__.update(new_hash_map.__dict__)
        
    def __eq__(self, other: 'HashMap') -> bool:
        """ Equality operator for the hash map. Returns true if the hash maps are equal.
        
            Examples:
                >>> hashmap = HashMap(23)
                >>> hashmap2 = HashMap(23)
                >>> hashmap == hashmap2
                True
            
            Args:
                other (HashMap): The other hash map to compare to.
                
            Returns:
                bool: True if the hash maps are equal.
            """
        if len(self) != len(other):
            return False
        for key, value in self.items():
            if key not in other or other[key] != value:
                return False
        
        return True
            
    def __ne__(self, other: 'HashMap') -> bool:
        """ Inequality operator for the hash map. Returns true if the hash maps are not equal.
        
            Examples:
                >>> hashmap = HashMap(23)
                >>> hashmap2 = HashMap(23)
                >>> hashmap != hashmap2
                False
            
            Args:
                other (HashMap): The other hash map to compare to.
                
            Returns:
                bool: True if the hash maps are not equal.
            """
        if self.__eq__(other) == True: 
            return False
        return True
        

    def __iter__(self) -> Any:
        """ Iterator for the hash map. Returns an iterator of the keys.

            Examples:
                >>> hashmap = HashMap(23)
                >>> for key in hashmap:
                ...     print(key)

            Returns:    
                Any: An iterator of the keys.
        """
        for bucket in self._buckets: 
            for pair in bucket: 
                yield pair.key

    def __delitem__(self, key: Any) -> None:
        """ Delete an item in the hash map. Does not resize the buckets, but does remove the associated chain link.
        Examples:
            >>> hashmap = HashMap(23)
            >>> del hashmap['x']

            Args:
                key (Any): The key to delete.
                
            Returns:
                None
        """
        bucket_number = self._hash_function(key, self.capacity)
        for pair in self._buckets[bucket_number]: 
            if pair.key == key: 
                self._buckets[bucket_number].extract(pair)
                return None
            
        raise KeyError("Key does not exist.")

    @property
    def load_factor(self) -> float:
        """ Get the current load factor of the hash map (count / capacity).
        
            Examples:
                >>> hashmap = HashMap(23, default_load_factor_threshold=0.6)
                >>> hashmap.current_load_factor
                0.0
            
            Returns:
                float: The current load factor of the hash map.
        """
        return self._count/self.capacity
    
    @property
    def load_factor_threshold(self) -> float:
        """ Get the load factor threshold of the hash map.
        
            Examples:
                >>> hashmap = HashMap(23, default_load_factor_threshold=0.6)
                >>> hashmap.load_factor_threshold
                0.6
            
            Returns:
                float: The load factor threshold of the hash map.
        """
        return self._load_factor_threshold


    def __contains__(self, key: Any) -> bool:
        """ Contains operator for the hash map. Returns true if the key is in the hash map. 
        
            Examples:
                >>> hashmap = HashMap(23)
                >>> 'x' in hashmap
                False
                
            Args:
                key (Any): The key to check for.
            
            Returns:
                bool: True if the key is in the hash map.
        """
        bucket_number = self._hash_function(key, self.capacity)

        for pair in self._buckets[bucket_number]:
            if pair.key == key:
                return True
    
        return False

    def clear(self) -> None:
        """ Clear the hash map. Removes all items from the hash map.
        
            Examples:
                >>> hashmap = HashMap(23)
                >>> hashmap.clear()
                
            Returns:
                None
        """
        for bucket in self._buckets: 
            bucket.clear()
        self._count = 0

    def keys(self) -> list:
        """ Returns a view object. The view object contains the keys of the dictionary, as a list.
        
            Examples:
                >>> hashmap = HashMap(23)
                >>> keys = hashmap.keys()
                >>> for key in keys:
                ...     print(key)
                0
                1
                2
                3
                4
                5
                6
                
            Returns:
                list: The keys of the hash map.
        """
        keys = []
        for key in self: 
            keys.append(key)
        
        return keys

    def values(self) -> list:
        """ Returns a view object. The view object contains the values of the dictionary, as a list.
        
            Examples:
                >>> hashmap = HashMap(23)
                >>> values = hashmap.values()
                >>> for value in values:
                ...     print(value)
                0
                1
                2
                3
                4
                5
                6
            
            Returns:
                list: The values of the hash map.
        """
        values = []
        for bucket in self._buckets: 
            for pair in bucket: 
                values.append(copy.copy(pair.value))
        
        return values

    def items(self) -> list:
        """ Returns a view object. The view object contains the key-value pairs of the dictionary, as a list of tuples.
        
            Examples:
                >>> hashmap = HashMap(23)
                >>> hashmap['x'] = 3
                >>> items = hashmap.items()
                >>> for key, value in items:
                ...     print(key, value)
                x 3
            
            Returns:
                list: The items of the hash map.
        """
        items = []
        for bucket in self._buckets: 
            for pair in bucket: 
                items.append((pair.key, pair.value))
        
        return items

    def __str__(self) -> str:
        """ String representation of the hash map.
        
            Examples:
                >>> hashmap = HashMap(23)
                >>> print(hashmap)
                HashMap count: 0, Items: Array(
        """
        string = '{'
        for bucket in self._buckets: 
            for pair in bucket: 
                string += f'{pair.key}: {pair.value}, '
        string = string[:-2]
       
        string += '}'

        return string
    
    def __repr__(self) -> str:
        """ Representation of the hash map.
        
            Examples:
                >>> hashmap = HashMap(23)
                >>> print(hashmap)
                HashMap count: 0, Items: Array(
        """
        return str(self)