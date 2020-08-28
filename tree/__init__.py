from queue import LifoQueue
from typing import Any, Generator, List, TypeVar

Node = TypeVar("T", bound="Node")


class Node(object):
    __slots__ = [
        "__data",
        "__children",
        "__parent",
    ]

    def __init__(self, data: Any = None) -> None:
        """Initializer for Node objects.

        :param data: any data to be held by the Node
        """
        self.__data = data
        self.__children = []
        self.__parent = None

    @property
    def data(self) -> Any:
        """Get objects data attribute."""
        return self.__data

    @data.setter
    def data(self, data: Any) -> None:
        """Set objects data attribute."""
        self.__data = data

    @property
    def children(self) -> List[Node]:
        """Get objects children attribute."""
        return self.__children

    @property
    def parent(self) -> Node:
        """Get objects parent attribute."""
        return self.__parent

    @property
    def root(self) -> Node:
        """Get top level node of tree."""
        current = self
        while current.parent is not None:
            current = current.parent

        return current

    @property
    def siblings(self) -> List[Node]:
        """Return the nodes adjacent siblings."""
        # If Node is Root, Return Empty List
        if self.parent is None:
            return []

        return self.parent.children

    def add_child(self, obj: Any) -> None:
        """Add children Nodes to current Nodes children list."""
        # Make Node if Object is Not Already a Node Instance
        if not isinstance(obj, Node):
            obj = Node(obj)

        # Track Parent/Child Relationship
        obj.__parent = self
        self.__children.append(obj)

    def display(self, from_root: bool = False) -> str:
        """String representation of tree from either the current node or root.

        :param from_root: bool to start tree from root instead of current node
        :return: string representation of tree
        """

        def dive(
            node: Node,
            last: str = "",
            prefix: str = "",
            string: List[str] = []
        ) -> str:
            """Recursively traverse nodes and build tree.

            :param node: Node object
            :param last: tracks last special character called
            :param prefix: string to track string nesting
            :param string: list of string results from dive calls
            :return: string representation of node tree
            """
            # Determine Leaf String
            if len(prefix) == 0:
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
            string.append("".join([current, str(node.data)]))

            # Re-Call on Children
            for child in node.children:
                dive(child, last=last, prefix=prefix)

            return "\n".join(string)

        # Return Tree from Current Node or From Root
        if from_root is True:
            return dive(self.root)
        else:
            return dive(self)

    def __iter__(self) -> Generator:
        """Overloaded __iter__ method to traverse tree from current node."""
        # Init Stack
        stack = LifoQueue()
        stack.put(self)

        # Iter Through Children and Yield to Caller
        while stack.qsize() > 0:
            current = stack.get()
            for child in current.children:
                stack.put(child)

            yield current

    def __str__(self) -> str:
        """Overloaded __str__ method to print node data."""
        return str(self.data)

    def __repr__(self) -> str:
        """Overloaded __repr__ method with condensed info."""
        return f"<{self.__class__.__name__} {hex(id(self))}>"
