#coding: utf-8
import exercise_correctness_observer as co

observer = co.Exercise_correctness_observer()
for i in range(0, 10):
    percentage = i*10
    print("percentage: "+ str(percentage))
    observer.notify(percentage, "legsx")

print("average: " + str(observer.get_correctness_average()))    
