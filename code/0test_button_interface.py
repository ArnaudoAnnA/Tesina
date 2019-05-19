#coding: utf-8

import button_interface as bi
import phrases_en as phrases

#SELECT TIME
#getting list of all items in time_dictionary (converting dictionary into a list)
time_dictionary = phrases.time_dictionary
list_values = [v for v in time_dictionary values()] 

initial_state = bi.Selecting_from_list_state(list_values)
obj = bi.Button_interface_thread(bi.Selecting_from_list_state)

while(obj.confirm != True): pass

output_interface.output("finito")
