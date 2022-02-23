from random import choice, randint


def dice(rolls: int, sides: int) -> int:
    return sum(randint(1, sides) for _ in range(rolls))


class Monster:
    """4, 6, 8, 10, 12"""
    monsters = {
        "Goblin": 4,
        "Witch": 4,
        "Druid": 4,
        "Gremlin": 4,
        "Orc": 6,
        "Troll": 8,
        "Golem": 8,
        "Displacer Beast": 8,
        "Giant": 10,
        "Serpent": 10,
        "Elemental": 10,
        "Ogre": 12,
        "Vampire": 12,
        "Dragon": 12,
    }

    def __init__(self):
        self.level = dice(1, 100)
        self.name = choice(list(self.monsters.keys()))
        self.health = dice(self.level, self.monsters[self.name])
        self.offence = dice(1, 100)
        self.defense = dice(1, 100)
        self.balance = dice(1, 100)
        self.rank = self.find_rank()

    def find_rank(self):
        total = sum((self.offence, self.defense, self.balance))
        if 0 < total <= 150:
            rank = "Common"
        elif 150 < total <= 250:
            rank = "Rare"
        elif 250 < total <= 300:
            rank = "Epic"
        else:
            rank = "Unknown"
        return rank

    def __str__(self):
        output = (
            f"Name: {self.name}",
            f"Level: {self.level}",
            f"Health: {self.health}",
            f"Offence: {self.offence}",
            f"Defense: {self.defense}",
            f"Balance: {self.balance}",
            f"Rank: {self.rank}",
        )
        return "\n" + "\n".join(output)


if __name__ == '__main__':
    for _ in range(100):
        print(Monster())
