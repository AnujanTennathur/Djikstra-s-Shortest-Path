# Collaborator: Aadem and Jenna

from typing import Any

from datastructures.linked_list import LinkedList

class ListStack:
    """ Class ListStack - representing a stack using a LinkedList
        Stipulations:
        1. Must use a LinkedList as the internal data structure from the LinkedList assignment.
        2. Must adhere to the docstring requirements per method, including raising
            raising appropriate exceptions where indicated.
    """
    def __init__(self) -> None:
        """ Constructor.
        
        Examples:
            >>> stack = ListStack()
            
        Returns:
            None
        """
        self._stack = LinkedList()
        self._top = None


    def push(self, item: Any) -> None:
        """ Push an item onto the stack.
        
        Examples:
            >>> stack = ListStack()
            >>> stack.push('cat')
            
        Args:
            item (Any): the item to push.
            
        Returns:
            None
        
        """
        self._stack.append(item)
        self._top = item

        return None

    def pop(self) -> Any:
        """ Pop an item from the stack and return the item.
        
        Examples:
            >>> stack = ListStack()
            >>> stack.push('cat')
            >>> item = stack.pop()
            >>> print(item)
            cat
            
        Returns:
            Any: the item that is popped.
            
        Raises:
            IndexError: if the stack is empty.
        """
        if self.empty:
            raise IndexError("Stack is empty!")
        
        item = self._top
        self._stack.pop_back()
        if len(self._stack) == 0:
            self._top = None
        else:
            self._top = self._stack.back

        return item

    def clear(self) -> None:
        """ Clear the stack.
        
        Examples:
            >>> stack = ListStack()
            >>> stack.push('cat')
            >>> stack.clear()
            >>> print(stack.empty)
            True
            
        Returns:
            None
        """
        self._stack.clear()
        self._top = None

        return None

    @property
    def top(self) -> Any:
        """ Get the item at the top of the stack.
        
        Examples:
            >>> stack = ListStack()
            >>> stack.push('cat')
            >>> print(stack.top)
            cat
            
        Returns:
            Any: the item that is at the top of the stack.
            
        Raises:
            IndexError: if the stack is empty.
        """
        if self.empty:
            raise IndexError("Stack is empty!")

        return self._top

    @property
    def empty(self) -> bool:
        """ Check if the stack is empty.
        
        Examples:
            >>> stack = ListStack()
            >>> print(stack.empty)
            True
        
        Returns:
            bool: True if the stack is empty, False otherwise.
        """
        if self._top == None:
            return True
        else:
            return False

    def __eq__(self, other: object) -> bool:
       """ Equality operator ==
       
       Examples:
           >>> stack1 = ListStack()
           >>> stack2 = ListStack()
           >>> print(stack1 == stack2)
           True
           
        Args:
            other (ListStack): the other ListStack to compare to
        """
       if not isinstance(other, ListStack):
            return False
       
       if len(self) != len(other):
            return False
       
       return str(self) == str(other)

    def __ne__(self, other: object) -> bool:
        """ Inequality operator !=
        
        Examples:
            >>> stack1 = ListStack()
            >>> stack2 = ListStack()
            >>> print(stack1 != stack2)
            False
            
        Args:
            other (ListStack): the other ListStack to compare to

        Returns:
            bool: True if the stacks are not equal, False otherwise.
        """
        return not self == other

    def __len__(self) -> int:
        """ Get the number of items on the stack.
        
        Examples:
            >>> stack = ListStack()
            >>> stack.push('cat')
            >>> print(len(stack))
            1
        
        Returns:
            int: the number of items on the stack.
        """
        return len(self._stack)

    def __str__(self) -> str:
        """ Get the string representation of the stack.
        
        Examples:
            >>> stack = ListStack()
            >>> stack.push('cat')
            >>> print(stack)
            'cat'
        
        Returns:
            str: the string representation of the stack.
        """
        return str(self._stack)
    
    def __repr__(self) -> str:
        """ Get the string representation of the stack.
        
        Examples:
            >>> stack = ListStack()
            >>> stack.push('cat')
            >>> print(stack)
            'cat'
        
        Returns:
            str: the string representation of the stack.
        """
        return str(self._stack)