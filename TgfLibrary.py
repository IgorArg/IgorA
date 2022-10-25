from tgfInit import *

def GetRealRoutes(type="UPM"):
   allCommand=tgf.getAllComponents()
   tempArrayOfCommand=[]
   realRoutes=[]
   for command in allCommand:
      if command[0]==type:
         count=0
         while count<len(command):
            if len(command[count])<3:
               command.pop(count)
            else:
               count+=1
         tempArrayOfCommand.append(command)
   arrayOfObjects=tgf.getLogicalNamesofType("SIGNAL") + tgf.getLogicalNamesofType("POINT") + tgf.getLogicalNamesofType("SHSIGNAL")+ tgf.getLogicalNamesofType("VSIGNAL")
   for command in tempArrayOfCommand:
      
      LogObjCount=1
      for obj in command:
         if arrayOfObjects.count(obj):
            LogObjCount+=1
      count=0
      print len(command)
      if LogObjCount<>len(command):
         print "continue"
         continue
      else:
         count=2
         SIGcount=0
         while count<len(command):
            if tgf.getLogicalType(command[count]) == "SIGNAL" or tgf.getLogicalType(command[count]) == "SHSIGNAL" or tgf.getLogicalType(command[count]) == "VSIGNAL":
                 SIGcount+=1
            count+=1
         if SIGcount<2:
            realRoutes.append(command)
   return realRoutes

def borderStageITI(StartLB):
   print StartLB
   if (tgf.getLogicalType(StartLB)=="HELPBLOCK_R4" or tgf.getLogicalType(StartLB)=="HELPBLOCK" or tgf.getLogicalType(StartLB)=="SALB" or tgf.getLogicalType(StartLB)=="SALB_E"):
      leg=tgf.getLogicalNeighbourLeg(StartLB, "0")
   elif tgf.getLogicalType(StartLB) in ("SIGNAL", "AB_R4"):
      leg=tgf.getLogicalNeighbourLeg(StartLB, "0")
      LineNext=tgf.getLogicalNeighbour(StartLB, "0")
   elif tgf.getLogicalType(StartLB) in ("ENDBLOCK", "HELPBLOCK"):
      return StartLB
   else:
      leg=tgf.getLogicalNeighbourLeg(StartLB, "1")
      LineNext=tgf.getLogicalNeighbour(StartLB, "1")
   while (tgf.getLogicalType(LineNext) not in ("LINEBLOCK", "HELPBLOCK_R4", "HELPBLOCK", "SALB","SALB_E", "ENDBLOCK", "LINEBLOCK2000","SHSIGNAL", "POINT","SECTION")):
      if leg=="0":
         leg=tgf.getLogicalNeighbourLeg(LineNext, "1")
         LineNext=tgf.getLogicalNeighbour(LineNext, "1")
         continue
      if leg=="1":
         leg=tgf.getLogicalNeighbourLeg(LineNext, "0")
         LineNext=tgf.getLogicalNeighbour(LineNext, "0")
   return LineNext 

