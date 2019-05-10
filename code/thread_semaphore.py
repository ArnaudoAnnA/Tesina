# coding=utf-8
import threading

class Semaphore:
  
  def __init__(self):
    self.semaphore = threading.Event()
    
  def lock(self):
    self.semaphore.set()
    
  def unlock(self):
    self.semaphore.clear()
