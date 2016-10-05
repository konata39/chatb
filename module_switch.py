"""
This class is for building and return a task handler
based on the task's domain.
"""
import medicine.medicine as medicine
#import hotel.hotel as hotel

class Switch(object):

    def __init__(self, console):
        self.console = console

    def get_handler(self, domain):
        print(domain)
        handler = None
        if domain == "病症":
            handler = medicine.MedicalListener(self.console)
        if domain == "住宿":
            handler = hotel.HotelListener(self.console)
        else:
            pass
        """

        """
        return handler
