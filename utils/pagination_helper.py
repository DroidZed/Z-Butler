class PaginationHelper:
    """
    ## Utility class for list pagination operations.

    This class is helpful for managing large lists and dividing them into smaller chunks or pages.

    Example usage:
    ```py
        # Create a PaginationHelper instance
        helper = PaginationHelper(['A', 'B', 'C', 'D', 'E', 'F', 'G'], 3)

        # Get the paginated list
        paged_list = helper.paged_list
        print(paged_list)  # Output: [['A', 'B', 'C'], ['D', 'E', 'F'], ['G']]

        # Get the total number of pages
        pages_count = helper.pages_count
        print(pages_count)  # Output: 3

        # Get a specific page by its index
        page_index = 1
        page_items = helper.get_page(page_index)
        print(page_items)  # Output: ['D', 'E', 'F']

        # Get the page index of a given item
        item_index = 4
        item_page_index = helper.get_page_index(item_index)
        print(item_page_index)  # Output: 1

        # Update the page size and re-paginate the list
        new_size = 2
        helper.update_page_size(new_size)

        # Get the updated paginated list
        paged_list = helper.paged_list
        print(paged_list)  # Output: [['A', 'B'], ['C', 'D'], ['E', 'F'], ['G']]

        # Get the updated total number of pages
        pages_count = helper.pages_count
        print(pages_count)  # Output: 4
    ```
    """

    def __init__(
        self, collection: list, items_per_page: int
    ):
        """
        Initialize the PaginationHelper with a collection and items per page.

        Args:
            collection (list): The list to paginate.
            items_per_page (int): The maximum size of each page.
        """
        self._collection = collection
        self._page_size = items_per_page
        self._paginate_list()

    def _paginate_list(self):
        """
        Paginates the collection into smaller chunks or pages based on the items per page.
        """
        self._paged_collection = [
            self._collection[i : i + self._page_size]
            for i in range(
                0, len(self._collection), self._page_size
            )
        ]
        self._pages_count = len(self._paged_collection)

    @property
    def paged_list(self):
        """
        Get the paginated list.

        Returns:
            list: The paginated list.
        """
        return self._paged_collection

    @property
    def pages_count(self):
        """
        Get the total number of pages.

        Returns:
            int: The total number of pages.
        """
        return self._pages_count

    def update_page_size(self, new_size: int):
        """
        Update the items per page and re-paginate the list.

        Args:
            new_size (int): The new size of items per page.
        """
        if new_size > 0:
            self._page_size = new_size
            self._paginate_list()

    def get_page(self, page_index: int) -> list:
        """
        Get a specific page by its index.

        Args:
            page_index (int): The index of the desired page.

        Returns:
            list: The list of items on the specified page.
        """
        if 0 <= page_index < self._pages_count:
            return self._paged_collection[page_index]
        return []

    def get_page_index(self, item_index: int) -> int:
        """
        Get the page index where a given item index is located.

        Args:
            item_index (int): The index of the item.

        Returns:
            int: The index of the page where the item is located.
        """
        if 0 <= item_index < len(self._collection):
            return item_index // self._page_size
        return -1

    def update_list(self, new_collection: list):
        """
        Update the underlying collection and re-paginate the list.

        Args:
            new_collection (list): The new collection to replace the existing one.
        """
        self._collection = new_collection
        self._paginate_list()
