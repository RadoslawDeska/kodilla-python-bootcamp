class Car:
    def __init__(self, make, model_name, top_speed, color):
        self.make = make
        self.model_name = model_name
        self.top_speed = top_speed
        self.color = color

        # Variables
        self._current_speed = 0

    def __str__(self):
        return f"{self.color} {self.make} {self.model_name}"
    
    def __repr__(self):
        return f"Car(make={self.make}, model={self.model_name}, top_speed={self.top_speed}, color={self.color})"
    
    def __eq__(self, other):
        return all(
            (
            self.make == other.make,
            self.model_name == other.model_name,
            self.top_speed == other.top_speed,
            self.color == other.color
            )
        )
    
    def __gt__(self, other):
        return self.top_speed > other.top_speed

    
    def accelerate(self, step=10):
        self._current_speed += step

    def decelerate(self, step=10):
        self._current_speed -= step
    
    @property
    def current_speed(self):
        return self._current_speed
    
    @current_speed.setter
    def current_speed(self, speed):
        if speed <= self.top_speed:
            self._current_speed = speed
        else:
            raise ValueError(f"Value {speed} exceeds top speed of {self.top_speed}")


class Truck(Car):
   def __init__(self, max_load, *args, **kwargs):
       super().__init__(*args, **kwargs)
       self.max_load = max_load


if __name__ == "__main__":
    # car = Car("Toyota", "Supra", 250, "Red")
    # car2 = Car("Porsche", "911", 350, "Black")

    # print(car.current_speed)
    # car.current_speed = 100
    # print(car.current_speed)

    # print(car == car2)
    # print(car < car2)
    # print(sorted([car2, car], key=lambda car: car.top_speed, reverse=False))
    # print(sorted([car2, car], key=lambda car: car.make, reverse=False))
    
    truck = Truck(make="Mercedes", model_name="Actros", color="Black", top_speed=90, max_load=1200)
    print(truck)
    truck.accelerate()
    print(truck.current_speed)