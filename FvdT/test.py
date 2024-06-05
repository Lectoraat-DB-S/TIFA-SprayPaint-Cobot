import URCommunication as urc
import Storage as st
import time
import math

# Per connection specifics.
IP_UR = "192.168.0.13"
PORT_RECIEVE = 30022

TOOL_IN = 0
TOOL_FLUSH = 13 
TOOL_OUT = 55


#MeasurementPoses = ["[-0.690796,-1.46479,2.05802,-0.585906,-0.702562,0.0167929]","[-0.755371,-1.43441,2.02297,-0.581487,-0.767256,0.0174955]","[-0.700706,-0.759412,1.32686,-0.6222,0.853325,3.17627]"]
MeasurementPoses = ["[0, 0, 0, 0, 0, 0]","[-27.729700, -91.775535, 129.911666, -251.508110, -65.436018, 107.945137]","[-28.979813, -116.074653, 120.972751, -167.868447, -62.095158, 81.843496]","[-28.979091, -101.342281, 132.159503, -227.846989, -62.096630, 278.157342]"]
#MeasurementPoses = ["[0, 0, 0, 0, 0, 0]","[-27.729700, -91.775535, 129.911666, -251.508110, -65.436018, 107.945137]","[-28.979813, -116.074653, 120.972751, -167.868447, -62.095158, 81.843496]","[-28.979091, -101.342281, 132.159503, -227.846989, -62.096630, 278.157342]"]
#["[-0.483975,-1.6018, 2.2674,-4.3896]"]
def graden_naar_radialen(graden_str):
    # Verwijder de haakjes en split de string naar individuele getallen
    graden = [float(hoek) for hoek in graden_str.strip("[]").split(", ")]
    # Zet de graden om naar radialen
    radialen = [math.radians(hoek) for hoek in graden]
    return radialen

# De gegeven lijst omzetten
MeasurementPoses_radialen = [graden_naar_radialen(poses) for poses in MeasurementPoses]

# De resultaten printen
for i, radialen in enumerate(MeasurementPoses_radialen):
    print(f"MeasurementPoses[{i}] in radialen: {radialen}")

MeasurementPoses = ["[-0.48397456559027163, -1.6017852585292942, 2.267386308451172, -4.389644614968075, -1.142073963494275, 1.2608]","[-0.5057931534622555, -2.0258848729599137, 2.1113728101452627, -2.9298571103595976, -1.083764956646097, 1.738438476542809]", "[-0.5057805521850561, -1.7687564749312916, 2.3066184651493233, -3.9766801488053023, -1.0837906478926864, 4.854761456495909]"]
#MeasurementPoses = ["[-0.48397456559027163, -1.6017852585292942, 2.267386308451172, -4.389644614968075, -1.142073963494275, 1.8839980521663544]","[-0.5057931534622555, -2.0258848729599137, 2.1113728101452627, -2.9298571103595976, -1.083764956646097, 1.428438476542809]", "[-0.5057805521850561, -1.7687564749312916, 2.3066184651493233, -3.9766801488053023, -1.0837906478926864, 4.854761456495909]"]
InbetweenPoses = ["[-1.0023,-1.04478,1.54754,-0.448062,-0.0243877,1.52694]"]

urc.greenLightUR(IP_UR)
write,read = urc.connectReadWrite(IP_UR,PORT_RECIEVE)



# For stability.
def DoCalibration():
    urc.syncWrite("movel("+MeasurementPoses[0]+")",write,read)
    curPose = urc.readWrite("get_actual_tcp_pose()",write,read)
    print(curPose)
    # Take measurement 2: High-Back 2.
    urc.syncWrite("movel("+MeasurementPoses[1]+")",write,read)

    # Take measurement 3: Low-Left.
    urc.syncWrite("movel("+MeasurementPoses[2]+")",write,read)
    #urc.syncWrite("movel("+MeasurementPoses[0]+")",write,read)

    



DoCalibration()

urc.closeReadWrite(write,read)


