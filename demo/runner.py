from __future__ import absolute_import
from __future__ import print_function

import os
import sys
import optparse
import random

# import python modules from the $SUMO_HOME/tools directory
if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")

from sumolib import checkBinary  # noqa
import traci  # noqa

routes = ['route01', 'route02', 'route03', 'route04', 'route05', 'route06', 'route07', 'route08', 'route09', 'route10', 'route11', 'route12']
cars = ['CarA', 'CarB', 'CarC', 'CarD']

def run():
    """execute the TraCI control loop"""
    step = 54000
    # we start with phase 2 where EW has green
    # traci.trafficlight.setPhase("0", 2)
    vehID = 0
    random.seed(10)

    traci.vehicle.add("test", "route01", typeID="CarTest", departLane="first", depart="54000")
    # inside simulation
    # while traci.simulation.getMinExpectedNumber() > 0:  # from step 54000 to 56164
    while step < 56000:  # from step 54000 to 56164
        traci.simulationStep()
        # add vehicle
        if step % 5 == 0:
            route = routes[random.randrange(11)]

            typeID = cars[random.randrange(3)]
            traci.vehicle.add(str(vehID), route, typeID=typeID, departLane="first")

        if step % 10 == 0:
            print(traci.vehicle.getLaneIndex("test"))
            traci.vehicle.changeLaneRelative("test", 1, 10)
        vehID += 1
        step += 1

    print("[Event] Finish Simulation")
    traci.close()
    sys.stdout.flush()


def get_options():
    optParser = optparse.OptionParser()
    optParser.add_option("--nogui", action="store_true",
                         default=False, help="run the commandline version of sumo")
    options, args = optParser.parse_args()
    return options


# this is the main entry point of this script
if __name__ == "__main__":
    options = get_options()

    # this script has been called from the command line. It will start sumo as a
    # server, then connect and run
    if options.nogui:
        sumoBinary = checkBinary('sumo')
    else:
        pass
    sumoBinary = checkBinary('sumo-gui')

    # this is the normal way of using traci. sumo is started as a
    # subprocess and then the python script connects and runs
    traci.start([sumoBinary, "-c", "data/demo.sumocfg",
                 "--tripinfo-output", "tripinfo.xml"])
    run()
