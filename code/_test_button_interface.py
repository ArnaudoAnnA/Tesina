#coding: utf-8

import config
import button_interface as bi
import _test_output as output_interface
from lang import dictionary
from lang import dict_values_sorted

#SELECT TIME
#getting list of all items in time_dictionary (converting dictionary into a list)
time_dictionary = dictionary["time_dictionary"]
list_values = dict_values_sorted(time_dictionary)
print list_values

initial_state = bi.Selecting_from_list_state(list_values)
obj = bi.Button_interface_thread(initial_state)
print("DEBUG:  ", obj)

#starting thread
obj.start()

while(obj.finish!= True): pass

output_interface.output("finito")
