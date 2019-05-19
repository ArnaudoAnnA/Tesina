class Simple_counter:
    """class that implements a simple counter with a domain that ranges from min to max"""
    int __value = 0
    int max = 0
    int min = 0
                                    
    def __init__(self, min, max):
        """constructor, sets min and max values. The counter value starts form min"""
        self.__value = min
        self.min = min
        self.max = max
        
    
    def increase(self):
        """if possible, it adds 1 to the counter"""
        if (self.__value < self.max):
            self.__value = self.__value + 1

    
    def decrease(self):
        """ if possible, it removes 1 from the counter"""
        if (self.__value > self.min):
            self.__value = self.__value - 1

    
    def get_value(self):
        """ returns the value of the private propriety value"""
        return self.__value        
                                            
