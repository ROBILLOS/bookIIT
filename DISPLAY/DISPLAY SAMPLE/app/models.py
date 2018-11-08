from app import app, psql

class Users(object):
    def __init__(self, room_name=None, college=None, capacity=None, rate=None, equipment=None):
        self.room_name = room_name
        self.college = college
        self.capacity = capacity
        self.rate = rate
        self.equipment = equipment

    @classmethod
    def all(cls):
        cursor = psql.connection.cursor()
        sql = "SELECT room.room_name, room.college, venue.capacity, venue.rate, venue.equipment FROM room, venue WHERE room.room_id=venue.venue_id"
        cursor.execute(sql)
        result = cursor.fetchall()
        return result



