#moveJ is move joint dus in ronde bewegingen
#moveL is move lineair dus in 1 rechte lijn



from robolink import *    # RoboDK API
from robodk import *    # Robot toolbox
RDK = Robolink()



RDK = Robolink()                    # establish a link with the simulator
robot = RDK.Item('UR10e')           # retrieve the robot by name
robot.setSpeed(8000)               #Set speed of cobot

robot.setJoints([-78.449661, -172.934799, 156.647965, -56.073010, 31.666535, -17.854569])      # set all robot axes to the start position
target = RDK.Item('pHome')        # retrieve the Target item
robot.MoveL(target)
pose = robot.Pose()                         #get the current position of de cobot
z,x,y,a,b,c = Pose_2_KUKA(pose)                  #get the current rotation of the joints

Offset = KUKA_2_Pose ([z, x, y ,a, b, c]) 
robot.MoveL(Offset) 



RDK.setSimulationSpeed(5)         #Set speed of simmulation

def lees_variabelen(bestandsnaam):
    variabelen = {}
    with open(bestandsnaam, 'r') as bestand:
        sleutel = None
        for regel in bestand:
            regel = regel.strip()
            if regel.endswith('='):
                sleutel = regel[:-1]  # Verwijder het '='-teken aan het einde
            else:
                waarde = float(regel) * 1000  # Vermenigvuldig de waarde met 1000
                variabelen[sleutel] = waarde
    return variabelen

bestandsnaam = "C:/Users/jutta/OneDrive - Windesheim Office365/Perron038/DataKozijnGroot.txt"
variabelen = lees_variabelen(bestandsnaam)

# Definieer de variabelen in de huidige scope
globals().update(variabelen)
#min_z=-min_z/10
#max_z=-max_z/10


#Lengte 
x1=max_x-min_x-50
y1=(max_y-min_y)/2
z1=max_z-min_z
d=100 
dh=50 #de helft van de dikte zodat de vervspuit in het midden spuit
RechtsBoven = KUKA_2_Pose ([-min_z+410, max_x+300, max_y+320 ,a, b, c]) 
robot.MoveL(RechtsBoven) 
pose = robot.Pose()                         #get the current position of de cobot
XYZABC = Pose_2_KUKA(pose)                  #get the current rotation of the joints
z,x,y,a,b,c = XYZABC


def voorkant_kozijn():
                  
    pose = robot.Pose()                         #get the current position of de cobot
    XYZABC = Pose_2_KUKA(pose)                  #get the current rotation of the joints
    z,x,y,a,b,c = XYZABC
    LinksBoven = KUKA_2_Pose ([z,x-x1,y,a,b,c])
    robot.MoveL(LinksBoven)

    LinksBoven = KUKA_2_Pose ([z,x-x1,y,a,b-90,c])
    robot.MoveL(LinksBoven)

    LinksOnder = KUKA_2_Pose ([z,x-x1,y-y1,a,b-90,c])
    robot.MoveL(LinksOnder)

    LinksOnder = KUKA_2_Pose ([z,x-x1,y-y1,0,-90,0])
    robot.MoveL(LinksOnder)

    RechtsOnder = KUKA_2_Pose ([z,x,y-y1,0,-90,0])
    robot.MoveL(RechtsOnder)
    RechtsOnder = KUKA_2_Pose ([z,x,y-y1,a,b-90,c])
    robot.MoveL(RechtsOnder)
    RechtsBoven = KUKA_2_Pose ([z, x, y ,a, b-90, c])
    robot.MoveL(RechtsBoven)


