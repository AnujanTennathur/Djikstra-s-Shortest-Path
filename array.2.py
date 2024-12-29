from typing import Any
import numpy as np
class Array:
    """Array class - representing a one-dimensional array.
        Stipulations:
            1. Must use a numpy array as the internal data structure.
            2. Must adhere to the docstring requirements per method, including raising
               raising appropriate exceptions where indicated.
    """

    def __init__(self, size: int = 0, default_item_value: Any = None) -> None:
        """ Array Constructor. Initializes the Array with a default capacity and default value.

        Examples:
            >>> array_one = Array()
            >>> print(array_one)
            []
            >>> array_two = Array(size=10)
            >>> print(array_two)
            [None, None, None, None, None, None, None, None, None, None]
            >>> array_three = Array(size=10, default_item_value=0)
            >>> print(array_three)
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

        Args:
            size (int): the desired capacity of the Array (default is 0)
            default_item_value (Any): the desired default value of the Array (default is None)

        Returns:
            None
        """
        self._items = np.array([default_item_value] * size, dtype = object)
        self._physical_size = size
        self._logical_size = size
        self._default_item_value = default_item_value

    @staticmethod
    def from_list(list_items: list) -> 'Array':
        """
        Create an Array from a Python list.
        
        Examples: 
            >>> array = Array.from_list([1, 2, 3])
            >>> print(array) 
            [1, 2, 3]
        
        Args:
            list_items (list): the list to create the Array from.
            
        Returns:
            array (Array): A new Array instance containing the items from `list_items`
        
        Raises:
            TypeError: if list_items is not a list.
        """
        if not isinstance(list_items, list):
            raise TypeError("list_items must be a list")
        return np.array(list_items)
    
    def __getitem__(self, index: int) -> Any:
        """ Bracket operator for getting an item from an Array.

        Examples:
            >>> array = Array.from_list(['zero', 'one', 'two', 'three', 'four'])
            >>> print(array[0]) # invokes __getitem__ using the [] operator
            zero

        Args:
            index (int): the desired index.
        
        Returns:
            Any: the item at the index.
        
        Raises:
            IndexError: if the index is out of bounds.
        """
        if index < 0 or index >= len(self._items):
            raise IndexError('Must be in range of array.')
        return self._items[index]

    def __setitem__(self, index: int, data: Any) -> None:
        """ Bracket operator for setting an item in an Array.

        Examples:
            >>> array = Array.from_list(['zero', 'one', 'two', 'three', 'four'])
            >>> array[0] = 'new zero' # invokes __setitem__
            >>> print(array[0])
            new zero

        Args:
            index (int): the desired index to set.
            data (Any): the desired data to set at index.
        
        Returns:
            None
        
        Raises: 
            IndexError: if the index is out of bounds.
        """
        if index < 0 or index >= len(self._items):
            raise IndexError('Must be in range of array.')
        else:
            self._items[index] = data

    def append(self, data: Any) -> None:
        """ Append an item to the end of the Array

        Examples:
            array = Array.from_list(['zero', 'one', 'two', 'three', 'four'])
            array.append('five') # invokes append
            print(array)
            [zero, one, two, three, four, five]

        Args:
            data (Any): the desired data to append.

        Returns:
            None
        """
        if self._logical_size == self._physical_size:
            new_physical_size = self._physical_size * 2
        else:
            new_physical_size = self._physical_size
        new_array = np.array([self._default_item_value] * new_physical_size, dtype='object')
        for i in range(len(self._items)):
            new_array[i] = self._items[i]
        new_array[len(self._items)] = data
        self._items = new_array
        self._physical_size = new_physical_size
        self._logical_size += 1
        return None
        
    def __len__(self) -> int:
        """ Length operator for getting the logical length of the Array (number of items in the Array).

        Examples:
            >>> array = Array.from_list(['zero', 'one', 'two', 'three', 'four'])
            >>> print(len(array))
            5

        Returns:
            length (int): the length of the Array.
        """
        
        return self._logical_size

    def resize(self, new_size: int, default_value: Any = None) -> None:
        """ Resize an Array. Resizing to a size smaller than the current size will truncate the Array. Resizing to a larger size will append None to the end of the Array.

        Examples:
            >>> array = Array.from_list(['zero', 'one', 'two', 'three', 'four'])
            >>> array.resize(3) 
            >>> print(array)
            [zero, one, two]
            >>> array.resize(5)
            >>> print(len(array))
            5
            >>> print(array)
            [zero, one, two, None, None]

        Args:
            new_size (int): the desired new size of the Array.
            default_value (Any): the desired default value to append to the Array if the new size is larger than the current size. Only makes sense if the new_size is larger than the current size. (default is None).
        
        Returns:
            None
        
        Raises:
            ValueError: if the new size is less than 0.
        """
        if new_size < 0:
            raise ValueError("The new size cannot be a negative value")

        # Update the physical size
        self._physical_size = new_size

        # Create a new array with the desired size
        new_array = np.array([default_value] * new_size, dtype='object')

        # Copy items from the old array to the new array
        for i in range(min(new_size, len(self._items))):
            new_array[i] = self._items[i]

        # If the new size is larger, fill the remaining slots with the default value
        for i in range(len(self._items), new_size):
            new_array[i] = default_value

        # Update the items array
        self._items = new_array

        # Update the logical size
        self._logical_size = len(self._items)

        return None
        

    def __eq__(self, other: object) -> bool:
        """ Equality operator == to check if two Arrays are equal (deep check).

        Examples:
            >>> array1 = Array.from_list(['zero', 'one', 'two', 'three', 'four'])
            >>> array2 = Array.from_list(['zero', 'one', 'two', 'three', 'four'])
            >>> print(array1 == array2) 
            True

        Args:
            other (object): the instance to compare self to.
        
        Returns:
            is_equal (bool): true if the arrays are equal (deep check).
        """
        if not isinstance(other, Array):
            return False
        if len(self) != len(other):
            return False
        for item_self, item_other in zip(self, other):
            if item_self != item_other:
                return False
        return True

    def __ne__(self, other: object) -> bool:
        """ Non-Equality operator !=.
        
        Examples:
            >>> array1 = Array.from_list(['zero', 'one', 'two', 'three', 'four'])
            >>> array2 = Array.from_list(['zero', 'one', 'two', 'three', 'four'])
            >>> print(array1 != array2)
            False
        
        Args:
            other (object): the instance to compare self to.
            
        Returns:
            is_not_equal (bool): true if the arrays are NOT equal (deep check).
        """
        return not self == other

    def __iter__(self) -> Any:
        """ Iterator operator. Allows for iteration over the Array.
        Examples:
            >>> array = Array.from_list(['zero', 'one', 'two', 'three', 'four'])
            >>> for item in array: print(item, end=' ') # invokes iter
            zero one two three four 

        Yields:
            item (Any): yields the item at index
        """
        return iter(self._items)
    def __reversed__(self) -> Any:
        """ Reversed iterator operator. Allows for iteration over the Array in reverse.
        Examples:

            >>> array = Array.from_list(['zero', 'one', 'two', 'three', 'four'])
            >>> for item in reversed(array): print(item, end= ' ') # invokes __reversed__
            four three two one zero 

        Yields:
            item (Any): yields the item at index starting at the end
        """
        return reversed(self._items)

    def __delitem__(self, index: int) -> None:
        """ Delete an item in the array. Copies the array contents from index + 1 down
            to fill the gap caused by deleting the item and shrinks the array size down by one.

        Examples:

            >>> array = Array.from_list(['zero', 'one', 'two', 'three', 'four'])
            >>> del array[2]
            >>> print(array)
            [zero, one, three, four]
            >>> len(array)
            4

        Args:
            index (int): the desired index to delete.
        
        Returns:
            None
        """
        if not 0 <= index < len(self):
            raise IndexError("Index out of range")
        self._items = np.delete(self._items, index)
        self._logical_size -= 1

    def __contains__(self, item: Any) -> bool:
        """ Contains operator (in). Checks if the array contains the item.

        Examples:

            >>> array = Array.from_list(['zero', 'one', 'two', 'three', 'four'])
            >>> print('three' in array)
            True

        Args:
            item (Any): the desired item to check whether it's in the array.

        Returns:
            contains_item (bool): true if the array contains the item.
        """
        return item in self._items
    
    def __does_not_contain__(self, item: Any) -> bool:
        """ Does not contain operator (not in)

        Examples:

            >>> array = Array.from_list(['zero', 'one', 'two', 'three', 'four'])
            >>> print('five' not in array)
             True

        Args:
            item (Any): the desired item to check whether it's in the array.

        Returns:
            does_not_contains_item (bool): true if the array does not contain the item.
        """ 
        return item not in self._items 

    def clear(self) -> None:
        """ Clear the Array
        
        Examples:
        
            >>> array = Array.from_list(['zero', 'one', 'two', 'three', 'four'])
            >>> array.clear()
            >>> print(array)
            []
            >>> print(len(array))
            0
            
        Returns:
            None
        """
        self._items = np.array([self._default_item_value] * self._physical_size, dtype = 'object')
        self._logical_size = 0

        return None

    def __str__(self) -> str:
        """ Return a string representation of the data and structure. 

        Examples:

            >>> array = Array.from_list(['zero', 'one', 'two', 'three', 'four'])
            >>> print(array)
            [zero, one, two, three, four]

        Returns:
            string (str): the string representation of the data and structure.
        """
        message = "["
        for i in range(len(self._items)):
            if i == len(self._items) - 1:
                message += f"{self._items[i]}]"
            else:
                message += f"{self._items[i]}, "
        return message
    
    
    def __repr__(self) -> str:
        """ Return a string representation of the data and structure.
        
        Examples:
    
            >>> array = Array.from_list(['zero', 'one', 'two', 'three', 'four'])
            >>> print(repr(array))
        [zero, one, two, three, four]
        
        Returns:
            string (str): the string representation of the data and structure.
        """
        message = "["
        for i in range(len(self._items)):
            if i == len(self._items) - 1:
                message += f"{self._items[i]}]"
            else:
                message += f"{self._items[i]}, "
        return message
    
    def to_linked_list(self, py_list): 
        from datastructures.linked_list import LinkedList
        if not isinstance(py_list, list):
            raise TypeError("Input is not a list!")
        linked_list = LinkedList()
        for item in py_list:
            linked_list.append(item)

        return linked_list
    
    def to_list(self) -> list:
        return list(self._items)