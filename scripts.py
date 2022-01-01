import random
from typing import List, Tuple

from drivers import Driver
from teams import Engine
from teams import Team
from tracks import Track
from globals import driver_generator


def generate_tracks() -> List[Track]:
    tracks = []
    tracks.append(Track("Melbourne", 0.6, 0.8))
    tracks.append(Track("Shanghai", 0.5, 0.8))
    tracks.append(Track("Bahrain", 0.7, 0.8))
    tracks.append(Track("Sochi", 0.3, 0.8))
    tracks.append(Track("Barcelona", 0.6, 0.8))
    tracks.append(Track("Monaco", 0.9, 0.8))
    tracks.append(Track("Montreal", 0.2, 0.8))
    tracks.append(Track("Baku", 0.1, 0.8))
    tracks.append(Track("Spielberg", 0.2, 0.8))
    tracks.append(Track("Silverstone", 0.5, 0.8))
    tracks.append(Track("Budapest", 0.75, 0.8))
    tracks.append(Track("Spa", 0.1, 0.8))
    tracks.append(Track("Monza", 0.1, 0.8))
    tracks.append(Track("Singapore", 0.85, 0.8))
    tracks.append(Track("Kuala Lumpur", 0.35, 0.8))
    tracks.append(Track("Suzuka", 0.6, 0.8))
    tracks.append(Track("Austin", 0.4, 0.8))
    tracks.append(Track("Mexico City", 0.4, 0.8))
    tracks.append(Track("Sao Paulo", 0.25, 0.8))
    tracks.append(Track("Abu Dhabi", 0.65, 0.8))
    return tracks


def generate_engines() -> List[Engine]:
    engines = []
    seat = Engine('SEAT', random.random(), 0.8, "red", "bright_black")
    engines.append(seat)
    nissan = Engine('Chevrolet', random.random(), 0.8, "bright_black", "gold3")
    engines.append(nissan)
    peugeot = Engine('Jaguar', random.random(), 0.8, "gold3", "dark_green")
    engines.append(peugeot)
    audi = Engine('Audi', random.random(), 0.8, "bright_black", "bright_white")
    engines.append(audi)
    toyota = Engine('Toyota', random.random(), 0.8, "red", "bright_white")
    engines.append(toyota)
    ford = Engine('Ford', random.random(), 0.8, "bright_white", "dark_blue")
    engines.append(ford)
    porsche = Engine('Hyundai', random.random(), 0.8, "dark_blue", "bright_white")
    engines.append(porsche)
    bmw = Engine('BMW', random.random(), 0.8, "bright_white", "deep_sky_blue4")
    engines.append(bmw)
    honda = Engine('Honda', random.random(), 0.8, "bright_white", "black")
    engines.append(honda)
    renault = Engine('Renault', random.random(), 0.8, "black", "bright_yellow")
    engines.append(renault)
    merc = Engine('Mercedes', random.random(), 0.8, "black", "white")
    engines.append(merc)
    ferrari = Engine('Ferrari', random.random(), 0.8, "yellow", "red")
    engines.append(ferrari)

    return engines


def populate_world(drivers_pool) -> Tuple[List[Track], List[Engine], List[Team], List[Driver]]:
    tracks = generate_tracks()

    # Engines
    engines = generate_engines()

    # Teams & Drivers
    teams = []

    drivers = [driver_generator.generate_driver() for _ in range(drivers_pool)]

    drv1 = drivers[0]
    drv2 = drivers[1]
    engine = random.choice(engines)
    team = Team(
        'Lucky Strike', [drv1, drv2], [1, 2], random.random()*0.9, engine, "red", "navajo_white1",
        random.randint(1, 5))
    teams.append(team)
    engine.add_team(team)
    drv1.team = team
    drv2.team = team

    drv1 = drivers[2]
    drv2 = drivers[3]
    engine = random.choice(engines)
    team = Team(
        'Marlboro', [drv1, drv2], [1, 2], random.random()*0.9, engine, "bright_white", "red", random.randint(1, 5))
    teams.append(team)
    engine.add_team(team)
    drv1.team = team
    drv2.team = team

    drv1 = drivers[4]
    drv2 = drivers[5]
    engine = random.choice(engines)
    team = Team(
        'Phillip Morris', [drv1, drv2], [1, 2], random.random()*0.9, engine, "dodger_blue1", "bright_white",
        random.randint(1, 5))
    teams.append(team)
    engine.add_team(team)
    drv1.team = team
    drv2.team = team

    drv1 = drivers[6]
    drv2 = drivers[7]
    engine = random.choice(engines)
    team = Team(
        'Chesterfield', [drv1, drv2], [1, 2], random.random()*0.9, engine, "black", "orange1", random.randint(1, 5))
    teams.append(team)
    engine.add_team(team)
    drv1.team = team
    drv2.team = team

    drv1 = drivers[8]
    drv2 = drivers[9]
    engine = random.choice(engines)
    team = Team(
        'Camel', [drv1, drv2], [1, 2], random.random()*0.9, engine, "blue", "yellow3", random.randint(1, 5))
    teams.append(team)
    engine.add_team(team)
    drv1.team = team
    drv2.team = team

    drv1 = drivers[10]
    drv2 = drivers[11]
    engine = random.choice(engines)
    team = Team(
        'Newport', [drv1, drv2], [1, 2], random.random()*0.9, engine, "black", "light_sea_green", random.randint(1, 5))
    teams.append(team)
    engine.add_team(team)
    drv1.team = team
    drv2.team = team

    drv1 = drivers[12]
    drv2 = drivers[13]
    engine = random.choice(engines)
    team = Team(
        'Winston', [drv1, drv2], [1, 2], random.random()*0.9, engine, "dark_blue", "white", random.randint(1, 5))
    teams.append(team)
    engine.add_team(team)
    drv1.team = team
    drv2.team = team

    drv1 = drivers[14]
    drv2 = drivers[15]
    engine = random.choice(engines)
    team = Team(
        'West', [drv1, drv2], [1, 2], random.random()*0.9, engine, "grey78", "dark_red", random.randint(1, 5))
    teams.append(team)
    engine.add_team(team)
    drv1.team = team
    drv2.team = team

    drv1 = drivers[16]
    drv2 = drivers[17]
    engine = random.choice(engines)
    team = Team(
        'Rothmans', [drv1, drv2], [1, 2], random.random()*0.9, engine, "gold3", "navy_blue", random.randint(1, 5))
    teams.append(team)
    engine.add_team(team)
    drv1.team = team
    drv2.team = team

    drv1 = drivers[18]
    drv2 = drivers[19]
    engine = random.choice(engines)
    team = Team(
        'Pall Mall', [drv1, drv2], [1, 2], random.random()*0.9, engine, "white", "green4", random.randint(1, 5))
    teams.append(team)
    engine.add_team(team)
    drv1.team = team
    drv2.team = team

    return tracks, engines, teams, drivers
