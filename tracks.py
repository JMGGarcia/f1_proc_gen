class Track:
    def __init__(self, name: str, downforce_over_engine: float, car_over_driver: float):
        """

        :param name: Name of the track
        :param downforce_over_engine: The importance of the downforce of the car compared to the engine
        :param car_over_driver: The importance of the quality of the car vs the quality of the driver
        (i.e. more or less technical tracks)
        """
        self.name = name
        self.downforce_over_engine = downforce_over_engine
        self.car_over_driver = car_over_driver
