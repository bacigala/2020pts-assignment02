import unittest
from library_mixed import Reservation

class TestReservation(unittest.TestCase):

    def setUp(self):
        self.res1 = Reservation("2", "4", "book1", "User1")

    def test___init__(self):      
        self.assertEquals(self.res1._from, "2")
        self.assertEquals(self.res1._to, "4")
        self.assertEquals(self.res1._book, "book1")
        self.assertEquals(self.res1._for, "User1")

    def test_overlapping(self):
        self.assertTrue(self.res1.overlapping(Reservation("4", "6", "book1", "User1")))
        self.assertTrue(self.res1.overlapping(Reservation("1", "2", "book1", "User2")))
        self.assertTrue(self.res1.overlapping(Reservation("3", "3", "book1", "User3")))
        self.assertFalse(self.res1.overlapping(Reservation("1", "1", "book1", "User1")))
        self.assertFalse(self.res1.overlapping(Reservation("5", "7", "book1", "User1")))
        self.assertFalse(self.res1.overlapping(Reservation("2", "4", "book2", "User1")))

    def test_includes(self):
        self.assertTrue(self.res1.includes("2"))
        self.assertTrue(self.res1.includes("4"))
        self.assertFalse(self.res1.includes("1"))
        self.assertFalse(self.res1.includes("5"))

    def test_identify(self):
        self.assertTrue(self.res1.identify("2", "book1", "User1"))
        self.assertFalse(self.res1.identify("2", "book2", "User1"))
        self.assertFalse(self.res1.identify("2", "book2", "User2"))
        self.assertFalse(self.res1.identify("1", "book2", "User1"))
        self.assertFalse(self.res1.identify("5", "book2", "User1"))

    def test_change_for(self):
        self.res1.change_for("new_user")
        self.assertEquals(self.res1._for, "new_user")
        self.assertTrue(self.res1.identify("2", "book1", "new_user"))
        self.assertFalse(self.res1.identify("2", "book1", "User1"))

