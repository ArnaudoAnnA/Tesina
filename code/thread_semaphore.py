
# coding=utf-8
import threading

class Semaphore:

  def __init__(self):
    self.semaphore = threading.Event()

  def lock(self):
    self.semaphore.clear()

  def is_unLocked(self):
    return self.semaphore.isSet()

  def unlock(self):
    self.semaphore.set()

  def wait_for_unlock(self):
    self.semaphore.wait()