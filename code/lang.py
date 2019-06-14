#coding: utf-8

import config
import dictionary_en as dicitonary      #to change lang import a different module

# returns the values of the dict correctly oredered
def dict_values_sorted(dictionary):
    tuples = dictionary.items()
    tuples.sort()
    ret = []
    for item in tuples:
        ret.append(item[1])
    return ret

dictionary = {

    #setting number
    "DISCARDED_VALUE": "",
    "NUMBER_SETTINGS_GUIDE" : "",
    "CONFIRM" : "",

    #setting timer
    "TIMER_SETTINGS_BEGIN" : "",
    # dictionary that associates a progressive id with the number of seconds the exercise will be executed (in both numerical and string value)
    "TIME_DICTIONARY" :{
      0  : "",
      10 : "",
      30 : "",
      60: "",
      120: "",
      180: "" ,
      240: "",
      300: "",
      360: "" ,
      420: "",
      480: "",
      540: "",
      600: ""
    },

    #registration
    "ID_EXERCISE_SETTINGS_BEGIN" : "",
    "SENDING_DATA" : "",
    "REGISTRATION_WILL_START_IN" : "",
    "REGISTRATION_ENDED" : "",

    #feedback 
    "ERROR_FEEDBACK" : "", #sostituire, in seguito, al numero del sensore la sua posizione
    "CORRECT" : "",
    "EXERCISE_DONE_WITH" : "",
    "PERCENTAGE_OF_CORRECTNESS" : "",

    #exercise selection
    "NO_AVAIABLE_EXERCISE" : "",
    "SELECT_THE_EXERCISE" : "",


    #generals
    "YES" : "",
    "NO" : "",
    "SECONDS" : "",
    "GO" : "",
    #sensor positions
    config.SENSORPOSITION_LEGSX : "",
    config.SENSORPOSITION_LEGDX : "",
    config.SENSORPOSITION_ARMSX : "",
    config.SENSORPOSITION_ARMDX : ""
}
  

#upload all the dictionary from a specific language
keys = dicitonary.dictionary.keys()

for key in keys:
    dictionary[key] = dicitonary.dictionary[key] 
