# Tesina
DESCRIPTION: trousers with sensors that permits recognition of the executed movememt, The objective is to control that the sport exercise will be executed correctly
 
# Used Technologies
- Raspberry Pi
- Random Forest Classifier (AI Algorithm)
- Accelerometer and gyroscope sensor (MPU-6050 https://www.invensense.com/products/motion-tracking/6-axis/mpu-6050/)
- Audio interface
- Python (for all the software)

# Implementation Details
There are two sensors, one positioned on the left wirst and the other one on the left ankle and they are connected to the Raspberry Pi postioned in a pouch lied to the waist.
All the job is managed by the Raspberry Pi, that reads the data coming from the two sensors and instantly execute a control using the Random Forest Classifier, because he needs to understand if the user is executing well the exercise.

Once there will be a protype ready, there will be te possibility to prooced with the right part of the body, that will be identical to the other part, just adding a "simmetry" control.