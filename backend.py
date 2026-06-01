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
