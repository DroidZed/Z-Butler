from utils.pagination_helper import PaginationHelper
import pytest


class TestPagination:
    helper = PaginationHelper([i for i in range(20)], 3)

    def test_should_guess_the_correct_page_of_the_given_item_index(
        self,
    ):
        assert self.helper.get_page_index(5) == 1
        assert self.helper.get_page_index(7) == 2
        assert self.helper.get_page_index(11) == 3

    def test_should_not_find_item(
        self,
    ):
        assert self.helper.get_page_index(21) == -1

    def test_on_empty_array(
        self,
    ):
        self.helper.update_page_size(0)
        assert self.helper.get_page_index(21) == -1
