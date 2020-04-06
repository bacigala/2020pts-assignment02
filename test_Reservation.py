import unittest
from library_mixed import Reservation

class TestReservation(unittest.TestCase):

    def test_overlapping(self):
        res1 = Reservation("2", "4", "book1", "User1")
        self.assertTrue(res1.overlapping(Reservation("4", "6", "book1", "User1")))
        self.assertTrue(res1.overlapping(Reservation("1", "2", "book1", "User2")))
        self.assertTrue(res1.overlapping(Reservation("3", "3", "book1", "User3")))
        self.assertFalse(res1.overlapping(Reservation("1", "1", "book1", "User1")))
        self.assertFalse(res1.overlapping(Reservation("5", "7", "book1", "User1")))
        self.assertFalse(res1.overlapping(Reservation("2", "4", "book2", "User1")))
