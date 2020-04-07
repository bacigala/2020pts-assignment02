import unittest
from library_mixed import Reservation
from library_mixed import Logger

class TestLogger(unittest.TestCase):

    def setUp(self):
        self.res1 = Reservation(1, 2, "Book1", "User1")

    def test_ReservationInit(self):      
        self.assertEquals(self.res1.msg, "Created a reservation with id {} of Book1 from 1 to 2 for User1.".format(self.res1._id))

    def test_ReservationOverlapping(self):
        # Overlap with itself
        Logger.ReservationOverlapping(Reservation.overlapping(self.res1, self.res1))
        self.assertEquals(self.res1.msg, 'Reservations {} and {} do overlap'.format(self.res1._id, self.res1._id))
        # Common end-date
        self.res2 = Reservation(2, 3, "Book1", "User2")
        Logger.ReservationOverlapping(Reservation.overlapping(self.res1, self.res2))
        self.assertEquals(self.res1.msg, 'Reservations {} and {} do overlap'.format(self.res1._id, self.res2._id))
        # Common start-date
        self.res2 = Reservation(1, 1, "Book1", "User2")
        Logger.ReservationOverlapping(Reservation.overlapping(self.res1, self.res2))
        self.assertEquals(self.res1.msg, 'Reservations {} and {} do overlap'.format(self.res1._id, self.res2._id))
        # Various books
        self.res2 = Reservation(2, 2, "Book2", "User2")
        Logger.ReservationOverlapping(Reservation.overlapping(self.res1, self.res2))
        self.assertEquals(self.res1.msg, 'Reservations {} and {} do not overlap'.format(self.res1._id, self.res2._id))
        # Various dates
        self.res2 = Reservation(3, 5, "Book1", "User2")
        Logger.ReservationOverlapping(Reservation.overlapping(self.res1, self.res2))
        self.assertEquals(self.res1.msg, 'Reservations {} and {} do not overlap'.format(self.res1._id, self.res2._id))

    def test_ReservationIncludes(self):
        # First date
        Logger.ReservationIncludes(Reservation.includes(self.res1, 1))
        self.assertEquals(self.res1.msg, 'Reservation {} includes 1'.format(self.res1._id))
        # Last date
        Logger.ReservationIncludes(Reservation.includes(self.res1, 2))
        self.assertEquals(self.res1.msg, 'Reservation {} includes 2'.format(self.res1._id))
        # Date before
        Logger.ReservationIncludes(Reservation.includes(self.res1, 0))
        self.assertEquals(self.res1.msg, 'Reservation {} does not include 0'.format(self.res1._id))
        # Date after
        Logger.ReservationIncludes(Reservation.includes(self.res1, 3))
        self.assertEquals(self.res1.msg, 'Reservation {} does not include 3'.format(self.res1._id))

