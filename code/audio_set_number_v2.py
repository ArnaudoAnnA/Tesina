# -*- coding: utf-8 -*-

#------------------------------------------------------
#Python 2

#IMPORTANT: needs the Rpy.GPIO module
#------------------------------------------------------

import audio_files_ita as audio_files
import RPi.GPIO as GPIO
import threading
import audio_timer
import raspberry_output as output_interface
import config
from abc import ABC, abstractmethod #abstract classes

#constants
LEFT_BUTTON_PIN 	= config.LEFT_BUTTON_PIN
CENTRAL_BUTTON_PIN 	= config.CENTRAL_BUTTON_PIN
RIGHT_BUTTON_PIN 	= config.RIGHT_BUTTON_PIN


class Get_number_from_user:
    """ class that uses an timer object (improprially) to allow user to select a number using buttons"""	
	
    def __init__(self):
        
        self.state = All_off_state()
        self.number_object = audio_timer.Timer(0)
        self.confirm = False
        
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
class Thread_get_number_from_user(Get_number_from_user, threading.Thread):
    """class that makes the method "set_pins_and_start" executed in a new thread"""	

    def __init__(self):
        threading.Thread.__init__(self)
        Get_number_from_user.__init__(self)
        
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
   
   
#-------STATE ALL-OFF(for state design pattern)---------------------------------------------------------------------       
class All_off_state(State):
    """that class is the state of the program before first click on centre button.
    The first click on the centre button start the procedure of selecting number via buttons.
    So, in this phase, if a right or a left button is pressed, I pass"""
    
    def __init__(self):
        super().__init__()
        
        
    
    def central_button_click(self, context):
        """OVERRIDE METHOD from abstract super class.
        Pression on centre button makes the procedure of setting number to start."""
        
        output_interface.output(audio_files.DIRECTORY_PATH, [audio_files.NUMBER_SETTINGS_GUIDE])    #I give in output istructions to the user
        context.number_object = audio_timer.Timer(0)                                                                #I create a new timer object (that I will use impropially)
        context.state = Setting_number_state()                                                                  #I switch the state
        
        
    
    #if left or right button is pressed, I do nothing
    def right_button_click(self, context): pass
    def left_button_click(self, context): pass
    
#-------STATE SETTING_NUMBER(for state design pattern)---------------------------------------------------------------------    
class Setting_number_state(State):
    """that class is the state of the program when user uses left and right button to decrease or increase the number.
    -   if user clicks on right button, the number increase of one unit and then the audio interface tells the new number
    -   if user clicks on left button, the number decrease of one unit and then the audio interface tells the new number
    (NOTE: the class is designed to avoid number goes under 0)
    -   if user clicks on central button, the state machine switches to the confirm-phase """
    
    def __init__(self):
        super().__init__()
        
        
    
    def central_button_click(self, context):
        """OVERRIDE METHOD from abstract super class.
        If user clicks on central button, the state machine switches to the confirm-phase"""
        
        output_interface.output(audio_files.DIRECTORY_PATH, [audio_files.CONFIRM])                  #asking user if he want to confirm the number 
        context.state = Confirm_request_state()   #I switch the state
        
        
    
    def right_button_click(self, context): 
        """OVERRIDE METHOD from abstract super class.
        if user clicks on right button, the number increase of one unit and then the audio interface tells the new number
        (audio_timer object will automatically give new value output on the audio interfaces when it changes)"""
        
        context.number_object.increase(+1)
        
        
            
    def left_button_click(self, context):
        """OVERRIDE METHOD from abstract super class.
        if user clicks on left button, the number increase of one unit and then the audio interface tells the new number
        (audio_timer object will automatically give new value output on the audio interfaces when it changes)"""
        if(context.number_object.value>0):  
            context.number_object.increase(-1)
        
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
        user don't want to confirm current number -> the state returns to all-off and current program restart to allow user to select another number"""
        
        output_interface.output(audio_files.DIRECTORY_PATH, [audio_files.DISCARDED_VALUE])
        context.state = All_off_state()
        
                