def buitenkant_kozijn():
    target = RDK.Item('Buiten')        #beweeg naar homepositie toe waar de assen goed staan om met een hoek van 45 graden te spuiten
    robot.MoveJ(target)

    pose = robot.Pose()                         #get the current position of de cobot
    z,x,y,a,b,c = Pose_2_KUKA(pose)                  #get the current rotation of the joints
    
    RechtsBoven = KUKA_2_Pose ([-min_z+330-d, max_x+300+d, max_y+280+d ,0, 45, 180]) #45 graden op de bovenkant
    robot.MoveL(RechtsBoven) 
    #RechtsBoven = KUKA_2_Pose ([z+min_z, x+max_x, y+max_y ,0, 45, 180]) #45 graden op de bovenkant
    #robot.MoveL(RechtsBoven)

    pose = robot.Pose()                         #get the current position of de cobot
    XYZABC = Pose_2_KUKA(pose)                  #get the current rotation of the joints
    z,x,y,a,b,c = XYZABC
    
 

    LinksBoven = KUKA_2_Pose ([z,x-x1-d*2,y,0,45,180]) #45 graden op de bovenkant
    robot.MoveL(LinksBoven)

    LinksNaastBoven= KUKA_2_Pose ([z,x-x1-d*2,y,45,0,-90])#45 graden op de linkerbuitenkant
    robot.MoveL(LinksNaastBoven)

    LinksNaastOnder= KUKA_2_Pose ([z,x-x1-d*2,y-y1-d*2,45,0,-90])#45 graden op de linker buitenkant
    robot.MoveL(LinksNaastOnder)
    LinksNaastOnder= KUKA_2_Pose ([z,x-x1-d,y-y1-d*2,45,0,-90])#45 graden op de linker buitenkant
    robot.MoveL(LinksNaastOnder)
    LinksOnder = KUKA_2_Pose ([z,x-x1-d,y-y1-d*2,0,-45,0]) #45 graden op de onderkant
    robot.MoveL(LinksOnder)

    RechtsOnder = KUKA_2_Pose ([z,x,y-y1-d*2,0,-45,0])#45 graden op de onderkant
    robot.MoveL(RechtsOnder)

    RechtsNaastOnder= KUKA_2_Pose ([z,x,y-y1-d*2,-45,0,90]) #45 graden op de rechter buitenkant
    robot.MoveL(RechtsNaastOnder)

    RechtsNaastBoven= KUKA_2_Pose ([z,x,y,-45,0,90])  #45 graden op de rechter buitenkant
    robot.MoveL(RechtsNaastBoven)

    RechtsBovenTerug= KUKA_2_Pose ([z+200,x,y,-45,0,90])  #45 graden op de rechter buitenkant
    robot.MoveL(RechtsBovenTerug)



def binnenkant_kozijn():

    target = RDK.Item('Binnen')        # retrieve the Target item
    robot.MoveJ(target)
    
    pose = robot.Pose()                         #get the current position of de cobot
    z,x,y,a,b,c = Pose_2_KUKA(pose)             #set the current position as the base

    #BinnenRechtsBoven = KUKA_2_Pose ([z+min_z, x+max_x, y+max_y ,0, -45, 0]) #45 graden op de boven binnenkant
    #robot.MoveL(BinnenRechtsBoven)
    BinnenRechtsBoven = KUKA_2_Pose ([-min_z+330, max_x+300, max_y+280 ,0, -45, 0]) #45 graden op de boven binnenkant
    robot.MoveL(BinnenRechtsBoven)

    pose = robot.Pose()                         #get the current position of de cobot
    z,x,y,a,b,c = Pose_2_KUKA(pose)             #set the current position as the base

    BinnnenLinksBoven = KUKA_2_Pose ([z, x-x1, y ,0, -45, 0]) #45 graden op de boven binnenkant
    robot.MoveL(BinnnenLinksBoven)

    BinnenLinksNaastBoven= KUKA_2_Pose ([z,x-x1,y,-45,0,90]) #45 graden op de linker binnenkant
    robot.MoveL(BinnenLinksNaastBoven)

    BinnenLinksNaastOnder= KUKA_2_Pose ([z,x-x1,y-y1,-45,0,90])#45 graden op de linker binnenkant
    robot.MoveL(BinnenLinksNaastOnder)

    BinnenLinksOnder = KUKA_2_Pose ([z, x-x1, y-y1 ,0, 45, 180])#45 graden op de onder binnenkant
    robot.MoveL(BinnenLinksOnder)

    BinnenRechtsOnder = KUKA_2_Pose ([z, x, y-y1 ,0, 45, 180])#45 graden op de onder binnenkant
    robot.MoveL(BinnenRechtsOnder)

    BinnenRechtsNaastOnder= KUKA_2_Pose ([z,x,y-y1,-315,0,270])#45 graden op de rechter binnenkant
    robot.MoveL(BinnenRechtsNaastOnder)

    BinnenRechtsNaastBoven= KUKA_2_Pose ([z,x,y,45,0,-90]) #45 graden op de rechter binnenkant
    robot.MoveL(BinnenRechtsNaastBoven)


    
voorkant_kozijn()
#buitenkant_kozijn()
#binnenkant_kozijn()

pose = robot.Pose()                         #get the current position of de cobot
z,x,y,a,b,c = Pose_2_KUKA(pose)             #set the current position as the base
BinnenRechtsNaastBoven= KUKA_2_Pose ([z+300,x,y,a,b,c]) #45 graden op de rechter binnenkant
robot.MoveL(BinnenRechtsNaastBoven)
target = RDK.Item('pHome')
robot.MoveJ(target)