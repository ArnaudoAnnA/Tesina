#test
import ai_functions as ai 
import config as c

print("start")
movement_leg = [-0.32763671875,-0.3330078125,-0.328369140625,-0.334228515625,-0.330322265625,-0.32177734375,-0.330322265625,-0.330078125,-0.315185546875,-0.313232421875,-0.1318359375,-0.137451171875,-0.13427734375,-0.130615234375,-0.1328125,-0.128662109375,-0.132080078125,-0.133056640625,-0.1318359375,-0.131591796875,-0.964599609375,-0.97607421875,-0.96240234375,-0.975341796875,-0.9560546875,-0.9404296875,-0.9541015625,-0.955810546875,-0.96826171875,-0.967529296875,-0.11450381679389313,0.015267175572519083,1.7938931297709924,-1.9541984732824427,-0.4351145038167939,-0.5267175572519084,-0.366412213740458,-0.3511450381679389,-0.3816793893129771,-0.16793893129770993,-0.05343511450381679,-0.08396946564885496,-0.07633587786259542,-0.061068702290076333,-0.05343511450381679,-0.05343511450381679,-0.061068702290076333,-0.061068702290076333,-0.04580152671755725,-0.07633587786259542,1.9389312977099236,-0.007633587786259542,0.05343511450381679,-0.05343511450381679,0.0916030534351145,0.1450381679389313,0.05343511450381679,0.07633587786259542,0.11450381679389313,0.015267175572519083] #1
movement_arm = [-0.271484375,-0.522216796875,-0.62109375,-0.678955078125,-0.770751953125,-0.906494140625,-0.91796875,-0.93310546875,-0.92138671875,-0.748291015625,-0.98681640625,-1.17724609375,-1.22705078125,-0.80322265625,-0.61279296875,-0.583740234375,-0.494384765625,-0.4541015625,-0.273681640625,-0.2509765625,0.6796875,0.393798828125,0.396240234375,0.040771484375,-0.32763671875,-0.293701171875,0.03076171875,0.177490234375,0.261474609375,0.49169921875,-1.7938931297709924,2.595419847328244,-0.5343511450381679,-7.198473282442748,-2.7786259541984735,0.8854961832061069,-1.3893129770992367,-5.137404580152672,-8.34351145038168,-6.801526717557252,8.938931297709924,6.656488549618321,7.778625954198473,9.16793893129771,4.137404580152672,-3.0763358778625953,-5.961832061068702,-6.1679389312977095,-6.404580152671755,-8.84732824427481,-8.053435114503817,-6.580152671755725,-1.183206106870229,1.8473282442748091,0.9847328244274809,1.748091603053435,3.1297709923664123,4.587786259541985,5.6183206106870225,3.7404580152671754] #2
print("2 list created")

aiLeg = ai.TheBrain(c.SENSORPOSITION_LEGSX)
aiLeg.fit_from_csv()
print("leg ai trained")

aiArm = ai.TheBrain(c.SENSORPOSITION_ARMSX)
aiArm.fit_from_csv()
print("arm ai trained")

aiArm.serialize()
aiLeg.serialize()
print("2 ai serialized")

leg = ai.TheBrain(c.SENSORPOSITION_LEGSX)
arm = ai.TheBrain(c.SENSORPOSITION_ARMSX)
print("2 instanced")

leg.deserialize()
arm.deserialize()
print("2 ai deserialized")

(leg_res, leg_res_p) = leg.movement_recognizer(movement_leg)
(arm_res, arm_res_p) = arm.movement_recognizer(movement_arm)

print("LEG: [movement class] " + leg_res + " [affidability] " + leg_res_p[leg_res-1]*100 + "%")
print("ARM: [movement class] " + arm_res + " [affidability] " + arm_res_p[arm_res-1]*100 + "%")