def listOfLine(StartLB, Count=2):
   RevCount=0
   arrayOfLineN=[]
   arrayOfLineI=[]
   LineNext=tgf.getLogicalNeighbour(StartLB, "1")
   if tgf.getLogicalType(LineNext)=="HELPBLOCK":
      return arrayOfLineN
   while (tgf.getLogicalType(LineNext) != "LINEBLOCK"):  
      if tgf.getLogicalType(LineNext) == "LINE" and tgf.getLogicalNeighbourLeg(LineNext, "0")== "0":
         arrayOfLineI.append(LineNext)
         LineNext=tgf.getLogicalNeighbour(LineNext, "0")
         break
      if tgf.getLogicalType(LineNext) == "LINE" and tgf.getLogicalNeighbourLeg(LineNext, "1")== "0" and RevCount==0:
            arrayOfLineN.append(LineNext)
            LineNext=tgf.getLogicalNeighbour(LineNext, "1")
            
      else:
         if tgf.getLogicalType(LineNext) == "LINE" and tgf.getLogicalNeighbourLeg(LineNext, "1")== "1" and RevCount==0:
               arrayOfLineN.append(LineNext)
               LineNext=tgf.getLogicalNeighbour(LineNext, "1")
               RevCount+=1
         if tgf.getLogicalType(LineNext) == "LINE" and tgf.getLogicalNeighbourLeg(LineNext, "0")== "1" and RevCount==1:     
            arrayOfLineI.append(LineNext)
            LineNext=tgf.getLogicalNeighbour(LineNext, "0")
         if tgf.getLogicalType(LineNext) == "LNLX" and tgf.getLogicalNeighbourLeg(LineNext, "0")== "1" and RevCount==1:
            LineNext=tgf.getLogicalNeighbour(LineNext, "0")   
         if tgf.getLogicalType(LineNext) == "LNLX" and tgf.getLogicalNeighbourLeg(LineNext, "1")== "0" and RevCount==0:
            LineNext=tgf.getLogicalNeighbour(LineNext, "1")
         if tgf.getLogicalType(LineNext) == "LNLX" and tgf.getLogicalNeighbourLeg(LineNext, "1")== "1" and RevCount==0:
               LineNext=tgf.getLogicalNeighbour(LineNext, "1")
               RevCount+=1 
         if tgf.getLogicalType(LineNext) == "BRIDGE" and tgf.getLogicalNeighbourLeg(LineNext, "0")== "1" and RevCount==1:
            LineNext=tgf.getLogicalNeighbour(LineNext, "0") 
         if tgf.getLogicalType(LineNext) == "BRIDGE" and tgf.getLogicalNeighbourLeg(LineNext, "1")== "0" and RevCount==0:
            LineNext=tgf.getLogicalNeighbour(LineNext, "1") 
   if Count==0:                 
      return arrayOfLineN
   elif Count==1:                 
      return arrayOfLineI
   else:
      return arrayOfLineN+arrayOfLineI

def SearchPos(point, pos, ArrayOfRoute, data=""):
   RouteWithPoint=[]
   for TempRoute in ArrayOfRoute:
      for ObjInRoute in TempRoute:
         if ObjInRoute==point:
            RouteWithPoint.append(TempRoute)
   for Route in RouteWithPoint:
      Maneuvres=GetManeuvres(Route,data)
      count=1
      #print Maneuvres
      while count<len(Maneuvres):
          if Maneuvres[count]==pos and Maneuvres[count-1]==point:
             return Route
          count+=2
   return "0"

