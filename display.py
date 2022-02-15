from __future__ import annotations
from typing import Tuple, List, Dict

from rich.table import Table, Column
from rich import box

from basic import Track
from teams import Team, Engine
from drivers import Driver
from globals import console
from translation import flags


def new_chassis_values(values: List[Dict]):
    chassis_table = Table("Team", "Old Chassis", "New Chassis", title="Driver Statistics", box=box.SIMPLE)
    for value in values:
        chassis_table.add_row(
            value["team"].text_display, str(int(value["old_chassis"] * 100)), str(int(value["team"].chassis * 100)))
    console.print(chassis_table)


def new_engine_values(values: List[Dict]):
    engine_table = Table(
        "Engine", "Old Power", "New Power", "Old Reliability", "New Reliability",
        title="Driver Statistics", box=box.SIMPLE)
    for value in values:
        engine_table.add_row(
            value["engine"].text_display, str(int(value["old_power"] * 100)), str(int(value["engine"].power * 100)),
            str(int(value["old_reliability"]*100)), str(int(value["engine"].reliability*100)))
    console.print(engine_table)


def join_driver_pool(new_driver: Driver):
    console.print(
        f"Driver joined the pool of drivers: {new_driver.name} {flags[new_driver.nationality]}"
        f" (skill: {int(100 * new_driver.skill)})")


def new_engine_deal(team: Team, engine: Engine, renew: bool=False):
    if renew:
        renew_text = "renew"
    else:
        renew_text = "now"
    console.print(
        f"Team {team.text_display} {renew_text} with engine {engine.text_display} with {int(100 * engine.power)} "
        f"power and {int(100 * engine.reliability)} reliability for {str(team.engine_contract)} years")


def renew_winning_team_engine(winning_team: Team, winning_team_engine: Engine):
    new_engine_deal(winning_team, winning_team_engine, True)


def renew_winning_driver_engine(winning_driver: Driver, winning_driver_engine: Engine):
    renew_winning_team_engine(winning_driver.team, winning_driver_engine)


def driver_change_teams(new_driver: Driver, team: Team, contract: int):
    console.print(
        f"Driver {new_driver.name} {flags[new_driver.nationality]} (skill: {int(100 * new_driver.skill)}) "
        f"now in {team.text_display}  for {team.driver_contracts[contract]} years!")


def retire_driver(driver: Driver):
    console.print(
        f"Driver {driver.name} {flags[driver.nationality]} (skill: {int(100 * driver.skill)}) "
        f"retired at age {driver.age}")


def new_direction(team: Team, old_stats: Tuple[int, int, int, int]):
    new_stats = team.direction.get_stats()
    console.print(
        f"{team.text_display} has a new direction, skill change:\n "
        f"\tOld - avg: {old_stats[0]} (dev: {old_stats[1]}; sct: {old_stats[2]}; eng_sct: {old_stats[3]})\n"
        f"\tNew - avg: {new_stats[0]} (dev: {new_stats[1]}; sct: {new_stats[2]}; eng_sct: {new_stats[3]})")


def race_results(track: Track, driver_performances: List[Tuple[Driver, float]]):
    race_table = Table(
        "Pos", "Driver", "Nat", "Skill", Column("Team", justify="right"), "Engine", "Performance",
        title=f"Results for {track.name} race!", box=box.SIMPLE)
    for idx, d in enumerate(driver_performances):
        if d[1] == -1:
            race_table.add_row(
                "NA", d[0].name, flags[d[0].nationality], str(d[0].skill_100), d[0].team.text_display,
                d[0].team.engine.text_display, str(int(d[1] * 100)))
        else:
            race_table.add_row(
                str(idx + 1), d[0].name, flags[d[0].nationality], str(d[0].skill_100), d[0].team.text_display,
                d[0].team.engine.text_display, str(int(d[1] * 100)))
    console.print(race_table)


def history(history_driver: List[Tuple], history_team: List[Tuple]):
    history_table = Table(
        "Season", "Name", "Age", "Nat", "Skill", Column("Team", justify="right"), "Engine", "S",
        Column("Team", justify="right"), "Engine", "Quality", title="History", box=box.SIMPLE)
    for i in range(len(history_driver)):
        history_table.add_row(
            str(history_driver[i][0]), history_driver[i][1], history_driver[i][3], flags[history_driver[i][6]],
            str(int(100 * float(history_driver[i][2]))), history_driver[i][4], history_driver[i][5],
            str(history_driver[i][0]), history_team[i][1], history_team[i][2],
            str(int(100 * history_team[i][3])))
    console.print(history_table)


def stats(
        drv_stats: List[Tuple[Driver, int]], team_stats: List[Tuple[Team, int]],
        engine_stats: List[Tuple[Engine, int]]):
    driver_stats_table = Table("Pos", "Name", "Nat", "tSkill", "Wins", title="Driver Statistics", box=box.SIMPLE)
    for idx, s in enumerate(drv_stats):
        driver_stats_table.add_row(
            str(idx + 1), s[0].name, flags[s[0].nationality], str(s[0].top_skill_100), str(s[1]))
    console.print(driver_stats_table)

    team_stats_table = Table("Pos", "Name", "Wins", title="Team Statistics", box=box.SIMPLE)
    for idx, s in enumerate(team_stats):
        team_stats_table.add_row(str(idx + 1), s[0].text_display, str(s[1]))
    console.print(team_stats_table)

    engine_stats_table = Table("Pos", "Name", "Wins", title="Engine Statistics", box=box.SIMPLE)
    for idx, s in enumerate(engine_stats):
        engine_stats_table.add_row(str(idx + 1), s[0].text_display, str(s[1]))
    console.print(engine_stats_table)


def season(driver_results: List[Tuple[Driver, int]], team_results: List[Tuple[Team, int]]):
    driver_results_table = Table(
        "Pts", "Name", "Nat", "Skill", Column("Team", justify="right"), "Engine", title="Driver Results",
        box=box.SIMPLE)
    for r in driver_results:
        driver_results_table.add_row(
            str(r[1]), r[0].name, flags[r[0].nationality], str(int(100 * r[0].skill)), r[0].team.text_display,
            r[0].team.engine.text_display)
    console.print(driver_results_table)

    team_results_table = Table(
        "Pts", Column("Team", justify="right"), "Engine",  "Quality", "Direction", title="Team Results", box=box.SIMPLE)
    for r in team_results:
        team_results_table.add_row(
            str(r[1]), r[0].text_display, r[0].engine.text_display, str(r[0].avg_skill_100),
            str(r[0].direction.avg_100))
    console.print(team_results_table)
