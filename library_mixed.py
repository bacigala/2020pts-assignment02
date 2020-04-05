from itertools import count

class Logger():
    # Prints all log messages
    def logPrinter(func):
         def inner(self, *args, **kwargs):
             result = func(self, *args, **kwargs)
             print(self.msg)
             return result
         return inner


    # String-constructing decorators for Reservation functions

    def ReservationInit(func):
        @Logger.logPrinter
        def inner(self, *args, **kwargs):
            func(self, *args, **kwargs)
            self.msg = F'Created a reservation with id {self._id} of {self._book} '
            self.msg += F'from {self._from} to {self._to} for {self._for}.'
        return inner

    def ReservationOverlapping(func):
        @Logger.logPrinter
        def inner(self, other):
            result = func(self, other)
            str = 'do'
            if not result:
                str = 'do not'
            self.msg = F'Reservations {self._id} and {other._id} {str} overlap'
            return result
        return inner

    def ReservationIncludes(func):
        @Logger.logPrinter
        def inner(self, date):
            result = func(self, date)
            str = 'includes'
            if not result:
                str = 'does not include'
            self.msg = F'Reservation {self._id} {str} {date}'
            return result
        return inner

    def ReservationIdentify(func):
        @Logger.logPrinter
        def inner(self, date, book, for_):
            result = func(self, date, book, for_)
            if result:
                self.msg = F'Reservation {self._id} is valid {for_} of {book} on {date}.'
            else:
                if book != self._book: 
                    self.msg = F'Reservation {self._id} reserves {self._book} not {book}.'
                elif for_!=self._for:
                    self.msg = F'Reservation {self._id} is for {self._for} not {for_}.'
                elif not self.includes(date):
                    self.msg = F'Reservation {self._id} is from {self._from} to {self._to} which '
                    self.msg += F'does not include {date}.'
            return result
        return inner

    def ReservationChange_for(func):
        @Logger.logPrinter
        def inner(self, for_):
            previous_owner = self._for
            func(self, for_)
            self.msg = F'Reservation {self._id} moved from {previous_owner} to {for_}'
        return inner


    # String-constructing decorators for Library functions

    def LibraryInit(func):
        @Logger.logPrinter
        def inner(self, *args, **kwargs):
            func(self, *args, **kwargs)
            self.msg = F'Library created.'
        return inner

    def LibraryAdd_user(func):
        @Logger.logPrinter
        def inner(self, name):
            result = func(self, name)
            self.msg = F'User {name} created.'
            if not result:
                self.msg = F'User not created, user with name {name} already exists.'
            return result
        return inner

    def LibraryAdd_book(func):
        @Logger.logPrinter
        def inner(self, name):
            func(self, name)
            self.msg = F'Book {name} added. We have {self._books[name]} coppies of the book.'
        return inner

    def LibraryReserve_book(func):
        @Logger.logPrinter
        def inner(self, user, book, date_from, date_to):
            result = func(self, user, book, date_from, date_to)
            if result >= 0:
                self.msg = F'Reservation {result} included.'
            else:
                if user not in self._users: 
                    self.msg = F'We cannot reserve book {book} for {user} from {date_from} to {date_to}. '
                    self.msg += F'User does not exist.'
                elif date_from > date_to:
                    self.msg = F'We cannot reserve book {book} for {user} from {date_from} to {date_to}. '
                    self.msg += F'Incorrect dates.'
                elif self._books.get(book, 0) == 0:
                    self.msg = F'We cannot reserve book {book} for {user} from {date_from} to {date_to}. '
                    self.msg += F'We do not have that book.'
                else:
                   self.msg = F'We cannot reserve book {book} for {user} from {date_from} '
                   self.msg += F'to {date_to}. We do not have enough books.' 
            return result
        return inner

    def LibraryCheck_reservation(func):
        @Logger.logPrinter
        def inner(self, user, book, date):
            result = func(self, user, book, date)
            str = 'exists'
            if not result:
                str = 'does not exist'
            self.msg = F'Reservation for {user} of {book} on {date} {str}.'
            return result
        return inner
    




class Reservation(object):
    _ids = count(0)
    
    @Logger.ReservationInit
    def __init__(self, from_, to, book, for_):
        self._id = next(Reservation._ids)
        self._from = from_
        self._to = to    
        self._book = book
        self._for = for_
        self._changes = 0

    @Logger.ReservationOverlapping
    def overlapping(self, other):
        return (self._book == other._book and self._to >= other._from 
               and self._to >= other._from)

    @Logger.ReservationIncludes
    def includes(self, date):
        return (self._from <= date <= self._to)      

    @Logger.ReservationIdentify        
    def identify(self, date, book, for_):
        if book != self._book: 
            return False
        if for_!=self._for:
            return False
        if not self.includes(date):
            return False
        return True        

    @Logger.ReservationChange_for
    def change_for(self, for_):
        self._for = for_
        

class Library(object):
    @Logger.LibraryInit
    def __init__(self):
        self._users = set()
        self._books = {}   #maps name to count
        self._reservations = [] #Reservations sorted by from

    @Logger.LibraryAdd_user
    def add_user(self, name):
        if name in self._users:
            return False
        self._users.add(name)
        return True

    @Logger.LibraryAdd_book
    def add_book(self, name):
        self._books[name] = self._books.get(name, 0) + 1

    @Logger.LibraryReserve_book
    def reserve_book(self, user, book, date_from, date_to):
        book_count = self._books.get(book, 0)
        if user not in self._users:
            return -1
        if date_from > date_to:
            return -1
        if book_count == 0:
            return -1
        desired_reservation = Reservation(date_from, date_to, book, user)
        relevant_reservations = [res for res in self._reservations
                                 if desired_reservation.overlapping(res)] + [desired_reservation]
        #we check that if we add this reservation then for every reservation record that starts 
        #between date_from and date_to no more than book_count books are reserved.
        for from_ in [res._from for res in relevant_reservations]:
            if desired_reservation.includes(from_):
                if sum([rec.includes(from_) for rec in relevant_reservations]) > book_count:
                    return -1
        self._reservations+=[desired_reservation]
        self._reservations.sort(key=lambda x:x._from) #to lazy to make a getter
        return desired_reservation._id

    @Logger.LibraryCheck_reservation
    def check_reservation(self, user, book, date):
        return any([res.identify(date, book, user) for res in self._reservations])        

    def change_reservation(self, user, book, date, new_user):
        relevant_reservations = [res for res in self._reservations 
                                     if res.identify(date, book, user)]
        if not relevant_reservations:        
            print(F'Reservation for {user} of {book} on {date} does not exist.')
            return False
        if new_user not in self._users:
            print(F'Cannot change the reservation as {new_user} does not exist.')
            return False
            
        print(F'Reservation for {user} of {book} on {date} changed to {new_user}.')        
        relevant_reservations[0].change_for(new_user)
        return True
        
