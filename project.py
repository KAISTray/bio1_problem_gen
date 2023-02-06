import random
import turtle

# const
male = True
female = False

def ReLU(x):
    if (x >= 0):
        return x
    else:
        return 0

# description / notes

# Person class : Id(Int), Sex(Boolean), Genes(List), Mother(Person)
# Father(Person), Spouse(Person), Children(Set(Person))
# Family class : Set(Person) //Hh, Tt, ABO, etc..

class Problem:
    def testFunc():
        print("hi")

class ProblemT1(Problem):
    def __init__(self, answerTree, problems, hints):
        self.answer = answerTree # as Family
        self.problem = problems # 질문 형식은 추후 고려해보겠습니다..
        self.hint = hints

class Person:
    def __init__(self, numId, boolSex):
        self.id = numId
        self.sex = boolSex
        self.genes = []
        self.mother = None
        self.father = None
        self.spouse = None
        self.children = set()

class Family:
    def __init__(self):
        self.members = set()

    def add(self, human):
        self.members.add(human)

    def marriage(self, person1, person2):
        if (person1.sex != person2.sex):
            person1.spouse = person2
            person2.spouse = person1
            childs = person1.children | person2.children
            person1.children = childs
            person2.children = childs

    def baby(self, father, mother, child):
        father.children.add(child)
        mother.children.add(child)

    def babies(self, father, mother, children): #list input!
        father.children.update(children)
        mother.children.update(children)
        
    def find(self, ident):
        for person in list(self.members):
            if (person.id == ident):
                return person
        return None

################################ Helper Function For Turtle Drawing Module ################################

class DrawPartition:
    def __init__(self, headleft, tailright):
        self.head = headleft[1]
        self.left = headleft[0]
        self.tail = tailright[1]
        self.right = tailright[0]
        self.width = self.right - self.left
        self.height = self.head - self.tail
    
    def AABBCollision(partA, partB):
        a = partA
        b = partB
        (ar, al, at, ab) = (a.right, a.left, a.head, a.tail)
        (br, bl, bt, bb) = (b.right, b.left, b.head, b.tail)
        
        if (ar > bl and br > al and at > bb and bt > ab):
            return True
        else:
            return False

    def centerAlign(partition, curx, cury, width, height, alignOption = "center", returnOption = ("center", "center")):
        # alignOption : vertical, horizontal, center
        # returnOption : (_, _) : ({left, right, center/middle}, {top/head, bottom/tail, center/middle})
        (pr, pl, pt, pb) = (partition.right, partition.left, partition.head, partition.tail)

        cx = (pr + pl) / 2
        cy = (pt + pb) / 2

        if (alignOption == "vertical"):
            cy = cury
        elif (alignOption == "horizontal"):
            cx = curx
        
        (rx, ry) = (cx, cy)

        if (returnOption[0] == "left"):
            rx = cx - width / 2
        elif (returnOption[0] == "right"):
            rx = cx + width / 2
        
        if (returnOption[1] == "top" or returnOption[1] == "head"):
            ry = cy + height / 2
        elif (returnOption[1] == "bottom" or returnOption[1] == "tail"):
            ry = cy - height / 2
        
        return (rx, ry)

def drawline(turtlebot, centerCoord, xs, ys, dir, len):
    turtlebot.penup()
    turtlebot.goto(xs + centerCoord[0], ys + centerCoord[1])
    turtlebot.setheading(dir)
    turtlebot.pendown()
    turtlebot.forward(len)
    turtlebot.penup()

def writeTxt(turtlebot, centerCoord, xs, ys, ffont, txt):
    ys = ys - ffont[1] * 0.75
    # what value shit the fuck
    turtlebot.penup()
    turtlebot.goto(xs + centerCoord[0], ys + centerCoord[1])
    turtlebot.pendown()
    turtlebot.write(txt, move=False, align = "center", font = ffont)
    turtlebot.penup()

