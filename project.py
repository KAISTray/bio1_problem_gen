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

    def marriage(person1, person2):
        if (person1.sex != person2.sex):
            person1.spouse = person2
            person2.spouse = person1
            childs = person1.children | person2.children
            person1.children = childs
            person2.children = childs

    def baby(father, mother, child):
        father.children.add(child)
        mother.children.add(child)

    def babies(father, mother, children): #list input!
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
        turtlebot.color("gray")

    if (shapeType == "circle"):
        turtlebot.circle(radius)
    elif (shapeType == "square"):
        turtlebot.goto(center[0] - (radius / 2), center[1] - (radius / 2))
        for _ in range(4):
            turtlebot.forward(radius)
            turtlebot.left(90)
    
    turtlebot.penup()
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

            drawline(turtlebot, xs, ys, -45, d * (2 ** 0.5))

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
    if (shapeType == "square"):
        return originRadius
    else:
        return originRadius / 2

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
    leftP = random.randrange(0, leftN)
    rightP = random.randrange(0, rightN)

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
        if (iditer - 5 == leftP):
            itersex = male
        else:
            if (random.random() > 0.5):
                itersex = male
            else:
                itersex = female
        leftChild.append(Person(iditer, itersex))

    for iditer in range(4+leftN, 4+leftN+rightN):
        itersex = female
        if (iditer - 5 - leftN == rightP):
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

    grandchild = Person(5 + leftN + rightN)
    familyT.add(grandchild)

    #각 멤버들 결혼, 자식관계 지정하기
    
    Family.marriage(leftFather, leftMother)
    Family.marriage(rightFather, rightMother)
    Family.babies(leftFather, leftMother, leftChild)
    Family.babies(rightFather, rightMother, rightChild)
    leftSecond = familyT.find(5 + leftP)
    rightSecond = familyT.find(4 + leftN + rightP)
    Family.marriage(leftSecond, rightSecond)
    Family.babies(leftSecond, rightSecond, grandchild)

    aux = [leftN, rightN, leftP, rightP]
    return (familyT, aux)

# familyT : Class Family | Tree of family
# headcenterCoord : lefthigh coordinate
# treeSize : size of Tree



def drawTree(familyT, headcenterCoord = (0, 950), treeSize = (920, 700)):
    size_pen = 1
    pen = turtle.Turtle("circle") # circle-shaped turtle generated
    pen.pensize(size_pen)
    pen.pencolor("black")


    





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





input("press any key to exit..")













    



                         
    

    
