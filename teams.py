from typing import List, Optional
import math
import random


class Team:
    def __init__(self):
        self.members = []
        self.name = ""

    def __len__(self):
        return len(self.members)


class TeamsContainer:
    def __init__(self):
        self.teams: List[Team] = []
        self.extras: Optional[Team] = None

    def __len__(self):
        return len(self.teams)


def generate_teams(
    members, size: Optional[int] = None, team_count: Optional[int] = None
) -> TeamsContainer:
    result = TeamsContainer()

    random.shuffle(members)

    if not size:
        size = math.floor(len(members) / team_count)

    team_index = 0
    current_team = Team()
    for m in members:
        if team_count and team_index + 1 > team_count:
            if result.extras is None:
                result.extras = Team()
            result.extras.members.append(m)
            continue

        if len(current_team) < size:
            current_team.members.append(m)
            continue

        # the team is full, check if we should move on
        result.teams.append(current_team)
        current_team = Team()
        team_index += 1

        # If we're over count, the current member belongs in the 'extras'
        if team_count and team_index + 1 > team_count:
            result.extras = Team()
            result.extras.members.append(m)
            continue

        # Otherwise, they're the first member of the next team
        current_team.members.append(m)

    if len(current_team) > 0:
        result.teams.append(current_team)

    return result


def format_teams(t: TeamsContainer) -> str:
    result = ""

    i = 1
    for team in t.teams:
        result += f"Team {i}: {team.name}\n"
        result += "\n".join([m.mention for m in team.members])
        result += "\n\n"
        i += 1

    if t.extras:
        result += f"Extras: {t.extras.name}\n"
        result += "\n".join([m.mention for m in t.extras.members])

    return result