def drawShape(turtlebot, shapeType = "circle", center = (0, 0), radius = 1, opt = 0):
    # option 0 : just shape
    # option 1 : right-up hatched
    # option 2 : left-up hatched
    # option 3 : X-cross hatched
    # option 4 : horizontal hatched
    # option 5 : vertical hatched
    # option 6 : filled_black
    # option 7 : filled_gray
    # shapeType = {circle, square, triangle}
    turtlebot.penup()
    turtlebot.goto(center[0], center[1])
    turtlebot.setheading(0)
    turtlebot.pendown()
    if (opt == 6):
        turtlebot.begin_fill()
        turtlebot.color("black")
    elif (opt == 7):
        turtlebot.begin_fill()

    if (shapeType == "circle"):
        turtlebot.penup()
        turtlebot.goto(center[0], center[1] - radius)
        turtlebot.pendown()
        turtlebot.circle(radius)
        turtlebot.penup()
        turtlebot.goto(center[0], center[1])
    elif (shapeType == "square"):
        radius = radius * 2
        turtlebot.penup()
        turtlebot.goto(center[0] - (radius / 2), center[1] - (radius / 2))
        turtlebot.pendown()
        for _ in range(4):
            turtlebot.forward(radius)
            turtlebot.left(90)
    
    turtlebot.penup()

    if (opt == 7):
        turtlebot.color("gray")

    if (opt == 6 or opt == 7):
        turtlebot.end_fill()
        turtlebot.color("black")
    
    if (opt == 1 and shapeType == "circle"):
        for i in range(15):
            h = (i - 7) * radius / 5
            d = (2 * (radius ** 2) - (h ** 2)) ** 0.5
            xs = -0.5 * (h + d)
            ys = xs + h
            
            drawline(turtlebot, center, xs, ys, 45, d * (2 ** 0.5))

    elif (opt == 2 and shapeType == "circle"):
        for i in range(15):
            h = (i - 7) * radius / 5
            d = (2 * (radius ** 2) - (h ** 2)) ** 0.5
            xs = -0.5 * (- h + d)
            ys = -xs + h

            drawline(turtlebot, center, xs, ys, -45, d * (2 ** 0.5))

    elif (opt == 3 and shapeType == "circle"):
        for i in range(15):
            h = (i - 7) * radius / 5
            d = (2 * (radius ** 2) - (h ** 2)) ** 0.5
            xs = -0.5 * (h + d)
            ys = xs + h
            
            drawline(turtlebot, center, xs, ys, 45, d * (2 ** 0.5))

            h = (i - 7) * radius / 5
            d = (2 * (radius ** 2) - (h ** 2)) ** 0.5
            xs = -0.5 * (- h + d)
            ys = -xs + h

            drawline(turtlebot, center, xs, ys, -45, d * (2 ** 0.5))

    elif (opt == 4 and shapeType == "circle"):
        for i in range(15):
            h = (i - 7) * radius / 8
            d = ((radius**2) - (h**2))**0.5
            xs = -d
            ys = h

            drawline(turtlebot, center, xs, ys, 0, 2 * d)

    elif (opt == 5 and shapeType == "circle"):
        for i in range(15):
            h = (i - 7) * radius / 8
            d = ((radius**2) - (h**2))**0.5
            xs = h
            ys = -d
            
            drawline(turtlebot, center, xs, ys, 90, 2 * d)

    elif (opt == 1 and shapeType == "square"):
        for i in range(15):
            h = (i - 7) * radius / 8
            d = abs(radius - h)
            xs = ReLU(-h) - (radius / 2)
            ys = xs + h
            drawline(turtlebot, center, xs, ys, 45, d * (2 ** 0.5))

    elif (opt == 2 and shapeType == "square"):
        for i in range(15):
            h = (i - 7) * radius / 8
            d = abs(radius - h)
            xs = ReLU(h) - (radius / 2)
            ys = -xs + h
            drawline(turtlebot, center, xs, ys, -45, d * (2 ** 0.5))

    elif (opt == 3 and shapeType == "square"):
        for i in range(15):
            h = (i - 7) * radius / 8
            d = abs(radius - h)
            xs = ReLU(-h) - (radius / 2)
            ys = xs + h
            drawline(turtlebot, center, xs, ys, 45, d * (2 ** 0.5))
            xs = ReLU(h) - (radius / 2)
            ys = -xs + h
            drawline(turtlebot, center, xs, ys, -45, d * (2 ** 0.5))

    elif (opt == 4 and shapeType == "square"):
        for i in range(15):
            h = (i - 7) * radius / 16
            d = radius
            xs = -radius / 2
            ys = h
            drawline(turtlebot, center, xs, ys, 0, d)

    elif (opt == 5 and shapeType == "square"):
        for i in range(15):
            h = (i - 7) * radius / 16
            d = radius
            xs = h
            ys = -radius / 2
            drawline(turtlebot, center, xs, ys, 90, d)

    return

def normalizeRadius(shapeType, originRadius):
    return originRadius

###########################################################################################################

def genProblem(type):
    if (type == 1):
        print("temp")
    else:
        print("tempp")


