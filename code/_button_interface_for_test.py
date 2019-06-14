#coding: utf-8

import config
import RPi.GPIO as GPIO
import threading
import lang
from abc import ABCMeta, abstractmethod #abstract classes
from simple_counter import Simple_counter
import button_interface as bi
import _test_output as output_interface

LEFT_BUTTON_PIN     = "S"
CENTRAL_BUTTON_PIN  = "C"
RIGHT_BUTTON_PIN    = "D"

MAX_EXERCISE_ID = config.MAX_EXERCISE_ID

NUMBER_SETTINGS_GUIDE = lang.dictionary["NUMBER_SETTINGS_GUIDE"]
CONFIRM = lang.dictionary["CONFIRM"]
DISCARDED_VALUE = lang.dictionary["DISCARDED_VALUE"]

class Button_interface(bi.Button_interface):

    def __init__(self, initial_state):
        self.initial_state = initial_state      #to keep track of the first state of the state machine
        self.state = initial_state
        self.return_value = None
        self.finish = False


    def set_pins_and_start(self):    
        while(self.finish != True):
            lettera = str(raw_input("LETTERA: "))

            if(lettera == LEFT_BUTTON_PIN):
                self.left_button_click(self)
            elif(lettera == CENTRAL_BUTTON_PIN):
                self.central_button_click(self)
            elif(lettera== RIGHT_BUTTON_PIN):
                self.right_button_click(self)

                
                
#-------STATE CLASS (for state design pattern)---------------------------------------------------------------------
class State():
    """ABSTRACT CLASS. It defines the interface that all state classes must have"""
    __metaclass__ = ABCMeta
    
    def __init__(self): pass
    
    @abstractmethod
    def central_button_click(self, context): 
        """when user clicks on the centre button that method of the current state is called. """
        pass
     
    @abstractmethod
    def right_button_click(self, context):
        """when user clicks on the right button that method of the current state is called. """
        pass
     
    @abstractmethod    
    def left_button_click(self, context):
        """when user clicks on the left button that method of the current state is called. """
        pass
   

   
#-------STATE SETTING_NUMBER(for state design pattern)---------------------------------------------------------------------    
class Setting_number_state(State):
    """that class is the state of the program when user uses left and right button to decrease or increase the number.
    -   if user clicks on right button, the number increase of one unit and then the audio interface tells the new number
    -   if user clicks on left button, the number decrease of one unit and then the audio interface tells the new number
    (NOTE: the class is designed to avoid number goes under 0)
    -   if user clicks on central button, the state machine switches to the confirm-phase """
    
    def __init__(self):
        super(State, self).__init__()
        self.counter = Simple_counter(0, MAX_EXERCISE_ID)
        output_interface.output(NUMBER_SETTINGS_GUIDE) 
        
        
    
    def central_button_click(self, context):
        """OVERRIDE METHOD from abstract super class.
        If user clicks on central button, the state machine switches to the confirm-phase"""
        
        context.return_value = self.counter.get_value()
        context.state = Confirm_request_state()             #I switch the state
        
        
    
    def right_button_click(self, context): 
        """OVERRIDE METHOD from abstract super class.
        if user clicks on right button, the number increase of one unit and then the audio interface tells the new number"""
        self.counter.increase()
        output_interface.output(self.counter.get_value())
        
        
            
    def left_button_click(self, context):
        """OVERRIDE METHOD from abstract super class.
        if user clicks on left button, the number increase of one unit and then the audio interface tells the new number"""
        self.counter.decrease()
        output_interface.output(self.counter.get_value())
            

#-------STATE SELECTING_FROM_LIST(for state design pattern)---------------------------------------------------------------------    
class Selecting_from_list_state(State):
    """that class is the state of the program when user uses left and right button to decrease or increase the number.
    -   if user clicks on right button, the number increase of one unit and then the audio interface tells the new number
    -   if user clicks on left button, the number decrease of one unit and then the audio interface tells the new number
    (NOTE: the class is designed to avoid number goes under 0)
    -   if user clicks on central button, the state machine switches to the confirm-phase """
    
    def __init__(self, list_to_scroll):
        super(State, self).__init__()
        self.counter = Simple_counter(0, len(list_to_scroll)-1)
        self.list_to_scroll = list_to_scroll
        output_interface.output(NUMBER_SETTINGS_GUIDE) 
        
        
    
    def central_button_click(self, context):
        """OVERRIDE METHOD from abstract super class.
        If user clicks on central button, the state machine switches to the confirm-phase"""
        
        context.return_value = self.counter.get_value()
        context.state = Confirm_request_state()             #I switch the state
        
        
    
    def right_button_click(self, context): 
        """OVERRIDE METHOD from abstract super class.
        if user clicks on right button, the number increase of one unit and then the audio interface tells the new number"""
        self.counter.increase()
        list_element = self.list_to_scroll[self.counter.get_value()]
        output_interface.output(list_element)
        
        
            
    def left_button_click(self, context):
        """OVERRIDE METHOD from abstract super class.
        if user clicks on left button, the number increase of one unit and then the audio interface tells the new number"""
        self.counter.decrease()
        list_element = self.list_to_scroll[self.counter.get_value()]
        output_interface.output(list_element)
            
        
#-------STATE CONFIRM-REQUEST(for state design pattern)---------------------------------------------------------------------  
class Confirm_request_state(State):
    """that class is the state of the program when raspberry is waiting for an user confirm for a selected number.
    -   if user clicks on right button, he will confirm number -> after that the selected number can be returned
    -   if user clicks on left button, he won't confirm number -> after that the state returns to all-off
    -   if user clicks on central button, I do nothing """
    
    def __init__(self):
        super(State, self).__init__()
        output_interface.output(CONFIRM)
        
        
    
    def central_button_click(self, context):
        pass

    
    
    def right_button_click(self, context): 
        """OVERRIDE METHOD from abstract super class.
        user confirmed current number -> current module can return the selected number and its work is done"""
        
        context.finish = True
        
        
            
    def left_button_click(self, context):
        """OVERRIDE METHOD from abstract super class.
        user don't want to confirm current number -> the state returns to inital_state to allow user to select another number"""
        
        output_interface.output(DISCARDED_VALUE)
        context.state = context.initial_state 


#----------------------------------------------------------------------------------------------------------------------------------------------
