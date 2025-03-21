import sys
sys.path.append(".")

from src import ScenarioProcessor, ScenarioVisualizer
from src.utils import read_data
import copy


# read a list of scenario from a specified partition. this function return a list of scenario objects.
# if scenario_id_set is not specified, all secnarios within this partition are returned
scenario = read_data("/media/led/LED-WD1T/WOMD/validation/validation.tfrecord-00000-of-00150", )[30] # we get one for example

# initantiate a ScenarioProcessor
sp = ScenarioProcessor(scenario)

# plot the map of this scenario to visualize it
sv = ScenarioVisualizer(scenario)
sv.save_map(base_dir=".")

sv.save_video(base_dir=".", video_name="original.mp4")

# call this function to execute imputation and correction of traffic signals, and return the result
# specify "return_data=dymamic_states" to get the result in a format that is the same as how traffic signals are defined in the original scenario object
dynamic_map_states = sp.generate_waymonic_tls(return_data="dynamic_states")

# after that, you can replace the old dynamic_map_states object with the new one
scenario_copied = copy.deepcopy(scenario)
for t in range(91):
    scenario_copied.dynamic_map_states[t].CopyFrom(dynamic_map_states[t])
    
# visualize the result
sv2 = ScenarioVisualizer(scenario_copied)
sv2.save_video(base_dir=".", video_name="new.mp4")