def familyTreeGen():
    familyT = Family()
    # 랜덤 인수 :
    # 친가 2세대 자식이 몇명인가? leftN
    # 외가 2세대 자식이 몇명인가? rightN
    # 친가 2세대 중 누가 결혼할것인가? (id value로) leftP
    # 외가 2세대 중 누가 결혼할것인가? (id value로) rightP
    # 대립유전형질은 3종류 (Aa, Bb, Dd)
    # 상염색체 개수 (numberA), 성염색체 개수 (numberS)
    # ABO 나옴? isABOProblem
    # 

    leftN = random.randrange(1, 4)
    rightN = random.randrange(1, 4)
    leftP = 4 + leftN
    rightP = leftP + 1
    leftFather = Person(1, male)
    leftMother = Person(2, female)
    rightFather = Person(3, male)
    rightMother = Person(4, female)
    leftChild = []
    rightChild = []
    familyT.add(leftFather)
    familyT.add(leftMother)
    familyT.add(rightFather)
    familyT.add(rightMother)
    
    
    for iditer in range(5, 5+leftN):
        itersex = male
        if (iditer == 4 + leftN):
            itersex = male
        else:
            if (random.random() > 0.5):
                itersex = male
            else:
                itersex = female
        leftChild.append(Person(iditer, itersex))

    for iditer in range(4+leftN + 1, 4+leftN+rightN + 1):
        itersex = female
        if (iditer == 5 + leftN):
            itersex = female
        else:
            if (random.random() > 0.5):
                itersex = male
            else:
                itersex = female
        rightChild.append(Person(iditer, itersex))

    for person in leftChild:
        familyT.add(person)

    for person in rightChild:
        familyT.add(person)

    if (random.random() > 0.5):
        itersex = male
    else:
        itersex = female
    grandchild = Person(5 + leftN + rightN, itersex)
    familyT.add(grandchild)

    #각 멤버들 결혼, 자식관계 지정하기
    
    familyT.marriage(leftFather, leftMother)
    familyT.marriage(rightFather, rightMother)
    familyT.babies(leftFather, leftMother, leftChild)
    familyT.babies(rightFather, rightMother, rightChild)
    leftSecond = familyT.find(4 + leftN)
    rightSecond = familyT.find(4 + leftN + 1)
    familyT.marriage(leftSecond, rightSecond)
    familyT.baby(leftSecond, rightSecond, grandchild)

    aux = [leftN, rightN, leftP, rightP]

    # 문제 Generate 해서 Text 넣기




    boxtxt = dict() #dictionary : int id to inside str
    # boxtxt[key] = "Text" 로 mapping 추가 가능

    gfactor = 1 # gene factor
    hfactor = 1 # hint factor


    for i in range(1, 4 + leftN + rightN + 2):
        boxtxt[i] = str(i)

    # end of problem gen

    return (familyT, aux, boxtxt)

# familyT : Class Family | Tree of family
# headcenterCoord : lefthigh coordinate
# treeSize : size of Tree



