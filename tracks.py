from dataclasses import dataclass


@dataclass
class Track:
    name: str
    # The importance of the downforce of the car compared to the engine
    downforce_over_engine: float
    # The importance of the quality of the car vs the quality of the driver (i.e. more or less technical tracks)
    car_over_driver: float
