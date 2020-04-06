import unittest
from library_mixed import Library

class TestLibrary(unittest.TestCase):

    def setUp(self):
        self.lib1 = Library()

    def test___init__(self):      
        self.assertEquals(len(self.lib1._users), 0)
        self.assertEquals(len(self.lib1._books), 0)
        self.assertEquals(len(self.lib1._reservations), 0)

    def test_add_user(self):
        self.assertTrue(self.lib1.add_user("User1"))
        self.assertEquals(len(self.lib1._users), 1)
        self.assertEquals(len(self.lib1._books), 0)
        self.assertEquals(len(self.lib1._reservations), 0)
        self.assertTrue(self.lib1.add_user("User2"))
        self.assertFalse(self.lib1.add_user("User1"))
        self.assertEquals(len(self.lib1._users), 2)

    def test_add_book(self):
        self.lib1.add_book("Book1")
        self.assertEquals(len(self.lib1._books), 1)
        self.assertEquals(self.lib1._books.get("Book1", 0), 1)
        self.lib1.add_book("Book1")
        self.assertEquals(len(self.lib1._books), 1)
        self.assertEquals(self.lib1._books.get("Book1", 0), 2)

    def test_reserve_book(self):
        self.assertFalse(self.lib1.reserve_book("User1", "Book1", 1, 5))
        self.assertTrue(self.lib1.add_user("User1"))
        self.assertFalse(self.lib1.reserve_book("User1", "Book1", 1, 5))
        self.lib1.add_book("Book1")
        self.assertFalse(self.lib1.reserve_book("User1", "Book2", 1, 5))
        self.assertFalse(self.lib1.reserve_book("User2", "Book1", 1, 5))
        self.assertFalse(self.lib1.reserve_book("User1", "Book1", 3, 2))
        self.assertTrue(self.lib1.reserve_book("User1", "Book1", 1, 5))
        self.assertFalse(self.lib1.reserve_book("User1", "Book1", 1, 5))
        self.assertTrue(self.lib1.add_user("User2"))
        self.assertTrue(self.lib1.reserve_book("User2", "Book1", 6, 7))

    def test_check_reservation(self):
        self.assertFalse(self.lib1.check_reservation("User1", "Book1", 1))
        self.assertTrue(self.lib1.add_user("User1"))
        self.lib1.add_book("Book1")
        self.assertTrue(self.lib1.reserve_book("User1", "Book1", 1, 5))
        self.assertFalse(self.lib1.check_reservation("User1", "Book1", 0))
        self.assertFalse(self.lib1.check_reservation("User1", "Book1", 6))
        self.assertTrue(self.lib1.check_reservation("User1", "Book1", 1))
        self.assertTrue(self.lib1.check_reservation("User1", "Book1", 5))
        self.assertTrue(self.lib1.reserve_book("User1", "Book1", 7, 7))
        self.assertTrue(self.lib1.check_reservation("User1", "Book1", 7))
        self.assertFalse(self.lib1.check_reservation("User1", "Book1", 6))
        self.assertFalse(self.lib1.check_reservation("User1", "Book1", 8))

    def test_change_reservation(self):
        self.assertFalse(self.lib1.change_reservation("User1", "Book1", 1, "User2"))
        self.assertTrue(self.lib1.add_user("User1"))
        self.lib1.add_book("Book1")
        self.assertTrue(self.lib1.reserve_book("User1", "Book1", 1, 5))
        self.assertFalse(self.lib1.change_reservation("User1", "Book1", 1, "User2"))
        self.assertTrue(self.lib1.add_user("User2"))
        self.assertFalse(self.lib1.check_reservation("User2", "Book1", 1)) 
        self.assertTrue(self.lib1.change_reservation("User1", "Book1", 1, "User2"))
        self.assertFalse(self.lib1.check_reservation("User1", "Book1", 1))
        self.assertFalse(self.lib1.check_reservation("User1", "Book1", 5))
        self.assertTrue(self.lib1.check_reservation("User2", "Book1", 1))