def drawTree(bot, familyGenerated, center, blocksize):
    leftN = familyGenerated[1][0]
    rightN = familyGenerated[1][1]
    txtdict = familyGenerated[2]
    font = ("Arial", 12, "normal")

    
    drawShape(bot, "square", (center[0] - 4.5 * blocksize, center[1] + 2 * blocksize), blocksize / 2, 0) # left  father
    writeTxt(bot, center, -4.5 * blocksize, 2 * blocksize, font, txtdict[1])
    drawShape(bot, "circle", (center[0] - 1.5 * blocksize, center[1] + 2 * blocksize), blocksize / 2, 0) # left  mother
    writeTxt(bot, center, -1.5 * blocksize, 2 * blocksize, font, txtdict[2])
    drawShape(bot, "square", (center[0] + 1.5 * blocksize, center[1] + 2 * blocksize), blocksize / 2, 0) # right father
    writeTxt(bot, center, 1.5 * blocksize, 2 * blocksize, font, txtdict[3])
    drawShape(bot, "circle", (center[0] + 4.5 * blocksize, center[1] + 2 * blocksize), blocksize / 2, 0) # right mother
    writeTxt(bot, center, 4.5 * blocksize, 2 * blocksize, font, txtdict[4])
    drawline(bot, center, -4 * blocksize, 2 * blocksize, 0, 2 * blocksize)
    drawline(bot, center,  2 * blocksize, 2 * blocksize, 0, 2 * blocksize)
    drawline(bot, center, -3 * blocksize, 2 * blocksize, 270, blocksize)
    drawline(bot, center,  3 * blocksize, 2 * blocksize, 270, blocksize)

    gShape = ""
    if (leftN == 1):
        drawline(bot, center, -3 * blocksize, 1 * blocksize, 270, 0.5 * blocksize)
        if (familyGenerated[0].find(familyGenerated[1][2]).sex == male):
            gShape = "square"
        else:
            gShape = "circle"
        drawShape(bot, gShape, (center[0] + blocksize * (-3), center[1]), blocksize / 2, 0) # left children
        writeTxt(bot, center, -3 * blocksize, 0 * blocksize, font, txtdict[4 + leftN])
        drawline(bot, center, -2.5 * blocksize, 0, 0, 1.5 * blocksize)
    else:
        drawline(bot, center, -4.5 * blocksize, blocksize, 0, 3 * blocksize)
        for i in range(leftN):
            if (familyGenerated[0].find(4 + 1 + i).sex == male):
                gShape = "square"
            else:
                gShape = "circle"
            drawShape(bot, gShape, (center[0] + blocksize * (-4.5 + i * (3 / (leftN - 1))), 0), blocksize / 2, 0)
            writeTxt(bot, center, blocksize * (-4.5 + i * (3 / (leftN - 1))), 0 * blocksize, font, txtdict[5 + i])
            drawline(bot, center, (-4.5 + i * (3 / (leftN - 1))) * blocksize, 1 * blocksize, 270, 0.5 * blocksize)


    if (rightN == 1):
        drawline(bot, center,  3 * blocksize, 1 * blocksize, 270, 0.5 * blocksize)
        if (familyGenerated[0].find(familyGenerated[1][3]).sex == male):
            gShape = "square"
        else:
            gShape = "circle"
        drawShape(bot, gShape, (center[0] + 3 * blocksize, center[1]), blocksize / 2, 0) # right children
        drawline(bot, center, 1 * blocksize, 0, 0, 1.5 * blocksize)
    else:
        drawline(bot, center, 4.5 * blocksize, blocksize, 180, 3 * blocksize)
        for i in range(rightN):
            if (familyGenerated[0].find(4 + leftN + 1 + i).sex == male):
                gShape = "square"
            else:
                gShape = "circle"
            drawShape(bot, gShape, (center[0] + blocksize * (1.5 + i * (3 / (rightN - 1))), 0), blocksize / 2, 0)
            writeTxt(bot, center, blocksize * (1.5 + i * (3 / (rightN - 1))), 0 * blocksize, font, txtdict[5 + leftN + i])
            drawline(bot, center, (1.5 + i * (3 / (rightN - 1))) * blocksize, 1 * blocksize, 270, 0.5 * blocksize)
    
    



    drawline(bot, center, -1 * blocksize, 0, 0, 2 * blocksize)
    drawline(bot, center, 0, 0, 270, blocksize * 1.5)
    if (familyGenerated[0].find(4 + 1 + leftN + rightN).sex == male):
        gShape = "square"
    else:
        gShape = "circle"
    drawShape(bot, gShape, (center[0], -2 * blocksize + center[1]), blocksize / 2, 0)
    writeTxt(bot, center, blocksize * 0, -2 * blocksize, font, txtdict[5 + leftN + rightN])
    
    


    





size_x = 550                # Total x width
size_w = 25                 # 여백
size_desc = (size_x, 400)   # size_desc
size_tree = (size_x, 300)   # size_tree
size_ques = (size_x, 100)   # size_ques


# automatic calculated
size_page = (size_x + 2 * size_w, size_desc[1] + size_tree[1] + size_ques[1] + 4 * size_w)

# turtle setup
turtle.setup(size_page[0], size_page[1])

# automatic calculated
x_radius = size_page[0] / 2
y_radius = size_page[1] / 2
radius = (x_radius, y_radius)
# partition
descPart = DrawPartition((size_w - x_radius, size_tree[1] + size_ques[1] + size_desc[1] + 3 * size_w - y_radius),(size_w + size_x - x_radius, size_tree[1] + size_ques[1] + 3 * size_w - y_radius))
treePart = DrawPartition((size_w - x_radius, size_ques[1] + size_tree[1] + 2 * size_w - y_radius), (size_w + size_x - x_radius, size_ques[1] + 2 * size_w - y_radius))
quesPart = DrawPartition((size_w - x_radius, size_w + size_ques[1] - y_radius), (size_w + size_x - x_radius, size_w - y_radius))

bot = turtle.Turtle()



testF = familyTreeGen()
drawTree(bot, testF, (0, 0), 30)




input("press any key to exit..")













    



                         
    

    
