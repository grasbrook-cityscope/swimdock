# swimdock

## The cityscope stormwater module

### Prerequisites
- a subcatchment.json in the data folder. This is the base-file for the output geojson. Needs to have features with a "Name" property, listing all subcatchments
- a cityPyoUser.json in the app folder. Your cityPyo usercreds

### What does it do?
- Regurlarly checks the stormwater_scenario.json on cityPyo for new scenario hashes
If new scenario:
- Modifies a baseline.inp file according to the scenario
- Computes simulation using swmm 
- Reads simulation result and fills it into a copy of subcatchments.json geojson
- Sends result to cityPyo as <HASH>.json


