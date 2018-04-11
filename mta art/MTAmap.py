'''
MTA Map
tool for displaing station on NYC MTA
By Alexander McVay
required files:
MTAcords.txt
MTAmap.gif
aditional
MTAMap master.gif
MTAdots.svg
'''
import turtle
IMAGE_REDUCTIONX = 2
IMAGE_REDUCTIONY = 1/.30
imageSize = (625*4/IMAGE_REDUCTIONX,675*4/IMAGE_REDUCTIONY)
dotMatix = []

def setupWindow():
    turtle.setup(imageSize[0]+50, imageSize[1]+50,startx = 0)
    turtle.screensize(canvwidth=imageSize[0], canvheight=imageSize[1],bg = "black")
    turtle.title("MTA Map")
def clearWindow():
    turtle.clearscreen()
def drawMTAMap():
    mapImage = turtle.Turtle()
    image = "MTAMap.gif" # image size 
    
    windowAdj = (int(turtle.screensize()[0]/2),int(turtle.screensize()[1]/2))
    mapImage.goto(imageSize[0]/2-windowAdj[0],imageSize[1]/2-windowAdj[1])
    turtle.addshape(image)
    mapImage.shape(image)
#distance function
def distance(one,two):
    return ((one[0]-two[0])**2 + (one[1]-two[1])**2)**.5
def addToFile(x,y):
    windowAdj = (int(turtle.screensize()[0]/2),int(turtle.screensize()[1]/2))
    print("here",x+windowAdj[0],y+windowAdj[1])
    
    tags=raw_input("add tags:").strip().lower().split(',')
    
    arr = [x+windowAdj[0],y+windowAdj[1]]
    nearest=dotMatix[0][1]
    best = distance(nearest,arr)
    
    for i in dotMatix:
        if distance(i[1],arr)<best:
            nearest = i[1]
            best = distance(i[1],arr)
    print(arr,nearest)
    arr = nearest
    dotPoint(arr,"red",5)
    page =[]
    with open("MTAcords.txt",'r') as f:
        for line in f:
            line = line.strip().split(',')
            if line[0] == str(arr[0]) and line[1] == str(arr[1]):
                print(tags)
                for tag in tags:
                    line.append(tag)
                page.append(",".join(line))                
            else:
                page.append(",".join(line))
    with open("MTAcords.txt",'w') as f:
        for line in page:
            f.write(line+"\n")
    turtle.bye()
    print("bye")
    setupWindow()
    clearWindow()
    drawMTAMap()
#make all points in doc               
def drawAll():
    for i in dotMatix:
        dotPoint(i[1],"black",5)
#translate from cornner to center corners
def dotPoint(loc,color,zise):
    turtle.up()
    windowAdj = (int(turtle.screensize()[0]/2),int(turtle.screensize()[1]/2))
    turtle.setpos(loc[0]-windowAdj[0],loc[1]-windowAdj[1])
    turtle.dot(zise, color)
    
def click(event):
    x, y = event.x, event.y
    windowAdj = (int(turtle.screensize()[0]/2),int(turtle.screensize()[1]/2))
    turtle.setpos(x-windowAdj[0],(y-windowAdj[1]))
    print(x+windowAdj[0],y+windowAdj[1])
    turtle.onscreenclick(lambda x, y: addToFile(x,y))
        
#after init get a point from tags
def getPointfromDotArray(tags):
    

    for i in range(len(dotMatix)):
        match = True
        for tag in tags:
            temp = dotMatix[i][0].replace(" ","")
            if tag not in temp:
                match = False
                break
        if match == True:
            return dotMatix[i][1]
    print("no match",tags)
    '''
    canvas = turtle.getcanvas()
    canvas.bind('<Motion>', click)    
    turtle.done()    
    return None
'''
#search thought tags in dotmatix for x,y
def getLine(tags):
    end = []
    for i in range(len(dotMatix)):
        match = True
        for tag in tags:
            temp = dotMatix[i][0].split(" ")
            if tag not in temp:
                match = False
                break
        if match == True:
            end.append(dotMatix[i][1])
    return end
#train class move ot next close of a list of points
class train():
    def __init__(self,stations):
        self.image = turtle.Turtle()
        self.stopsAll = []
        self.visited = []
        windowAdj = (int(turtle.screensize()[0]/2),int(turtle.screensize()[1]/2))
        for loc in stations:
            self.stopsAll.append((loc[0]-windowAdj[0],loc[1]-windowAdj[1]))
        for i in self.stopsAll:
            self.visited.append(i)
    def nextStop(self):
        
        location = self.image.position()
        best = 0
        for i in range(len(self.visited)):
            if distance(location,self.visited[i]) < distance(location,self.visited[best]):
                best=i
        try:
            location = self.visited.pop(best)
            self.image.goto(location[0],location[1])
        except:
            for i in self.stopsAll:
                self.visited.append(i)
        self.image.down()
    def setPos(self,location):
        self.image.up()
        self.image.goto(location[0],location[1])
        
