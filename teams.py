from __future__ import annotations

from dataclasses import dataclass, field
from typing import Tuple, List, Optional

from drivers import Driver
from globals import random
from settings import *


# Putting eq to false so that the object is hashable
@dataclass(eq=False)
class Engine:
    name: str
    power: float
    reliability: float
    text_color: str
    text_high: str
    teams: List[Team] = field(init=False)
    value: Optional[float] = field(init=False)

    def __post_init__(self):
        self.teams = []
        self.value = None
        self.update_value()

    @property
    def text_display(self) -> str:
        # return Text(self.name, style=f"{self.text_color} on {self.text_high}")
        return f"[{self.text_color} on {self.text_high}]{self.name}[/]"

    def add_team(self, team: Team):
        self.teams.append(team)

    def remove_team(self, r_team: Team):
        # There's probably a more pythonic way of doing this
        for idx, team in enumerate(self.teams):
            if team.name == r_team.name:
                del self.teams[idx]
                return

    def update_value(self):
        self.value = (self.power + self.reliability) / 2


class Direction:
    def __init__(self):
        self.years = 0
        self.development = random.random()
        self.scouting = random.random()
        self.eng_scouting = random.random()
        self.avg = (self.development + self.scouting + self.eng_scouting) / 3
        self.position_history = []

    @property
    def avg_100(self) -> int:
        return int(self.avg * 100)

    def yearly_update(self, position: int, total_teams: int) -> bool:
        """
        Method to see if direction remains in office
        If not, generate new direction
        If yes, do small updates
        :param position: Position of the team in the championship
        :param total_teams: Number of teams in the championship
        :return:
        """
        if self.years < 2:
            average_position = 0.0
        else:
            self.position_history.append(position)
            if len(self.position_history) > HISTORY_YEARS:
                self.position_history.pop(0)
            average_position = sum(self.position_history) * 1.0 / len(self.position_history)

        if (
                average_position == total_teams and self.years >= 3
        ) or (
                average_position > (total_teams * 3 / 4) and self.years >= 5 and position > (total_teams * 3 / 4)
        ) or (
                average_position > (total_teams / 2) and self.years >= 9 and position > (total_teams / 2)
        ):
            self.years = 0
            self.development = random.random()
            self.scouting = random.random()
            self.eng_scouting = random.random()
            self.avg = (self.development + self.scouting + self.eng_scouting) / 3
            self.position_history = []
            return True

        else:
            self.years += 1

            self.development += random.random() * (2 * YEARLY_CHANGE) - YEARLY_CHANGE
            if self.development < 0:
                self.development = 0
            elif self.development > 1:
                self.development = 1

            self.scouting += random.random() * (2 * YEARLY_CHANGE) - YEARLY_CHANGE
            if self.scouting < 0:
                self.scouting = 0
            elif self.scouting > 1:
                self.scouting = 1

            self.eng_scouting += random.random() * (2 * YEARLY_CHANGE) - YEARLY_CHANGE
            if self.eng_scouting < 0:
                self.eng_scouting = 0
            elif self.eng_scouting > 1:
                self.eng_scouting = 1

            self.avg = (self.development + self.scouting + self.eng_scouting) / 3
            return False

    # TODO improve to be more understandable
    def get_stats(self) -> Tuple[int, int, int, int]:
        return int(self.avg * 100), int(self.development * 100), int(self.scouting * 100), int(self.eng_scouting * 100)


@dataclass(eq=False)
class Team:
    name: str
    drivers: List[Optional[Driver]]
    driver_contracts: List[int, int]  # Represented by the number of years left
    chassis: float  # Represented by a 0-1 float representing the quality
    engine: Engine
    text_color: str
    text_high: str
    engine_contract: int = 3
    direction: Direction = field(init=False)

    def __post_init__(self):
        self.direction = Direction()

    @property
    def avg_skill_100(self) -> int:
        return int(((self.chassis + self.engine.value) / 2) * 100)

    @property
    def text_display(self) -> str:
        # return Text(self.name, justify="right", style=f"{self.text_color} on {self.text_high}")
        return f"[{self.text_color} on {self.text_high}]{self.name}[/]"

    def remove_engine(self):
        engine = self.engine
        self.engine = None
        self.engine_contract = -1
        engine.remove_team(self)

    def is_engine_contract_still_valid(self) -> bool:
        self.engine_contract -= 1
        if self.engine_contract == 0:
            return False
        else:
            return True

    def is_drivers_contracts_still_valid(self) -> Tuple[bool, bool]:
        status = []
        self.driver_contracts[0] -= 1
        if self.driver_contracts[0] == 0:
            status.append(False)
        else:
            status.append(True)
        self.driver_contracts[1] -= 1
        if self.driver_contracts[1] == 0:
            status.append(False)
        else:
            status.append(True)
        return status[0], status[1]
