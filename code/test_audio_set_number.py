import audio_set_number_v2 as audio_get_number_from_user

obj = audio_get_number_from_user.Get_number_from_user()
obj.set_pins_and_start()

while(obj.confirm != True): pass

print ("finito")
