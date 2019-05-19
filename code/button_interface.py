# -*- coding: utf-8 -*-

#------------------------------------------------------
#Python 2

#IMPORTANT: needs the Rpy.GPIO module
#------------------------------------------------------

import audio_files_ita as audio_files
import RPi.GPIO as GPIO
import threading
import audio_timer
import vocal_synthesizer as output_interface
import config
from abc import ABCMeta, abstractmethod #abstract classes
from simple_counter import Simple_counter

#constants
LEFT_BUTTON_PIN 	= config.LEFT_BUTTON_PIN
CENTRAL_BUTTON_PIN 	= config.CENTRAL_BUTTON_PIN
RIGHT_BUTTON_PIN 	= config.RIGHT_BUTTON_PIN
MAX_EXERCISE_ID		= config.MAX_EXERCISE_ID


class Button_interface:
    """ class that allows user to select a number or scroll a list using buttons.
        Inital state parameter must be an object that inherits from State abstract class (described in this module)"""	
	
    def __init__(self, inital_state):
        
        self.initial_state = initial_state      #to keep track of the first state of the state machine
        self.state = initial_state
        self.return_value = None
        self.confirm = False

        #init vocal sinthesizer
        output_interface.init()
        
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
        GPIO.add_event_detect(LEFT_BUTTON_PIN, GPIO.RISING)   #GPIO.FALLING significa che l'evento si scatena nel momento in cui il bottone viene premuto (non quando viene rilasciato)
        GPIO.add_event_callback(LEFT_BUTTON_PIN, self.left_button_click )

        #CENTRO
        GPIO.add_event_detect(CENTRAL_BUTTON_PIN, GPIO.RISING)
        GPIO.add_event_callback(CENTRAL_BUTTON_PIN, self.central_button_click )

        #DESTRA
        GPIO.add_event_detect(RIGHT_BUTTON_PIN, GPIO.RISING)
        GPIO.add_event_callback(RIGHT_BUTTON_PIN, self.right_button_click )

        while(self.confirm != True):
            pass
            

    #FUNCTIONS that call corresponding state function
    #Channel is an unused parameter but is required from the GPIO library
    def left_button_click(self, channel):
        self.state.left_button_click(self)
      
    def central_button_click(self, channel):
        self.state.central_button_click(self)
      
    def right_button_click(self, channel):
        self.state.right_button_click(self)  
        
        
#----THREAD VERSION------------------------------------------------------------------------------------	
class Button_interface_thread(Get_number_from_user, threading.Thread):
    """class that makes the method "set_pins_and_start" executed in a new thread"""	

    def __init__(self, inital state):
        threading.Thread.__init__(self)
        Button_interface.__init__(self)
        
    def run(self):
        set_pins_and_start()
        #thread exits when this function returns
        
       
       
#-------STATE CLASS (for state design pattern)---------------------------------------------------------------------
class State(ABC):
    """ABSTRACT CLASS. It defines the interface that all state classes must have"""
    
    def __init__(self):
        super().__init__()
    
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
        self.counter = Simple_counter(0, MAX_EXERCISE_ID)
        output_interface.output(NUMBER_SETTING_GUIDE) 
        
        
    
    def central_button_click(self, context):
        """OVERRIDE METHOD from abstract super class.
        If user clicks on central button, the state machine switches to the confirm-phase"""
        
        output_interface.output(CONFIRM)                    #asking user if he want to confirm the number
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
        self.counter = Simple_counter(0, list_to_scroll.length)
        self.list_to_scroll = list_to_scroll
        output_interface.output(NUMBER_SETTINGS_GUIDE) 
        
        
    
   def central_button_click(self, context):
        """OVERRIDE METHOD from abstract super class.
        If user clicks on central button, the state machine switches to the confirm-phase"""
        
        output_interface.output(CONFIRM)                    #asking user if he want to confirm the number
        context.return_value = self.counter.get_value()
        context.state = Confirm_request_state()             #I switch the state
        
        
    
    def right_button_click(self, context): 
        """OVERRIDE METHOD from abstract super class.
        if user clicks on right button, the number increase of one unit and then the audio interface tells the new number"""
        self.counter.increase()
        list_element = list_to_scroll[self.counter.get_value()]
        output_interface.output(list_element)
        
        
            
    def left_button_click(self, context):
        """OVERRIDE METHOD from abstract super class.
        if user clicks on left button, the number increase of one unit and then the audio interface tells the new number"""
        self.counter.decrease()
        list_element = list_to_scroll[self.counter.get_value()]
        output_interface.output(list_element)
            
        
#-------STATE CONFIRM-REQUEST(for state design pattern)---------------------------------------------------------------------  
class Confirm_request_state(State):
    """that class is the state of the program when raspberry is waiting for an user confirm for a selected number.
    -   if user clicks on right button, he will confirm number -> after that the selected number can be returned
    -   if user clicks on left button, he won't confirm number -> after that the state returns to all-off
    -   if user clicks on central button, I do nothing """
    
    def __init__(self):
        super().__init__()
        
        
    
    def central_button_click(self, context): pass

    
    
    def right_button_click(self, context): 
        """OVERRIDE METHOD from abstract super class.
        user confirmed current number -> current module can return the selected number and its work is done"""
        
        context.confirm = True
        
        
            
    def left_button_click(self, context):
        """OVERRIDE METHOD from abstract super class.
        user don't want to confirm current number -> the state returns to inital_state to allow user to select another number"""
        
        output_interface.output(DISCARDED_VALUE)
        context.state = context.inital_state 


#----------------------------------------------------------------------------------------------------------------------------------------------

