# Simulation the OPC UA Server from some kind of machine.
# This is intended for a machine with interdependent sensors.

# Commands to explore the OPC UA server:
# uals --url=opc.tcp://127.0.0.1:4840
# uals --url=opc.tcp://127.0.0.1:4840 --nodeid i=85
# uaread --url=opc.tcp://127.0.0.1:4840 --nodeid "ns=2;i=2"
# uaread --url=opc.tcp://127.0.0.1:4840 --path "0:Objects,2:MyObject,2:MyVariable"

import random, time, datetime, enum
import asyncio
from asyncua import ua, Server
from machine_simluation import Machine

opc_ua_server = "opc.tcp://0.0.0.0:4840"
opc_ua_namespace = "/"

async def main():
    # Initializations
    s = Machine(0,0)
    sleep_time = 1
    last_update = datetime.datetime.now()

    # initialize opc-ua server
    server = Server()
    await server.init()
    server.set_endpoint(opc_ua_server)
    idx = await server.register_namespace(opc_ua_namespace)
    
    # populate namespace
    obj_kinematics = await server.nodes.objects.add_object(idx, "kinematics")
    var_x = await obj_kinematics.add_variable(idx, "x", ua.Variant(s.x, ua.VariantType.Double))
    var_y = await obj_kinematics.add_variable(idx, "y", ua.Variant(s.y, ua.VariantType.Double))
    obj_sensors = await server.nodes.objects.add_object(idx, "sensors")
    var_t = await obj_sensors.add_variable(idx, "t", ua.Variant(s.t, ua.VariantType.Double))
    obj_states = await server.nodes.objects.add_object(idx, "states")
    var_datetime = await obj_states.add_variable(idx, "last update", ua.Variant(last_update, ua.VariantType.DateTime))
    var_status = await obj_states.add_variable(idx, "status", ua.Variant(s.status, ua.VariantType.UInt16))
    
    # run simulation
    async with server:
        while True:
            now_time = datetime.datetime.now()
            dT = datetime.datetime.now() - last_update
            last_update = now_time
    
            # update simulation
            s.update(dT.total_seconds())
            print(s.x, s.y, s.t, s.status, sep="\t")
            
            # update server
            await var_x.write_value(ua.Variant(s.x, ua.VariantType.Double))
            await var_y.write_value(ua.Variant(s.y, ua.VariantType.Double))
            await var_t.write_value(ua.Variant(s.t, ua.VariantType.Double))
            await var_datetime.write_value(ua.Variant(last_update, ua.VariantType.DateTime))
            await var_status.write_value(ua.Variant(s.status.value, ua.VariantType.UInt16))
            
            await asyncio.sleep(0.1)    
                        

if __name__ == "__main__":
    asyncio.run(main(), debug=True)