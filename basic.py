from __future__ import annotations
from operator import itemgetter
from typing import Tuple, List

from drivers import Driver
import display
from globals import random, driver_generator, console
import scripts
from settings import *
from teams import Team, Engine
from tracks import Track


class Race:
    def __init__(self, track: Track):
        self.track = track

    def perform_race(self, teams: List[Team]) -> List[Tuple[Driver, float]]:
        driver_performances = []

        Tr_CoD = self.track.car_over_driver
        Tr_DoE = self.track.downforce_over_engine
        for team in teams:
            performance_car = (Tr_DoE * team.chassis + (1 - Tr_DoE) * team.engine.power) / 2
            for driver in team.drivers:
                if random.random() > team.engine.reliability:
                    performance_driver = -1
                else:
                    performance_driver = Tr_CoD * performance_car + (1 - Tr_CoD) * driver.skill
                    random_factor = random.random()
                    performance_driver = random_factor * RACE_RANDOMNESS + (1 - RACE_RANDOMNESS) * performance_driver
                driver_performances.append(
                    (driver, performance_driver))

        driver_performances = sorted(driver_performances, key=itemgetter(1), reverse=True)

        if PRINT_RACE:
            display.race_results(self.track, driver_performances)

        return driver_performances


class Season:
    def __init__(self, tracks: List[Track], teams: List[Team], name: str):
        self.name = name
        self.tracks = tracks
        self.teams = teams
        self.points = RACE_POINTS
        self.classification_driver = {}
        self.classification_team = {}
        self.sorted_driver_results = None
        self.sorted_team_results = None

        for team in teams:
            self.classification_team[team] = 0
            for driver in team.drivers:
                self.classification_driver[driver] = 0

    def run_season(self):
        if STOP_PER_SEASON:
            stopornot = input(" ")
        for track in self.tracks:
            race = Race(track)
            results = race.perform_race(self.teams)

            if STOP_PER_RACE:
                stopornot = input(" ")

            for idx, performance in enumerate(results):
                if performance[1] != -1 and idx < len(self.points):
                    self.update_points(results[idx][0], self.points[idx])
                else:
                    break

        driver_results = self.classification_driver.items()
        driver_results = sorted(driver_results, key=itemgetter(1), reverse=True)
        team_results = self.classification_team.items()
        team_results = sorted(team_results, key=itemgetter(1), reverse=True)

        if PRINT_SEASON:
            display.season(driver_results, team_results)

        if STOP_PER_RACE:
            stopornot = input(" ")

        self.sorted_driver_results = driver_results
        self.sorted_team_results = team_results

    def update_points(self, driver: Driver, points: int):
        self.classification_driver[driver] = self.classification_driver[driver] + points
        self.classification_team[driver.team] = self.classification_team[driver.team] + points


