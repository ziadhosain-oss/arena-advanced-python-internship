# Parent Class
class Car:
    def __init__(self, brand, model):
        self.brand = brand
        self.model = model

    def start(self):
        print(f"{self.brand} {self.model} is starting...")

    def drive(self):
        print(f"{self.brand} {self.model} is driving at normal speed.")


# Child Class (Inheritance + Polymorphism)
class SportsCar(Car):
    def __init__(self, brand, model, horsepower):
        super().__init__(brand, model)   # inherit brand & model
        self.horsepower = horsepower

    def drive(self):   # Polymorphism: override drive()
        print(f"{self.brand} {self.model} zooms ahead with {self.horsepower} HP!")


# Create Objects
car1 = Car("Toyota", "Corolla")
car2 = SportsCar("Ferrari", "488 GTB", 660)

# Demonstration
car1.start()   # Parent method
car1.drive()   # Parent drive method

car2.start()   # Inherited method
car2.drive()   # Overridden method (Polymorphism)