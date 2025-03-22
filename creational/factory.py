class Car:
    def drive(self): return "Driving a car"

class Truck:
    def drive(self): return "Driving a truck"

class VehicleFactory:
    @staticmethod
    def create_vehicle(vtype):
        if vtype == "car": return Car()
        if vtype == "truck": return Truck()

vehicle = VehicleFactory.create_vehicle("car")
print(vehicle.drive())  # Driving a car