def CheckRoute(command,M_R_E=""):
   if command[0] in ("UMM", "UMB"):
     M_R_E="M_R_E=2"
   elif command[0] in ("UPM","UPB"):
     M_R_E="M_R_E=1"
   elif command[0] in ("UMD"):
     M_R_E="M_R_E=3"
   maneuvres=GetManeuvres(command)
   if maneuvres.count(M_R_E)==0:
      return("ERROR "+M_R_E + " in Route " + ' '.join(command)+"\n")
   NextObj=tgf.getLogicalNeighbour(command[1], "1")
   leg=tgf.getLogicalNeighbourLeg(command[1], "1")
   lastObject=""
   lastLeg=leg
   count=0
   while count<len(maneuvres):
      if maneuvres[count]==M_R_E:
         lastObject=maneuvres[count-1]
      count+=1
   print  lastObject
   if command[0] in ("UPM","UPB") and tgf.getLogicalType(lastObject) in ("LINEBLOCK", "LINEBLOCK2000", "SALB", "SALB_E", "ABTCE","ENDBLOCK"):
      return "OK"
   if command[0] in ("UMM","UMB","UMD") and tgf.getLogicalType(lastObject) == ("ENDBLOCK"):
      return "OK"
   if tgf.getLogicalType(lastObject)!="SECTION":
      return("ERROR end of route " + ' '.join(command)+"\n")
   if tgf.getListofLogicalIbits(tgf.getLogicalNamesofType("SECTION")[0]).count("I_ER0")!=0:
      while NextObj!=lastObject and tgf.getLogicalType(NextObj)not in ("ENDBLOCK","HELPBLOCK_R4", "HELPBLOCK", "SALB", "SALB_E","ABTCE"):
         if leg=="0":
            if tgf.getLogicalType(NextObj)=="POINT":
               count=0
               if maneuvres.count(NextObj)==0:
                  return(NextObj + " not in route: " + ' '.join(command)+"\n")
               while count<len(maneuvres):
                  if maneuvres[count]=="M_SW=1" and maneuvres[count-1]==NextObj:
                     leg=tgf.getLogicalNeighbourLeg(NextObj, "1")
                     NextObj=tgf.getLogicalNeighbour(NextObj, "1")
                     break
                  elif  maneuvres[count]=="M_SW=2" and maneuvres[count-1]==NextObj:
                     leg=tgf.getLogicalNeighbourLeg(NextObj, "2")
                     NextObj=tgf.getLogicalNeighbour(NextObj, "2")
                     break
                  count+=1
            else:        
                leg=tgf.getLogicalNeighbourLeg(NextObj, "1") 
                NextObj=tgf.getLogicalNeighbour(NextObj, "1")
         else:
            leg=tgf.getLogicalNeighbourLeg(NextObj, "0")
            NextObj=tgf.getLogicalNeighbour(NextObj, "0")
         if tgf.getLogicalType(NextObj)=="SECTION":
            lastLeg=leg
      if tgf.getLogicalType(NextObj)!="SECTION":
         return("ERROR end of route " + ' '.join(command)+"\n")
   if tgf.getListofLogicalIbits(tgf.getLogicalNamesofType("SECTION")[0]).count("I_ER0")!=0:
      if tgf.getLogicalIbitValue(lastObject, "I_ER"+lastLeg)=="0" and command[0] in ("UMM","UMB","UMD"):
         
         return("ERROR I_ER"+lastLeg+"=0 in "+ lastObject+".  Route " + ' '.join(command)+"\n")
      elif tgf.getLogicalIbitValue(lastObject, "I_ER"+lastLeg)!="2" and command[0] in ("UPM","UPB"):
         return("ERROR I_ER"+lastLeg+"<>2 in "+ lastObject+".  Route " + ' '.join(command)+"\n")
   else:
      if tgf.getLogicalIbitValue(lastObject, "I_ER")=="0": 
         if tgf.getLogicalIbitValue(lastObject, "I_ER"+lastLeg)=="0" and command[0] in ("UMM","UMB","UMD"):
            return("ERROR I_ER=0 in "+ lastObject+".  Route " + ' '.join(command)+"\n")
         elif tgf.getLogicalIbitValue(lastObject, "I_ER"+lastLeg)!="2" and command[0] in ("UPM","UPB"):
            return("ERROR I_ER<>2 in "+ lastObject+".  Route " + ' '.join(command)+"\n")
   return "OK"       
def GetManeuvres(Route, data=""):
   if data=="":
      dataFile=open(sys.argv[4], "r")
      comTable=dataFile.read()
      dataFile.close()
      comTable=comTable.replace(" ","")
   else:
      comTable=data
   count=1
   RouteStr=Route[0]+"||"
   while count<len(Route):
      RouteStr+=Route[count] + "|"
      count+=1
   #RouteStr=RouteStr[0:-1]
   FirstIndex=comTable.index(RouteStr)
   TempComTable=comTable[FirstIndex:]
   FirstIndex=TempComTable.index("Mainobjects")
   EndIndex=TempComTable.index("Component")
   TempComTable=TempComTable[FirstIndex:EndIndex]
   FirstIndex=TempComTable.index(".=====")
   EndIndex=TempComTable.rfind(".=====")
   TempComTable=TempComTable[FirstIndex:EndIndex]
   TempComTable=TempComTable.split("\n")
   TempComTable=TempComTable[3:-1]
   count=0
   outArray=[]
   while count<len(TempComTable):
      temp=TempComTable[count].split("|")
      outArray.append(temp[2])
      outArray.append(temp[3])
      count+=1
   return outArray

def PointTrailing(Point, LogicalType="SIGNAL", leg="2"):
   NextObj=Point
   if leg=="2":
      NextObj=tgf.getLogicalNeighbour(Point, "2")
   while (tgf.getLogicalType(NextObj) not in ("LINEBLOCK", "HELPBLOCK_R4", "HELPBLOCK", "SALB","SALB_E", "ENDBLOCK", "LINEBLOCK2000")):
      if leg=="0":
         leg=tgf.getLogicalNeighbourLeg(NextObj, "1")
         NextObj=tgf.getLogicalNeighbour(NextObj, "1")
         continue
      if leg=="1" or leg=="2":
         if tgf.getLogicalType(NextObj)==LogicalType:
            return NextObj
         leg=tgf.getLogicalNeighbourLeg(NextObj, "0")
         NextObj=tgf.getLogicalNeighbour(NextObj, "0")
   return "0"    

