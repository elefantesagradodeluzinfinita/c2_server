class Emergency:
    def __init__(self, identifier, timestamp, location, type, status, units, other, map):
        self.identifier = identifier
        self.timestamp = timestamp
        self.location = location
        self.type = type
        self.status = status
        self.units = units
        self.other = other
        self.map = map