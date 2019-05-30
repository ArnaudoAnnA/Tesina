#coding: utf-8

import button_interface as bi

LEFT_BUTTON_PIN     = "L"
CENTRAL_BUTTON_PIN  = "C"
RIGHT_BUTTON_PIN    = "D"

class Button_interface(bi.Button_interface):

    def __init__(self, initial_state):
        self.initial_state = initial_state      #to keep track of the first state of the state machine
        self.state = initial_state
        self.return_value = None
        self.finish = False


    def set_pins_and_start(self):    
        while(self.finish != True):
            lettera = raw_input()

            if(lettera == LEFT_BUTTON_PIN):
                self.left_button_click()
            elif(lettera == CENTRAL_BUTTON_PIN):
                self.central_button_click()
            elif(lettera== RIGHT_BUTTON_PIN):
                self.right_button_click()
                
