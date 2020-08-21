from queue import LifoQueue
from typing import Any, Generator, List, TypeVar

Node = TypeVar("T", bound="Node")


class Node(object):
    def __init__(self, data: Any = None) -> None:
        """Initializer for Node objects.
        
        :param data: any data to be held by the Node
        """
        self.data = data
        self.children = []
        self.parent = None

    @property
    def data(self) -> Any:
        """Get objects data attribute"""
        return self.__data

    @data.setter
    def data(self, data: Any) -> None:
        """Set objects data attribute"""
        self.__data = data

    @property
    def children(self) -> List[Node]:
        """Get objects children attribute"""
        return self.__children

    @children.setter
    def children(self, children: List[Any]) -> None:
        """Set objects children attribute"""
        self.__children = children

    @property
    def parent(self) -> Node:
        """Get objects parent attribute"""
        return self.__parent

    @parent.setter
    def parent(self, parent: Node) -> None:
        """Set objects parent attribute"""
        self.__parent = parent

    def add_child(self, obj: Any) -> None:
        """Add children Nodes to current Nodes children list."""
        obj.parent = self
        self.children.append(obj)

    def traverse(self) -> Generator:
        """Traverse all nodes of tree."""
        # Put First in Stack
        stack = LifoQueue()
        stack.put(self)

        # Loop Until Tree is Exausted
        while stack.qsize() > 0:
            current = stack.get()
            for child in current.children:
                stack.put(child)
            yield current
    
    def __str__(self) -> str:
        """Display nodes data"""
        return str(self.data)

    def __repr__(self) -> str:
        """Display node child tree"""
        def dive(node: Node, last: str = "", prefix: str = "", string: List[str] = []):
            """Recursively traverse nodes and build tree.

            :param node: Node object
            :param last: tracks last special character called
            :param prefix: string to track string nesting
            :param string: list of string results from dive calls
            :return: string representation of node tree
            """
            # Determine Leaf String
            if node.parent is None:
                current = f"{prefix}└─ "
            elif node.parent.children[-1] is not node:
                current = f"{prefix}├─ "
            elif last == "├":
                current = f"{prefix}└─ "
            else:
                current = f"{''.join([prefix[:-3], (3 * ' ')])}└─ "
    
            # Track Recurse Vars
            last = current[-3]
            prefix += f"│{2 * ' '}" if last == "├" else f"{3 * ' '}"
            string.append("".join([current, node.data]))
            
            # Re-Call on Children
            for child in node.children:
                dive(child, last=last, prefix=prefix)
    
            return "\n".join(string)
    
        return dive(self)
