# -*- coding: utf-8 -*-

#------------------------------------------------------
#Python 2

#IMPORTANT: needs the Rpy.GPIO module
#------------------------------------------------------

import config
import RPi.GPIO as GPIO
import threading
import lang
import vocal_synthesizer as output_interface
from abc import ABCMeta, abstractmethod #abstract classes
from simple_counter import Simple_counter
import time

#constants
LEFT_BUTTON_PIN         = config.LEFT_BUTTON_PIN
CENTRAL_BUTTON_PIN      = config.CENTRAL_BUTTON_PIN
RIGHT_BUTTON_PIN        = config.RIGHT_BUTTON_PIN

MAX_EXERCISE_ID         = config.MAX_EXERCISE_ID

YES                     = lang.dictionary["YES"]
NO                      = lang.dictionary["NO"]
NUMBER_SETTINGS_GUIDE   = lang.dictionary["NUMBER_SETTINGS_GUIDE"]
CONFIRM                 = lang.dictionary["CONFIRM"]
DISCARDED_VALUE         = lang.dictionary["DISCARDED_VALUE"]
DEBOUNCE_TIME           = 1.0


class Button_interface():
    """ class that allows user to select a number or scroll a list using buttons.
        Inital state parameter must be an object that inherits from State abstract class (described in this module).
        When the value is confirmed, the flag finish is putted to true"""  
    
    def __init__(self, initial_state):

        self.initial_state = initial_state      #to keep track of the first state of the state machine
        self.state = initial_state
        self.return_value = None
        self.finish = False
        self.old_time_left = 0
        self.old_time_central = 0
        self.old_time_right = 0
        
        GPIO.setmode(GPIO.BCM)                                              #specifico quale configurazione di pin intendo usare
        
        #PUD_DOWN significa che, se non viene ricevuto nessun segnale da raspberry, l'input del pin è di default 0
        #queste istruzioni sono importanti per evitare errori dovuti a variazioni di tensione, che avvengono anche quando un pin non riceve voltaggio, per motivi fisici
        GPIO.setup(LEFT_BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)     
        GPIO.setup(CENTRAL_BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(RIGHT_BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    # ------- MAIN ---------------------------------------------------------------------------------------------------

    def set_pins_and_start(self):
        """this is the main function. Adds an event listener on each button. 
        Then that functions loops until a number is selected and confirmed by the user.
        Callback functions do different things due to the value of "state" property (state design pattern).
        State classes are following described.
        NOTE: each event listener function is executed by a thread"""

        #aggiungo un event_detect ad ogni pin e associo la relativa funzione che gestirà l'evento click sul bottone
        #ulteriori spiegazioni:  https://sourceforge.net/p/raspberry-gpio-python/wiki/Inputs/
        #SINISTRA
        GPIO.add_event_detect(LEFT_BUTTON_PIN, GPIO.FALLING, callback=self.left_button_click)   #GPIO.FALLING significa che l'evento si scatena nel momento in cui il bottone viene premuto (non quando viene rilasciato)

        #CENTRO
        GPIO.add_event_detect(CENTRAL_BUTTON_PIN, GPIO.FALLING, callback=self.central_button_click)

        #DESTRA
        GPIO.add_event_detect(RIGHT_BUTTON_PIN, GPIO.FALLING, callback=self.right_button_click)

        while(self.finish != True):
            pass
        #print "finished"
        GPIO.remove_event_detect(LEFT_BUTTON_PIN)
        GPIO.remove_event_detect(CENTRAL_BUTTON_PIN)
        GPIO.remove_event_detect(RIGHT_BUTTON_PIN)

    #FUNCTIONS that call corresponding state function
    #Channel is the pin number
    def left_button_click(self, channel):
        now = float(time.time())
        #print(now - self.old_time_left)
        if (now - self.old_time_left > DEBOUNCE_TIME):
            self.old_time_left = now
            self.state.left_button_click(self)
      
    def central_button_click(self, channel):
        now = float(time.time())
        #print(now - self.old_time_central)
        if (now - self.old_time_central > DEBOUNCE_TIME):
            self.old_time_central = now
            self.state.central_button_click(self)
      
    def right_button_click(self, channel):
        now = float(time.time())
        #print(now - self.old_time_right)
        if (now - self.old_time_right > DEBOUNCE_TIME):
            self.old_time_right = now
            self.state.right_button_click(self)
        
        
'''#----THREAD VERSION------------------------------------------------------------------------------------ 
class Button_interface_thread(Button_interface, threading.Thread):
    """class that makes the method "set_pins_and_start" executed in a new thread""" 

    def __init__(self, inital_state):
        threading.Thread.__init__(self)
        Button_interface.__init__(self, inital_state)
        
    def run(self):
        super(Button_interface_thread, self).set_pins_and_start()
        #thread exits when this function returns
'''      
       
       
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
        output_interface.output(self.counter.get_value())
        
        
    
    def central_button_click(self, context):
        """OVERRIDE METHOD from abstract super class.
        If user clicks on central button, the state machine switches to the confirm-phase"""
        
        context.return_value = self.counter.get_value()
        context.state = Confirm_request_state(self.counter.get_value())             #I switch the state
        
        
    
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
    (NOTE: the class is designed to avoid number goes under MIN)
    -   if user clicks on central button, the state machine switches to the confirm-phase """
    
    def __init__(self, list_to_scroll, minimum = 1):
        super(State, self).__init__()
        self.counter = Simple_counter(minimum, len(list_to_scroll)-1)
        self.list_to_scroll = list_to_scroll
        
        list_element = self.list_to_scroll[self.counter.get_value()]
        output_interface.output(list_element)
        
    
    def central_button_click(self, context):
        """OVERRIDE METHOD from abstract super class.
        If user clicks on central button, the state machine switches to the confirm-phase"""
        
        context.return_value = self.counter.get_value()
        context.state = Confirm_request_state(self.list_to_scroll[self.counter.get_value()])             #I switch the state
        
        
    
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
    
    def __init__(self, selected):
        super(State, self).__init__()
        output_interface.output(CONFIRM + " " + str(selected) + "?")
        
        
    
    def central_button_click(self, context):
        pass

    
    
    def right_button_click(self, context): 
        """OVERRIDE METHOD from abstract super class.
        user confirmed current number -> current module can return the selected number and its work is done"""
        output_interface.output(YES)
        context.finish = True
        
        
            
    def left_button_click(self, context):
        """OVERRIDE METHOD from abstract super class.
        user don't want to confirm current number -> the state returns to inital_state to allow user to select another number"""
        
        output_interface.output(NO + ", " + DISCARDED_VALUE)
        context.state = context.initial_state 


#----------------------------------------------------------------------------------------------------------------------------------------------
