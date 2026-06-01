class LLNode:
    def __init__(self, nama, buku, rating):
        self.nama = nama
        self.buku = buku
        self.rating = int(rating)
        self.next = None

class linkedlist:
    def __init__(self):
        self.head = None

    def insert(self, nama, buku, rating):
        new_node = LLNode(nama, buku, int(rating))
        if not self.head:
            self.head = new_node
            return True
        current = self.head
        while current.next:
            current = current.next
        current.next = new_node
        return True

    def delete(self, nama, buku):
        current = self.head
        prev = None
        while current:
            if current.nama == nama and current.buku == buku:
                if prev:
                    prev.next = current.next
                else:
                    self.head = current.next
                return True
            prev = current
            current = current.next
        return False

    def update(self, nama, buku, new_rating):
        current = self.head
        while current:
            if current.nama == nama and current.buku == buku:
                current.rating = int(new_rating)
                return True
            current = current.next
        return False

    def get_all_data(self):
        data = []
        current = self.head
        while current:
            data.append((current.nama, current.buku, current.rating))
            current = current.next
        return data

    def get_unique_books_with_max_rating(self):
        book_ratings = {}
        current = self.head
        while current:
            if current.buku not in book_ratings:
                book_ratings[current.buku] = current.rating
            else:
                book_ratings[current.buku] = max(book_ratings[current.buku], current.rating)
            current = current.next
        result = [(buku, rating) for buku, rating in book_ratings.items()]
        return sorted(result, key=lambda x: x[1], reverse=True)

class stack:
    def __init__(self):
        self.items = []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        if not self.is_empty():
            return self.items.pop()
        return None

    def peek(self):
        if not self.is_empty():
            return self.items[-1]
        return None

    def is_empty(self):
        return len(self.items) == 0

    def size(self):
        return len(self.items)

class queue:
    def __init__(self):
        self.items = []

    def enqueue(self, item):
        self.items.append(item)

    def dequeue(self):
        if not self.is_empty():
            return self.items.pop(0)
        return None

    def peek(self):
        if not self.is_empty():
            return self.items[0]
        return None

    def is_empty(self):
        return len(self.items) == 0

    def size(self):
        return len(self.items)

class TreeNode:
    def __init__(self, buku, rating):
        self.buku = buku
        self.rating = int(rating)
        self.left = None
        self.right = None

class bst:
    def __init__(self):
        self.root = None

    def insert(self, buku, rating):
        self.root = self._insert_recursive(self.root, buku, int(rating))

    def inorder(self, node, result):
        if node:
            self.inorder(node.left, result)
            result.append((node.buku, node.rating))
            self.inorder(node.right, result)

    def _insert_recursive(self, node, buku, rating):
        if not node:
            return TreeNode(buku, rating)
        if buku < node.buku:
            node.left = self._insert_recursive(node.left, buku, rating)
        elif buku > node.buku:
            node.right = self._insert_recursive(node.right, buku, rating)
        else:
            node.rating = max(node.rating, rating)
        return node

    def search(self, buku):
        return self._search_recursive(self.root, buku)

    def _search_recursive(self, node, buku):
        if not node or node.buku == buku:
            return node
        if buku < node.buku:
            return self._search_recursive(node.left, buku)
        return self._search_recursive(node.right, buku)

    def get_books_by_min_rating(self, min_rating):
        result = []
        self._traverse_by_rating(self.root, result, min_rating)
        return sorted(result, key=lambda x: x[1], reverse=True)

    def _traverse_by_rating(self, node, result, min_rating):
        if not node:
            return
        self._traverse_by_rating(node.left, result, min_rating)
        if node.rating >= min_rating:
            result.append((node.buku, node.rating))
        self._traverse_by_rating(node.right, result, min_rating)

    def get_books_by_rating_range(self, min_rating, max_rating):
        result = []
        self._traverse_range(self.root, result, min_rating, max_rating)
        return sorted(result, key=lambda x: x[1], reverse=True)

    def _traverse_range(self, node, result, min_rating, max_rating):
        if not node:
            return
        self._traverse_range(node.left, result, min_rating, max_rating)
        if min_rating <= node.rating <= max_rating:
            result.append((node.buku, node.rating))
        self._traverse_range(node.right, result, min_rating, max_rating)

class bubble_sort:
    @staticmethod
    def sort(data):
        n = len(data)
        for i in range(n):
            for j in range(0, n - i - 1):
                if data[j][2] < data[j + 1][2]:
                    data[j], data[j + 1] = data[j + 1], data[j]
        return data


def bubble_sort_rating(data_list):
    n = len(data_list)
    for i in range(n):
        for j in range(0, n - i - 1):
            if data_list[j][2] < data_list[j + 1][2]:
                data_list[j], data_list[j + 1] = data_list[j + 1], data_list[j]
    return data_list

class RecommendationManager:
    def __init__(self, bst_obj, linked_list_obj):
        self.bst = bst_obj
        self.linked_list = linked_list_obj

    def get_top_rated_books(self, min_rating=4):
        all_books = self.linked_list.get_unique_books_with_max_rating()
        return [book for book in all_books if book[1] >= min_rating]

    def get_books_in_rating_range(self, min_rating=3, max_rating=5):
        return self.bst.get_books_by_rating_range(min_rating, max_rating)

    def get_all_top_books_summary(self):
        all_books = self.linked_list.get_unique_books_with_max_rating()
        return [{"buku": buku, "rating": rating} for buku, rating in all_books]
