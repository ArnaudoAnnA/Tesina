# coding=utf-8
import threading

class Semaphore:
  
  def __init__(self):
    self.semaphore = threading.Event()
    
  def unlock(self):
    self.semaphore.clear()
    
  def waitForUnlock(self)
    self.semaphore.wait()
