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
    # option 4 : vertical hatched
    # option 5 : horizontal hatched
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
            
    elif (opt == 3 and shapeType == "square"):

    elif (opt == 4 and shapeType == "square"):

    elif (opt == 5 and shapeType == "square"):
    



    return













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


def drawTree(familyT, aux):
    size_pen = 1
    pen = turtle.Turtle("circle") # circle-shaped turtle generated
    pen.pensize(size_pen)
    pen.pencolor("black")


















    



                         
    

    
