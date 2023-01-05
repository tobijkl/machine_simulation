# Simulation the MQTT signal from some kind of machine.
# This is intended for a machine with interdependent sensors.

import random, time, datetime, enum
import paho.mqtt.client as paho

broker = "broker.hivemq.com"
port = 1883
base_topic = "machine_sim"

class MachineStatus(enum.Enum):
    ERROR = 0
    IDLE = 1
    PRODUCTION = 2
    MAINTANANCE = 3

class State:
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
        

# Initializations
s = State(0,0)
sleep_time = 1
last_update = datetime.datetime.now()

client = paho.Client('machine_simulation')
client.connect(broker, port, keepalive=60)


# Run Simulation
while True:
    try:
        now_time = datetime.datetime.now()
        dT = datetime.datetime.now() - last_update
        last_update = now_time
        
        s.update(dT.total_seconds())

        print(s.x, s.y, s.t, s.status, sep="\t")
        
        client.publish(base_topic+"/time", '{}'.format(last_update))
        client.publish(base_topic+"/x", '{}'.format(s.x))
        client.publish(base_topic+"/y", '{}'.format(s.y))
        client.publish(base_topic+"/t", '{}'.format(s.t))
        client.publish(base_topic+"/status", '{}'.format(s.status))

        time.sleep(sleep_time)

    except KeyboardInterrupt:
        break

# Quitting
print("Terminating")