class World:
    def __init__(self, n_seasons: int):
        self.tracks, self.engines, self.teams, self.drivers = scripts.populate_world(DRIVERS_POOL)
        self.n_seasons = n_seasons

    def run_world(self):
        history_driver = []
        history_team = []
        statistics_driver = {}
        statistics_team = {}
        statistics_engine = {}

        for n_season in range(self.n_seasons):
            console.rule(f"[bold red]Season {n_season + 1}")
            s = Season(self.tracks, self.teams, "Season " + str(n_season))

            s.run_season()
            winning_driver = s.sorted_driver_results[0][0]
            team_results = s.sorted_team_results
            winning_team = team_results[0][0]

            # --- Driver operations and statistics ---
            statistics_driver[winning_driver] = statistics_driver.get(winning_driver, 0) + 1
            statistics_engine[winning_driver.team.engine] = \
                statistics_engine.get(winning_driver.team.engine, 0) + 1

            # --- Team operations and statistics ---
            statistics_team[winning_team] = statistics_team.get(winning_team, 0) + 1

            history_driver.append(
                (n_season + 1, winning_driver.name, "%.2f" % winning_driver.top_skill, str(winning_driver.age),
                 winning_driver.team.get_text(), winning_driver.team.engine.get_text(), winning_driver.nationality))

            history_team.append(
                (n_season+1,
                 winning_team.get_text(),
                 winning_team.engine.get_text(),
                 winning_team.direction.avg))

            # --- World updates ---
            self.update_directions(team_results)
            self.age_drivers()
            self.tweak_chassis_engine()
            self.teams_pick_engines(team_results, winning_driver, winning_team)
            self.teams_pick_drivers(team_results)
            self.tweak_driver_form()

        # --- After run statistics ---
        console.rule(f"[bold red]Final Statistics")
        drv_stats = statistics_driver.items()
        drv_stats = sorted(drv_stats, key=itemgetter(1), reverse=True)
        team_stats = statistics_team.items()
        team_stats = sorted(team_stats, key=itemgetter(1), reverse=True)
        engine_stats = statistics_engine.items()
        engine_stats = sorted(engine_stats, key=itemgetter(1), reverse=True)

        # --- Print world results
        if PRINT_RUN:
            display.history(history_driver, history_team)

        if PRINT_STATS:
            display.stats(drv_stats, team_stats, engine_stats)

    def update_directions(self, team_results: List[Tuple[Team, int]]):
        total_teams = len(self.teams)
        for idx, team_result in enumerate(team_results, 1):
            team = team_result[0]
            old_stats = team.direction.get_stats()
            new_direction = team.direction.yearly_update(idx, total_teams)
            if new_direction:
                display.new_direction(team, old_stats)
                team.remove_engine()

    def age_drivers(self):
        for driver in self.drivers:
            driver.age_driver()

    def tweak_chassis_engine(self):
        changelog_chassis = []
        changelog_engine = []
        revolution = False  # Tech revolution that can change the quality of cars a lot
        random_factor = 0.3
        if random.random() < REVOLUTION_PROBABILITY:
            revolution = True

        for team in self.teams:
            old_chassis = team.chassis
            if revolution:
                team.chassis = (1 - REVOLUTION_EFFECT) * team.chassis + REVOLUTION_EFFECT * random.random()
            value = random.random() * random_factor - (random_factor / 2) + team.direction.development * \
                TEAM_DEVELOPMENT_INFLUENCE
            team.chassis += value
            team.chassis = min(1, max(0, team.chassis))
            changelog_chassis.append({"team": team, "old_chassis": old_chassis})

        if PRINT_CHASSIS_ENGINE_UPDATES or (PRINT_CHASSIS_ENGINE_REVOLUTIONS and revolution):
            display.new_chassis_values(changelog_chassis)

        for engine in self.engines:
            old_power = engine.power
            old_reliability = engine.reliability
            if revolution:
                engine.power = (1 - REVOLUTION_EFFECT) * engine.power + REVOLUTION_EFFECT * random.random()
            value = random.random() * random_factor - (random_factor / 2)
            engine.power += value
            engine.power = min(1, max(0, engine.power))

            if revolution:
                engine.reliability -= random.random() * 0.2 + 0.3
            engine.reliability += random.random() * 0.1 + 0.05

            engine.reliability = min(MAXIMUM_RELIABILITY, max(MINIMUM_RELIABILITY, engine.reliability))

            engine.update_value()

            changelog_engine.append({"engine": engine, "old_power": old_power, "old_reliability": old_reliability})

        if PRINT_CHASSIS_ENGINE_UPDATES or (PRINT_CHASSIS_ENGINE_REVOLUTIONS and revolution):
            display.new_engine_values(changelog_engine)

    def tweak_driver_form(self):
        for team in self.teams:
            for driver in team.drivers:
                value = random.random()
                if value < 0.33:
                    driver.set_skill('L')
                elif value > 0.66:
                    driver.set_skill('H')
                else:
                    driver.set_skill('M')

    def take_out_driver_from_team(self, team: Team, idx: int):
        driver = team.drivers[idx]
        team.drivers[idx] = None
        team.driver_contracts[idx] = -1
        driver.team = None
        if driver.age > 38 or (driver.age > 30 and random.random() < 0.2):
            if PRINT_DRIVER_UPDATES:
                display.retire_driver(driver)
            self.retire_driver(driver)

    def teams_pick_drivers(self, team_results: List[Tuple[Team, int]]):
        for team in self.teams:
            drv1_valid, drv2_valid = team.is_drivers_contracts_still_valid()
            if not drv1_valid:
                self.take_out_driver_from_team(team, 0)
            if not drv2_valid:
                self.take_out_driver_from_team(team, 1)

        for team_result in team_results:
            team = team_result[0]

            team_perception = None
            for idx, driver in enumerate(team.drivers):
                if driver is None:
                    if not team_perception:
                        team_perception = self.compute_driver_perception(team)
                    new_driver = team_perception.pop(0)
                    team.drivers[idx] = new_driver
                    team.driver_contracts[idx] = self.engine_contract_years()
                    new_driver.team = team
                    if PRINT_DRIVER_UPDATES:
                        display.driver_change_teams(new_driver, team, idx)

    def compute_driver_perception(self, team):
        driver_list = [driver for driver in self.drivers if driver.team is None]
        scouting_value = SCOUTING_TRUE_FACTOR + team.direction.scouting * (1 - SCOUTING_TRUE_FACTOR)
        perception_list = []
        for driver in driver_list:
            perception = driver.skill * scouting_value + random.random() * (1 - scouting_value)
            perception_list.append(perception)

        return [driver for _, driver in sorted(zip(perception_list, driver_list), key=lambda d: d[0], reverse=True)]

    def teams_pick_engines(self, team_results: List[Tuple[Team, int]], winning_driver: Driver, winning_team: Team):
        winning_driver_engine = winning_driver.team.engine
        winning_team_engine = winning_team.engine

        # Deprecate contracts
        for team in self.teams:
            if not team.is_engine_contract_still_valid():
                engine = team.engine
                team.engine = None
                engine.remove_team(team)

        # Winning drivers' team and winning team always keep engines (loyalty)
        if winning_driver.team.engine is None:
            winning_driver.team.engine = winning_driver_engine
            winning_driver_engine.add_team(winning_driver.team)
            winning_driver.team.engine_contract = self.engine_contract_years()
            if PRINT_ENGINE_CHANGES:
                display.renew_winning_driver_engine(winning_driver, winning_driver_engine)

        if winning_team.engine is None:
            winning_team.engine = winning_team_engine
            winning_team_engine.add_team(winning_team)
            winning_team.engine_contract = self.engine_contract_years()
            if PRINT_ENGINE_CHANGES:
                display.renew_winning_team_engine(winning_team, winning_team_engine)

        # Pick engine, priority for highest classified team
        for team_result in team_results:
            team = team_result[0]
            if team.engine is None:
                team_perception = self.compute_engine_perception(team)
                for engine in team_perception:
                    if len(engine.teams) < MAX_TEAMS_PER_ENGINE:
                        team.engine = engine
                        engine.add_team(team)
                        team.engine_contract = self.engine_contract_years()
                        if PRINT_ENGINE_CHANGES:
                            display.new_engine_deal(team, engine)
                        break

    def compute_engine_perception(self, team: Team) -> List[Engine]:
        engine_list = self.engines
        scouting_value = SCOUTING_TRUE_FACTOR + team.direction.eng_scouting * (1 - SCOUTING_TRUE_FACTOR)
        perception_list = []
        for engine in engine_list:
            perception = engine.value * scouting_value + random.random() * (1 - scouting_value)
            perception_list.append(perception)

        return [engine for _, engine in sorted(zip(perception_list, engine_list), key=lambda e: e[0], reverse=True)]

    @staticmethod
    def engine_contract_years() -> int:
        contract_years_value = random.random()
        if contract_years_value < 0.02:
            return 2
        elif contract_years_value < 0.2:
            return 3
        elif contract_years_value < 0.8:
            return 4
        elif contract_years_value < 0.95:
            return 5
        else:
            return 6

    def generate_driver(self):
        new_driver = driver_generator.generate_driver()
        self.drivers.append(new_driver)
        if PRINT_DRIVER_UPDATES:
            display.join_driver_pool(new_driver)

    def retire_driver(self, driver: Driver):
        for idx, d in enumerate(self.drivers):
            if d.name == driver.name:
                del self.drivers[idx]
                self.generate_driver()
                return
        raise Exception("Did not retire driver")


def script():
    world = World(NUMBER_OF_SEASONS)
    world.run_world()


if __name__ == '__main__':
    script()
