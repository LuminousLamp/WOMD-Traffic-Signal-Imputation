import sys
sys.path.append(".")

from src import ScenarioProcessor
from src.utils import read_data
import copy
from src.processor.metrics import has_red_light_running, tlhead_count

if __name__ == "__main__":
    # read example_runcode.py before reading this script snippet

    # read a list of scenario from a specified partition. this function return a list of scenario objects.
    # if scenario_id_set is not specified, all secnarios within this partition are returned
    scenario = read_data("/media/led/LED-WD1T/WOMD/validation/validation.tfrecord-00000-of-00150", )[30] # we get one for example

    # initantiate a ScenarioProcessor
    sp = ScenarioProcessor(scenario)
    # we call .generate_waymonic
    tls_info_in_intersection_format = sp.generate_waymonic_tls(return_data="intersections")
    # note: specify return_data="intersections" will return a list of Intersection, format is "list[list[list[ApproachingLane]]]"
    # the outmost list() refers to a list of signalized intersections in this scenario
    # the middle list() refers to a list of approaches of the intersection (e.g. a typical 4-way intersection has 4 approaches)
    # the inner list() refers to a list of approaching lanes of this approach
    # signal data is encoded there
    
    # check whether there is a red light-running event
    red_light_running_before_imputed: bool = has_red_light_running(tls_info_in_intersection_format, data_type="raw")
    red_light_running_after_imputed: bool = has_red_light_running(tls_info_in_intersection_format, data_type="imputed")
    
    # count the number of traffic light heads before/after imputation
    tlhead_count_raw: int = tlhead_count(tls_info_in_intersection_format, data_type="raw")
    tlhead_count_imputed: int = tlhead_count(tls_info_in_intersection_format, data_type="imputed")
    
    1 - tlhead_count_raw / tlhead_count_imputed # this is the imputation rate for this scenario