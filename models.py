#M.P.Sooriya Bandara  24IT0532 (1 - 31)
class User:
    """
     Base Class 
    
    """
    def __init__(self, name, email, role):
        self.name = name
        self.email = email
        self.role = role  # 'tourist' or 'driver' 


class Tourist(User):
    """
    User class , Tourist Class 
    """
    def __init__(self, name, email, nationality):
        super().__init__(name, email, role="tourist")
        self.nationality = nationality

class Driver(User):
    """
     Driver Class 
    """
    def __init__(self, name, email, vehicle_type, rate_per_km):
        super().__init__(name, email, role="driver")
        self.vehicle_type = vehicle_type
        self.rate_per_km = float(rate_per_km)

from datetime import datetime
