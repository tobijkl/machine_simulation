import random, enum

class MachineStatus(enum.Enum):
    ERROR = 0
    IDLE = 1
    PRODUCTION = 2
    MAINTANANCE = 3

class Machine:
    v = 0.1

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.t = random.uniform(20, 30)
        self.status = MachineStatus.IDLE

    def update(self, dT):
        if self.status == MachineStatus.PRODUCTION:
            self.x = self.x + self.v * dT
            self.y = self.y + self.v * dT
            self.t = self.t + (random.random()-0.5)
            if random.random() < 0.1:
                self.status = random.choice(list(MachineStatus))
        else:
            if random.random() < 0.2:
                self.status = random.choice(list(MachineStatus))
        