from .models import Request, Accepted_req, Completed_trip, User

class DashinfoClass:
    def __init__(self):
        self.info = {}

    def get_drivercount(self):
        drivers = User.objects.filter(groups__name='driverUser')
        count = drivers.count()
        return count

    def populate_info(self):
        self.info['drivercount'] = self.get_drivercount()
        self.info['tripcount'] = Completed_trip.objects.count()
        self.info['progresscount'] = Accepted_req.objects.count()

    def __getitem__(self, key):
        return self.info[key]