#dot point class
class datapoint():
    def __init__(self):
        self.loc = [0,0]
        self.size = 3
        self.title1 = ""
        self.title2 = ""
        self.color="black"
        self.GLOBALTAGS = []
    def setTag(self,keys):
        temp = getPointfromDotArray(keys)
        if temp != None:
            self.loc = (int(temp[0]),int(temp[1]))
        return(self.loc)
    def draw(self):
        #print(self.loc)
        dotPoint(self.loc,self.color,self.size)
        if self.title1 != "":
            turtle.seth(45)
            turtle.forward(self.size)
            turtle.write(self.title1.title(),font=("Arial", 14, "normal"))
            turtle.backward(self.size)
        if self.title2 != "":
            turtle.seth(270+45)
            turtle.forward(self.size)
            turtle.write(self.title2.title(),font=("Arial", 14, "normal"))      
    def setColor(self,c):
        self.color = c
    def setSize(self,s):
        self.size = int(s)
    def setLoc(self,l):
        self.loc=l
    def setTitle1(self,text):
        self.title1 = text
    def setTitle2(self,text):
        self.title2 = text
#svg seach        
def getDat(phrase,line):
    startloc = line.index(phrase)
    startloc+=len(phrase)
    quotes = 2
    endloc = startloc
    while quotes>0:
        endloc+=1
        if line[endloc] == '"':
            quotes-=1
    while line[startloc:endloc][0] == '=' or line[startloc:endloc][0] == '"':
        startloc+=1
    
    return line[startloc:endloc]
        

    


#startup  
def initDotArray():
    del dotMatix[:]
    with open("MTAcords.txt") as f:
        next(f)
        for line in f:
            line = line.strip().split(',')
            cords = [int(float(line[0])),int(float(line[1]))]
            tags = []
            for i in range(len(line)):
                if i!=0 and i!=1:
                    tags.append(line[i])
            dotMatix.append((" ".join(tags),cords))
    
    


#svg make
def makeDotArray():
    dotCount = 0
    dotMatix = [] #dot is composed of 3 thing  x,y,color
    #extract svg dots
    with open("MTAdots.svg") as f:
        for l in f:
            line = l.strip()
            if line[0:len("<circle style")] =="<circle style":
                dotCount+=1
                point = [getDat("cx",line),getDat("cy",line)]
                if point not in dotMatix and point[0][0]!="-":
                    dotMatix.append([getDat("cx",line),getDat("cy",line)])
                    
    temp = dotMatix
    dotMatix = []
    
    #round
    for x,y in temp:
        dotMatix.append((int(float(x)+.5)/IMAGE_REDUCTIONX,imageSize[1]-int(float(y)+.5)/IMAGE_REDUCTIONY))

        
    
    #sort list
    dotMatix.sort()
    
    #write to file
    with open("MTAcords.txt",'w') as f:
        f.write("x,y,tags\n")
        for arr in dotMatix:
            line = ""
            for a in arr:
                line += str(a)+","
            line=line[:-1:]
                

            f.write(line+"\n")           
        return 1    
#add tags point in order
def addTags():  
    setupWindow()
    clearWindow()
    drawMTAMap()
    turtle.speed(0)
    turtle.pu()
    dotMatix = []
    
    with open("MTAcords.txt") as f:
        next(f)
        for line in f:
            line = line.strip().split(',')
            temp = [int(float(line[0])),int(float(line[1]))]
            for i in range(len(line)):
                if i!=0 and i!=1:
                    temp.append(line[i])
                    
            dotMatix.append(temp)    
    
    for i in range(len(dotMatix)):
        skip = False

        for j in dotMatix[i][2::]:
            if len(str(j)) == 1:
                skip = True
                break
        if skip == True:
            pass

        dotPoint(dotMatix[i],"red",3)
        name = input("Add a name to the point: ").strip().lower().split(",")
        if name == ["end"]:
            with open("MTAcords.txt",'w') as f:
                f.write("x,y,tags\n")
                for arr in dotMatix:
                    line = ""
                    for a in arr:
                        if str(a) not in line.split(","):
                            line += str(a)+","
                    line=line[:-1:]
                    f.write(line+"\n")   
            return 1
        elif name == [""]:
            continue
            
        for tag in name:
            dotMatix[i].append(tag)
        dotPoint(dotMatix[i],"black",3)        
    with open("MTAcords.txt",'w') as f:
        f.write("x,y,tags\n")
        for arr in dotMatix:
            line = ""
            for a in arr:
                if str(a) not in line:
                    line += str(a)+","
            line=line[:-1:]
            f.write(line+"\n")           
    return 1
    

