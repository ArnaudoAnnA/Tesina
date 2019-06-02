#coding: utf-8



import config
import _test_output as output_interface
import lang


#constants
MINIMUM_PERCENTAGE = config.MINIMUM_CORRECNTESS_PERCENTAGE



#audio
ERROR = lang.dictionary["ERROR_FEEDBACK"]
SENSORS_POSITIONS = lang.dictionary["SENSORS_POSITIONS"]

class Exercise_correctness_observer:
    """class that is notified when an ai object get a result.
    Result is the percentage of correctens with the exercise is executed.
    If that percentage is minor of a certain default percentage, outputs an error.
    That class memrise all result sent by the ai object, so every moment this object
    can retun the average percentage of correctness

    NOTE: 
    All ai objects call notify method on the same ai_observer, so the final
    average percentage of correctness is the medium correctness of all exercise."""

    def __init__(self):
        self.result_sum = 0
        self.n_result = 0


    def notify(self, percentage, sensor_position):
        self.result_sum += percentage
        self.n_result += 1 

        if(percentage<MINIMUM_PERCENTAGE):
            output_interface.output(ERROR + " " + SENSORS_POSITIONS[sensor_position])

            
    def get_correctness_average(self):
        average = 0
        if(self.n_result != 0):
            average = self.result_sum / self.n_result
            
        return average