def PointSection(Point, ArrayOfSection=tgf.getLogicalNamesofType("SECTION")):
   SectionArray=[]
   for Section in ArrayOfSection:
      if tgf.getLogicalStatus2IPU(Point, "C_TC")==tgf.getLogicalStatus2IPU(Section, "C_TC"):
         SectionArray.append(Section)
   if len(SectionArray)>0:
      SectionArray.sort()
      return SectionArray[0]
   else:
      return "0"

def GetMappedStatusLO(IPUobj, Check="C_TC", ArrayOfLogicalObjects=tgf.getLogicalNamesofType("SECTION")):
   for LogicalObject in ArrayOfLogicalObjects:
       if tgf.getListofLogicalStatus(LogicalObject).count(Check)!=0:
          if tgf.getLogicalStatus2IPU(LogicalObject, Check)==IPUobj:
             return LogicalObject
   return ""

def CheckCommand(ManeuvresArray, Obj, Maneuvre, POK="M_CC=3"):
   countM_M=0
   countM_CC=0
   count=1
   while count<len(ManeuvresArray):
      if ManeuvresArray[count]==Maneuvre and  ManeuvresArray[count-1]==Obj:
         countM_M+=1
      if ManeuvresArray[count]==POK and  ManeuvresArray[count-1]==Obj:
         countM_CC+=1
      count+=1
   if countM_M<>1 or countM_CC<>1:
      return(Obj)  
   else:
      return "OK" 


def CheckCommandFunc(allCommand, Mnem, Obj ,Maneuvre, POK="M_CC=3", VObjArray=[]):
   ErrorObj=[]
   hasCommand=0
   for command in allCommand:
      if command[0]==Mnem and command[1]==Obj:
         count=0
         hasCommand+=1
         while count<len(command):
            if len(command[count])<2:
               command.pop(count)
            else:
               count+=1
         ManeuvresArray=GetManeuvres(command)
         Check=CheckCommand(ManeuvresArray, Obj, Maneuvre, POK)
         if Check!="OK":
            ErrorObj.append(Check)         
         for VObj in VObjArray:
            Check=CheckCommand(ManeuvresArray, VObj, Maneuvre, POK)
            if Check!="OK":
               ErrorObj.append(Obj)
   if hasCommand<>1:
      ErrorObj.append(Obj)
   return ErrorObj



       
def GetSection(Object, Check="C_TC", ArrayOfSection=tgf.getLogicalNamesofType("SECTION")):
   SectionArray=[]
   for Section in ArrayOfSection:
      if len(tgf.getLogicalStatus2IPU(Object, Check))>2 and tgf.getLogicalStatus2IPU(Object, Check)==tgf.getLogicalStatus2IPU(Section, "C_TC"):
         print Section
         SectionArray.append(Section)
   if len(SectionArray)>0:
      SectionArray.sort()
      return SectionArray[0]
   else:
      for Order in tgf.getLogicalOrderFW(Section):
         if tgf.getLogicalOrderFW(Order)[0] in ("OFW_TCS", "OFW_TC") and tgf.getLogicalOrderFW(Order)[1]==Object and tgf.getLogicalOrderFW(Order)[0]==Check:
            return Section
      return "0"

def StraightRoute(ArrayOfRoute):
   dataFile=open(sys.argv[4], "r")
   comTable=dataFile.read()
   dataFile.close()
   RoutesArray=[]

   for Route in ArrayOfRoute:
      
      count=1
      pointCounter=0
      RouteStr=Route[0]+"   || "
      while count<len(Route):
         RouteStr+=Route[count] + " | "
         count+=1
      RouteStr=RouteStr[0:-1]
      FirstIndex=comTable.index(RouteStr)
      TempComTable=comTable[FirstIndex:]
      FirstIndex=TempComTable.index("Main objects")
      EndIndex=TempComTable.index("Component")
      TempComTable=TempComTable[FirstIndex:EndIndex]
      PointInRoute=Route[2:-1]
      for point in PointInRoute:
         FirstIndex=TempComTable.index(point+" ")
         PointString=TempComTable[FirstIndex:FirstIndex+50]
         if PointString.find("M_SW = 2")!=-1 and tgf.getLogicalIbitValue(point, "I_DIST")=="0":
            pointCounter+=1
      if pointCounter==0:
         RoutesArray.append(Route)
   if len(RoutesArray)==0:
      return "0"
   else:
      return RoutesArray
