from __future__ import annotations
import random
import os
from typing import List, Dict

from settings import *


class DriverGenerator:
    def __init__(self):
        self.current_id = 0
        self.name_structure = self.load_names()

    @staticmethod
    def load_names() -> Dict[str, Dict[str, List[str]]]:
        strut = {}

        name_root = "./names"
        dirs = next(os.walk(name_root))[1]

        for nationality in dirs:
            strut[nationality] = {}
            with open(f'{name_root}/{nationality}/first.txt', 'r') as f:
                names = f.read().splitlines()
                strut[nationality]["first"] = names
            with open(f'{name_root}/{nationality}/last.txt', 'r') as f:
                names = f.read().splitlines()
                strut[nationality]["last"] = names

        return strut

    def generate_driver(self) -> Driver:
        nat = random.choice(list(self.name_structure.keys()))
        first_name = random.choice(self.name_structure[nat]["first"])
        last_name = random.choice(self.name_structure[nat]["last"])
        skill = random.random() * 0.59  # TODO Review this
        d = Driver(
            driver_id=self.current_id, first_name=first_name, last_name=last_name, nationality=nat, skill=skill,
            age=random.randint(GEN_MIN_AGE, GEN_MAX_AGE))
        self.current_id += 1

        return d


class Driver:
    def __init__(
            self, driver_id: int, first_name: str, last_name: str, nationality: str, skill: float, form: str='M',
            age: int=20):
        self.id = driver_id
        self.first_name = first_name
        self.last_name = last_name
        self.name = f"{self.first_name} {self.last_name}"
        self.nationality = nationality
        self.base_skill = skill
        self.skill = skill
        self.top_skill = skill
        self.team = None
        self.form = form
        self.age = age

    def age_driver(self):
        self.age += 1
        if self.age <= 25:
            self.base_skill += 0.08 * random.random()
            if self.base_skill > 1:
                self.base_skill = 1
        elif self.age > 30:
            self.base_skill -= 0.08 * random.random()
            if self.base_skill < 0.1:
                self.base_skill = 0.1
        if self.base_skill > self.top_skill:
            self.top_skill = self.base_skill

    def set_skill(self, form: str):
        self.form = form
        if self.form == 'L':
            self.skill = self.base_skill - FORM_CHANGE
            if self.skill < 0:
                self.skill = 0
        elif self.form == ' H':
            self.skill = self.base_skill + FORM_CHANGE
            if self.skill > 1:
                self.skill = 1
        else:
            self.skill = self.base_skill

    def get_base_skill(self) -> int:
        return int(self.base_skill * 100)

    def get_top_skill(self) -> int:
        return int(self.top_skill * 100)

    def get_skill(self) -> int:
        return int(self.skill * 100)

    def __str__(self) -> str:
        return f"[{self.id}] {self.name} ({self.nationality}) - Age: {self.age} - Skill: {self.skill}"
