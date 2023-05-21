import random
import turtle
from enum import Enum
import copy
import os
from PIL import Image

# const
male = True
female = False

class GeneT(Enum):
    ABO = 0
    P = 1
    Q = 2
    R = 3
    S = 4


maxT = dict()
maxT[GeneT.ABO] = 9
maxT[GeneT.P] = 4
maxT[GeneT.Q] = 4
maxT[GeneT.R] = 4
maxT[GeneT.S] = 4

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
        self.genes = dict()
        self.ablegenes = dict()
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

def writeTxt(turtlebot, centerCoord, xs, ys, ffont, txt, scolor, alignoption = "center"):
    numLine = 1 + txt.count('\n')
    ys = ys - ffont[1] * 2.75 - ffont[1] * 1.25 * (numLine - 1)

    # what value shit the fuck
    turtlebot.penup()
    # color : dead code..
    turtlebot.color(scolor)
    turtlebot.goto(xs + centerCoord[0], ys + centerCoord[1])
    turtlebot.pendown()
    turtlebot.write(txt, move=False, align = alignoption, font = ffont)
    turtlebot.penup()
    turtlebot.color("black")

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
        turtlebot.color("silver")

    if (opt == 6 or opt == 7):
        turtlebot.end_fill()
        turtlebot.color("black")
    
    if (opt == 1 and shapeType == "circle"):
        for i in range(0, 15, 2):
            h = (i - 7) * radius / 5
            d = (2 * (radius ** 2) - (h ** 2)) ** 0.5
            xs = -0.5 * (h + d)
            ys = xs + h
            
            drawline(turtlebot, center, xs, ys, 45, d * (2 ** 0.5))

    elif (opt == 2 and shapeType == "circle"):
        for i in range(0, 15, 2):
            h = (i - 7) * radius / 5
            d = (2 * (radius ** 2) - (h ** 2)) ** 0.5
            xs = -0.5 * (- h + d)
            ys = -xs + h

            drawline(turtlebot, center, xs, ys, -45, d * (2 ** 0.5))

    elif (opt == 3 and shapeType == "circle"):
        for i in range(0, 15, 2):
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
        for i in range(0, 15, 2):
            h = (i - 7) * radius / 8
            d = ((radius**2) - (h**2))**0.5
            xs = -d
            ys = h

            drawline(turtlebot, center, xs, ys, 0, 2 * d)

    elif (opt == 5 and shapeType == "circle"):
        for i in range(0, 15, 2):
            h = (i - 7) * radius / 8
            d = ((radius**2) - (h**2))**0.5
            xs = h
            ys = -d
            
            drawline(turtlebot, center, xs, ys, 90, 2 * d)

    elif (opt == 1 and shapeType == "square"):
        for i in range(0, 15, 2):
            h = (i - 7) * radius / 8
            d = abs(radius - abs(h))
            xs = ReLU(-h) - (radius / 2)
            ys = xs + h
            drawline(turtlebot, center, xs, ys, 45, d * (2 ** 0.5))

    elif (opt == 2 and shapeType == "square"):
        for i in range(0, 15, 2):
            h = (i - 7) * radius / 8
            d = abs(radius - abs(h))
            xs = ReLU(h) - (radius / 2)
            ys = -xs + h
            drawline(turtlebot, center, xs, ys, -45, d * (2 ** 0.5))

    elif (opt == 3 and shapeType == "square"):
        for i in range(0, 15, 2):
            h = (i - 7) * radius / 8
            d = abs(radius - abs(h))
            xs = ReLU(-h) - (radius / 2)
            ys = xs + h
            drawline(turtlebot, center, xs, ys, 45, d * (2 ** 0.5))
            xs = ReLU(h) - (radius / 2)
            ys = -xs + h
            drawline(turtlebot, center, xs, ys, -45, d * (2 ** 0.5))

    elif (opt == 4 and shapeType == "square"):
        for i in range(0, 15, 2):
            h = (i - 7) * radius / 16
            d = radius
            xs = -radius / 2
            ys = h
            drawline(turtlebot, center, xs, ys, 0, d)

    elif (opt == 5 and shapeType == "square"):
        for i in range(0, 15, 2):
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

def familyTreeGen(args):
    familyT = Family()
    # 랜덤 인수 :
    # 친가 2세대 자식이 몇명인가? leftN
    # 외가 2세대 자식이 몇명인가? rightN
    # 친가 2세대 중 누가 결혼할것인가? (id value로) leftP
    # 외가 2세대 중 누가 결혼할것인가? (id value로) rightP
    # 대립유전형질은 3종류 (Aa, Bb, Dd)
    # 상염색체 개수 (numberA), 성염색체 개수 (numberS)
    # ABO 나옴? isABOProblem
    # args = {numNormalGene, numSexGene, numABO, problemType, hintargs}
    # problemType
    """
    args : 
    numNormalGene = 0, 1, 2, 3
    numSexGene = 0, 1
    numABO : 0, 1
    problemType : {
        0 : 단순 추론 (염색체 정보를 모두 공개한 후 빈칸만 뚫어서 추측하기)
        1 : Missing link를 주기
        2 : DNA 상대량
    }
    
    """



    hintlist = []
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

    

    pType = 2
    selectedG = list()
    geneunion = dict()
    boxtxt = dict() #dictionary : int id -> str
    intxt = dict() #dictionary : int id -> str
    fillT = dict()

    

    problemT = list()
    problemCode = str(1)
    # 인간의 염색체 쌍은 23쌍
    # 상염색체 1 ~ 22, 성염색체 23
    # boxtxt[key], intxt[key] = "Text" 로 mapping 추가 가능
    # boxtxt : Number
    # intxt : 내용   

    # AA Aa aA aa 1 2 3 4 GeneT.P GeneT.Q GeneT.R
    # XX Xx xX xx 1 2 3 4 GeneT.S woman
    # XY xY       1 2     GeneT.S man
    # AA AB AO BA BB BO OA OB OO 1 2 3 4 5 6 7 8 9


    if (pType == 1):
        selectedG.append(GeneT.ABO)
        geneunion[GeneT.ABO] = 9
        selectedG.append(GeneT.P)
        geneunion[GeneT.P] = 5
        selectedG.append(GeneT.S)
        geneunion[GeneT.S] = 23
    if (pType == 2):
        selectedG.append(GeneT.P)
        geneunion[GeneT.P] = 1
        selectedG.append(GeneT.Q)
        geneunion[GeneT.Q] = 2
        selectedG.append(GeneT.R)
        geneunion[GeneT.R] = 1



    GC = familyT.find(5 + leftN + rightN)
    LM = [familyT.find(i) for i in range(5, 5 + leftN)]
    RM = [familyT.find(i) for i in range(5 + leftN, 5 + leftN + rightN)]
    LT = [familyT.find(i) for i in range(1, 3)]
    RT = [familyT.find(i) for i in range(3, 5)]

    


    initPersonList = [tuple(LT), tuple(RT)]
    iterPersonList = [tuple(LT), tuple(RT), tuple([LM[leftN - 1], RM[rightN - 1]])]
    if (pType == 2):
        for iterC in initPersonList:
            for iterPerson in iterC:
                for gs in geneunion.keys():
                    iterPerson.genes[gs] = random.randint(1, maxT[gs] - (gs == GeneT.S) * (iterPerson.sex == male) * 2)

        for (father, mother) in iterPersonList:
            for childP in father.children:
                for gno in geneunion.values():
                    r = random.random()
                    for gene in [genes for genes, gns in geneunion.items() if gns == gno]:
                        m = mother.genes[gene]
                        f = father.genes[gene]
                        x = -1
                        if (gene != GeneT.ABO and gene != GeneT.S):
                            if (abs(r - 0.5) < 0.125): #L, L -> (L : mother -> Left, father -> right)
                                x = (m > 2) * 2 + (f > 2) + 1
                            elif (abs(r - 0.5) < 0.25): #L, R -> (L)
                                x = (m > 2) * 2 + (f > 2) + 1
                            elif (abs(r - 0.5) < 0.375): #R, L -> (R)
                                x = (m > 2) * 2 + (f > 2) + 1
                            else: #R, R -> (L)
                                x = (m > 2) * 2 + (f > 2) + 1
                            if (r > 0.5):
                                if (x == 2 or x == 3):
                                    x = 5 - x
                        elif (gene == GeneT.S):
                            if (childP.sex == male): #XY xY only
                                if (r > 0.5):
                                    x = (m <= 2) + 1
                                else:
                                    x = 2 - (m % 2)
                            else: # woman
                                if (abs(r - 0.5) > 0.25): #Father -> LeftG, Mother L -> RightG
                                    x = ((m <= 2) + 1) + 2 * (f - 1)
                                else:
                                    x = ((m % 2) + 1) + 2 * (f - 1)
                                if (r > 0.5):
                                    if (x == 2 or x == 3):
                                        x = 5 - x
                        elif (gene == GeneT.ABO):
                            if (abs(r - 0.5) < 0.125):
                                f = (f + 2) // 3 # ABO 123
                                m = (m + 2) // 3 # ABO 123
                            elif (abs(r - 0.5) < 0.25):
                                f = (f + 2) // 3 # ABO 123
                                m = (m % 3) + 1 # ABO 123
                            elif (abs(r - 0.5) < 0.375):
                                f = (f % 3) + 1 # ABO 123
                                m = (m + 2) // 3 # ABO 123
                            else:
                                f = (f % 2) + 1 # ABO 123
                                m = (m % 3) + 1 # ABO 123
                            if (r > 0.5):
                                x = (f - 1) * 3 + m
                            else:
                                x = (m - 1) * 3 + f
                        else:
                            x = -1 # exception
                        
                        childP.genes[gene] = x
                    
                    

    # Hint 1 : (ExpGeneType)가 발현된 사람은 (List)이다.
    # Hint 2 : (P)의 (G1)와(과) (G2)의 DNA 상대량을 더한 값은 (x)이다.
    # Hint 3 : (Father)와(과) (Mother) 사이에 태어난 자식의 (ExpGeneType : ㄱㄴㄷ)에 대한 표현형이 (Child)와 같을 확률은 (Probability)이다.
    # Hint 4 : (G1)과 (G2)의 DNA 상대량을 더한 값이 (x)인 사람은 (y)명이다.
    # Hint 5 : (P1), (P2), (P3)가 가진 (G1)의 DNA상대량을 (P4), (P5), (P6)가 가진 (G2)의 DNA상대량으로 나눈 값은 (q)이다.
    

    hintlist = list(range(1, 6))
    random.shuffle(hintlist)
    hintlist.pop()
    for i in range(1, 4 + leftN + rightN + 2):
        targetP = familyT.find(i)
        boxtxt[i] = str(i)

        if (pType == 1):
            tmp = targetP.genes[GeneT.ABO]
            if (tmp == 0):
                intxt[i] = "O"
            elif (tmp == 1 or tmp == 2):
                intxt[i] = "A"
            elif (tmp == 3 or tmp == 6):
                intxt[i] = "B"
            else:
                intxt[i] = "AB"
            fillT[i] = (targetP.genes[GeneT.P] <= 2) * 2 + (targetP.genes[GeneT.S] <= (2 + 1 * (targetP.sex == male))) * 1 + 1
        elif (pType == 2):
            fillFactor = (targetP.genes[GeneT.Q] <= 2) * 2 + (targetP.genes[GeneT.P] <= 2)
            if (fillFactor == 0):
                fillT[i] = 0
            elif (fillFactor == 1):
                fillT[i] = 1
            elif (fillFactor == 2):
                fillT[i] = 7
            else:
                fillT[i] = 6
            intxt[i] = ""
    
    
    
    if (pType == 1):
        problemT.append(problemCode)
        problemT.append("\n")
        problemT.append("다음은 어떤 집안의 유전 형질 ㄱ, ㄴ에 관한 자료이다.\n")
        problemT.append("- ㄱ은 대립 유전자 P와 P'에 의해,\n ㄴ은 대립 유전자 Q와 Q'에 의해 결정된다.\n")
        problemT.append("- 이 아래로 조건하고 문제가 추가될겁니다")
    elif (pType == 2):
        problemT.append(problemCode)
        problemT.append("\n")
        problemT.append("다음은 어떤 집안의 유전 형질 ㄱ, ㄴ, ㄷ에 관한 자료이다.\n")
        problemT.append("- ㄱ은 대립 유전자 P와 p에 의해, ㄴ은 대립 유전자 Q와 q에 의해,\n   ㄷ은 대립 유전자 R과 r에 의해 결정된다.\n")
        problemT.append("- P는 Q과 다른 염색체에 있으며, R과는 같은 염색체에 존재한다.\n")
        problemT.append(" ■ / ● (검정) : 유전 형질 ㄱ, ㄴ 발현 남자/여자\n")
        problemT.append(" 빗금(▨) : 유전 형질 ㄱ 발현 남자 / 여자\n")
        problemT.append(" ■ / ● (회색) : 유전 형질 ㄴ 발현 남자 / 여자\n")
        problemT.append(" □ / ○ (흰색) : 정상 남자 / 여자\n")


    for hintType in hintlist:
        noPerson = 5 + leftN + rightN
        geneList = selectedG
        if (hintType == 1):
            targetG = random.choice(geneList)
            extP = list()
            if (targetG == GeneT.ABO):
                continue
            for p in range(1, noPerson + 1):
                tarP = familyT.find(p)
                if (targetG != GeneT.S or (targetG == GeneT.S and tarP.sex == female)):
                    if tarP.genes[targetG] <= 3: #발현됨
                        extP.append(p)
                elif(targetG == GeneT.S and tarP.sex == male):
                    if tarP.genes[targetG] == 1:
                        extP.append(p)
            geneString = ""
            if (targetG == GeneT.P):
                geneString = "ㄱ"
            elif (targetG == GeneT.Q):
                geneString = "ㄴ"
            elif (targetG == GeneT.R):
                geneString = "ㄷ"
            elif (targetG == GeneT.S):
                geneString = "ㄹ"
            personString = ""
            for p in extP:
                personString = personString + str(p) + " ,"
            totalStr = " - " + geneString + "가 발현된 사람은 " + personString + "이다.\n"
            problemT.append(totalStr)
        elif (hintType == 2):
            tarP = random.randint(1, noPerson)
            while(True):
                G1 = random.choice(geneList)
                if (G1 != GeneT.ABO):
                    break
            while(True):
                G2 = random.choice(geneList)
                if (G2 != GeneT.ABO and G2 != G1):
                    break
            strG1 = geneStr(G1, True)
            strG2 = geneStr(G2, False)

            geneiterList = list((G1, G2))
            sumG = 0
            cap = 1
            for gn in geneiterList:
                if (gn == GeneT.S and familyT.find(tarP).sex == male):
                    sumG = sumG + (familyT.find(tarP).genes[gn] == cap)
                elif (gn != GeneT.ABO):
                    if (cap == 1):
                        sumG = sumG + (familyT.find(tarP).genes[gn] <= 1) + (familyT.find(tarP).genes[gn] <= 3)
                    else:
                        sumG = sumG + (familyT.find(tarP).genes[gn] >= 4) + (familyT.find(tarP).genes[gn] >= 2)
                cap = 2

            totalStr = " - " + str(tarP) + "의 " + strG1 + "와(과) " + strG2 + "의 DNA 상대량을 더한 값은 " + str(sumG) + "이다.\n" 
            problemT.append(totalStr)
        elif (hintType == 3):
            # 1 - 2 = 5 ~ 4 + leftN, 3 - 4 = 5 + leftN ~ 4 + leftN + rightN, 4 + leftN - 5 + leftN = 5 + leftN + rightN
            FatherNo = 0
            MotherNo = 0
            ChildNo = 0
            rF = random.randint(1, 3)
            if (rF == 1):
                FatherNo = 1
                MotherNo = 2
                ChildNo = random.randint(5, 4 + leftN)
            elif (rF == 2):
                FatherNo = 3
                MotherNo = 4
                ChildNo = random.randint(5 + leftN, 4 + leftN + rightN)
            else:
                FatherNo = 4 + leftN
                MotherNo = 5 + leftN
                ChildNo = random.randint(5 + leftN + rightN, 5 + leftN + rightN)
            fP = familyT.find(FatherNo)
            mP = familyT.find(MotherNo)
            cP = familyT.find(ChildNo)
            EGTyp = random.choice(geneList)

            GStr = geneStr(EGTyp, True)

            pu = 0
            pd = 4

            if (EGTyp == GeneT.ABO):
                fABO = list(((fP.genes[EGTyp] - 1) // 3, ((fP.genes[EGTyp] - 1) % 3)))
                mABO = list(((mP.genes[EGTyp] - 1) // 3, ((mP.genes[EGTyp] - 1) % 3)))
                cABO = list(((cP.genes[EGTyp] - 1) // 3, ((cP.genes[EGTyp] - 1) % 3)))

                for i in range(0, 2):
                    for j in range(0, 2):
                        if (fABO[i] + mABO[j] == cABO[0] + cABO[1] and fABO[i] * mABO[j] == cABO[0] * cABO[1]):
                            pu = pu + 1

            elif (EGTyp == GeneT.S):
                pd = 2
                fS = list((fP.genes[EGTyp] // 2))
                mS = list(((mP.genes[EGTyp] - 1) // 2, (mP.genes[EGTyp] - 1) % 2))
                if (cP.sex == male):
                    pu = (mS[0] == cP.genes[EGTyp] // 2) + (mS[1] == cP.genes[EGTyp] // 2)
                else:
                    cS = list(((cP.genes[EGTyp] - 1) // 2, (cP.genes[EGTyp] - 1) % 2))
                    for i in range(0, 1):
                        for j in range(0, 2):
                            if (fS[i] + mS[j] == cS[0] + cS[1] and fS[i] * mS[j] == cS[0] * cS[1]):
                                pu = pu + 1
            else:
                pd = 4
                fABO = list(((fP.genes[EGTyp] - 1) // 2, ((fP.genes[EGTyp] - 1) % 2)))
                mABO = list(((mP.genes[EGTyp] - 1) // 2, ((mP.genes[EGTyp] - 1) % 2)))
                cABO = list(((cP.genes[EGTyp] - 1) // 2, ((cP.genes[EGTyp] - 1) % 2)))

                for i in range(0, 2):
                    for j in range(0, 2):
                        if (fABO[i] + mABO[j] == cABO[0] + cABO[1] and fABO[i] * mABO[j] == cABO[0] * cABO[1]):
                            pu = pu + 1
            
            while(True):
                if (pu == 1 or pu == 3):
                    break
                else:
                    pu = pu // 2
                    pd = pd // 2

            totalStr = " - " + str(FatherNo) + "와(과) " + str(MotherNo) + " 사이에 태어난 자식의 " + GStr + "에 대한 표현형이\n" + str(ChildNo) + "와(과) 같을 확률은 " + str(pu) + "/" + str(pd) + "이다.\n"
            problemT.append(totalStr)
        elif (hintType == 4):
            while(True):
                G1 = random.choice(geneList)
                if (G1 != GeneT.ABO):
                    break
            while(True):
                G2 = random.choice(geneList)
                if (G2 != GeneT.ABO and G2 != G1):
                    break
            strG1 = geneStr(G1, True)
            strG2 = geneStr(G2, False)
            cap = 0
            geneiterList = list((G1, G2))
            sumG = 0
            isChecked = dict()
            for gn in geneiterList:
                for i in range(1, 6 + leftN + rightN):
                    if (DNARelevant(familyT.find(i).genes, gn, cap, familyT.find(i).sex) == 1):
                        if (cap == 0):
                            isChecked[i] = True
                        else:
                            if (isChecked[i] == True):
                                sumG = sumG + 1
                    else:
                        isChecked[i] = False
                cap = 1
            totalStr = " - " + strG1 + "와(과) " + strG2 + "의 DNA 상대량을 더한 값이 1인 사람은 " + str(sumG) + "명이다.\n"
            problemT.append(totalStr)
        elif (hintType == 5):
            while(True):
                G1 = random.choice(geneList)
                if (G1 != GeneT.ABO):
                    break
            while(True):
                G2 = random.choice(geneList)
                if (G2 != GeneT.ABO and G2 != G1):
                    break
            strG1 = geneStr(G1, True)
            strG2 = geneStr(G2, False)
            cap = 0
            geneiterList = list((G1, G2))
            sU = 0
            sD = 0

            x = list(range(1, 6 + leftN + rightN))
            random.shuffle(x)
            iterP = x

            for gn in geneiterList:
                for h in range(3):
                    i = iterP[h + 3 * cap]
                    if (cap == 0):
                        sU = sU + DNARelevant(familyT.find(i).genes, gn, cap, familyT.find(i).sex)
                    else:
                        sD = sD + DNARelevant(familyT.find(i).genes, gn, cap, familyT.find(i).sex)
                cap = 1
            totalStr = " - " + str(iterP[0]) + ", " + str(iterP[1]) + ", " + str(iterP[2]) + "가 가진 " + strG1 + "의 DNA 상대량을\n  " + str(iterP[3]) + ", " + str(iterP[4]) + ", " + str(iterP[5]) + "가 가진 " + strG2 + "의 DNA상대량으로 나눈 값은 " + str(sU) + "/" + str(sD) + "이다.\n"
            problemT.append(totalStr)


    return (familyT, aux, (boxtxt, intxt, fillT, problemT))


def geneStr(gene, cap):
    if (gene == GeneT.P and cap == True):
        return "P"
    elif (gene == GeneT.P and cap == False):
        return "p"
    elif (gene == GeneT.Q and cap == True):
        return "Q"
    elif (gene == GeneT.Q and cap == False):
        return "q"
    elif (gene == GeneT.R and cap == True):
        return "R"
    elif (gene == GeneT.R and cap == False):
        return "r"
    elif (gene == GeneT.S and cap == True):
        return "X"
    elif (gene == GeneT.S and cap == False):
        return "x"
    elif (gene == GeneT.ABO):
        return "ABO"

def DNARelevant(gs, gType, gFormal, gender = male):
    gV = gs[gType]
    if (gType == GeneT.ABO):
        return ((gV - 1) // 3 == gFormal) + ((gV - 1) % 3 == gFormal)
    elif (gType == GeneT.S):
        if (gender == male):
            return 1 * ((gV // 2) == gFormal)
    else:
        return ((gV - 1) // 2 == gFormal) + ((gV - 1) % 2 == gFormal)


def drawS(bot, shp, center, mCenter, xs, ys, bs, fillcode, font, txtN, txtDict):
    txtcolor = ""
    if (fillcode == 6):
        txtcolor = "white"
    else:
        txtcolor = "black"
    drawShape(bot, shp, (center[0] + xs * bs, center[1] + ys * bs), bs / 2, fillcode)
    writeTxt(bot, center, xs * bs, ys * bs, font, txtN, scolor = "black")
    writeTxt(bot, mCenter, xs * bs, ys * bs, font, txtDict, scolor = txtcolor)

def drawTree(bot, familyGenerated, center, blocksize):
    leftN = familyGenerated[1][0]
    rightN = familyGenerated[1][1]
    txtno = familyGenerated[2][0]
    txtdict = familyGenerated[2][1]
    fillc = familyGenerated[2][2]
    font = ("Arial", 12, "normal")
    mCenter = (center[0], (center[1] + font[1] * 2))
    drawS(bot, "square", center, mCenter, -4.5, 2, blocksize, fillc[1], font, txtno[1], txtdict[1])
    drawS(bot, "circle", center, mCenter, -1.5, 2, blocksize, fillc[2], font, txtno[2], txtdict[2])
    drawS(bot, "square", center, mCenter,  1.5, 2, blocksize, fillc[3], font, txtno[3], txtdict[3])
    drawS(bot, "circle", center, mCenter,  4.5, 2, blocksize, fillc[4], font, txtno[4], txtdict[4])
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
        
        fillcode = fillc[4 + leftN]
        drawS(bot, gShape, center, mCenter, -3, 0, blocksize, fillc[4 + leftN], font, txtno[4 + leftN], txtdict[4 + leftN])
        drawline(bot, center, -2.5 * blocksize, 0, 0, 1.5 * blocksize)
    else:
        drawline(bot, center, -4.5 * blocksize, blocksize, 0, 3 * blocksize)
        for i in range(leftN):
            if (familyGenerated[0].find(4 + 1 + i).sex == male):
                gShape = "square"
            else:
                gShape = "circle"
            fillcode = fillc[5 + i]
            drawS(bot, gShape, center, mCenter, (-4.5 + i * (3 / (leftN - 1))), 0, blocksize, fillc[5 + i], font, txtno[5 + i], txtdict[5 + i])
            drawline(bot, center, (-4.5 + i * (3 / (leftN - 1))) * blocksize, 1 * blocksize, 270, 0.5 * blocksize)


    if (rightN == 1):
        drawline(bot, center,  3 * blocksize, 1 * blocksize, 270, 0.5 * blocksize)
        if (familyGenerated[0].find(familyGenerated[1][3]).sex == male):
            gShape = "square"
        else:
            gShape = "circle"
        fillcode = fillc[5 + leftN]
        drawS(bot, gShape, center, mCenter, 3, 0, blocksize, fillc[5 + leftN], font, txtno[5 + leftN], txtdict[5 + leftN])
        drawline(bot, center, 1 * blocksize, 0, 0, 1.5 * blocksize)
    else:
        drawline(bot, center, 4.5 * blocksize, blocksize, 180, 3 * blocksize)
        for i in range(rightN):
            if (familyGenerated[0].find(4 + leftN + 1 + i).sex == male):
                gShape = "square"
            else:
                gShape = "circle"
            fillcode = fillc[5 + i + leftN]
            drawS(bot, gShape, center, mCenter, (1.5 + i * (3 / (rightN - 1))), 0, blocksize, fillc[5 + i + leftN], font, txtno[5 + i + leftN], txtdict[5 + i + leftN])
            drawline(bot, center, (1.5 + i * (3 / (rightN - 1))) * blocksize, 1 * blocksize, 270, 0.5 * blocksize)
    
    



    drawline(bot, center, -1 * blocksize, 0, 0, 2 * blocksize)
    drawline(bot, center, 0, 0, 270, blocksize * 1.5)
    if (familyGenerated[0].find(4 + 1 + leftN + rightN).sex == male):
        gShape = "square"
    else:
        gShape = "circle"
    drawS(bot, gShape, center, mCenter, 0, -2, blocksize, fillc[5 + leftN + rightN], font, txtno[5 + leftN + rightN], txtdict[5 + leftN + rightN])

    bot.hideturtle()



size_x = 550                # Total x width
size_w = 25                 # 여백
size_desc = (size_x, 200)   # size_desc
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

problemTexts = ""





testF = familyTreeGen(list())
problemSentList = testF[2][3]

problemTexts = ""

for sent in problemSentList:
    problemTexts = problemTexts + sent


writeTxt(bot, (descPart.left, descPart.head), 0, 0, ("Arial", 12, "normal"), problemTexts, "black", "left")
drawTree(bot, testF, (treePart.centerAlign(0, 0, 300, 150)), 30)

cv = turtle.getcanvas()
cv.postscript(file="gen_problem.ps", colormode = 'color')
psimage=Image.open('gen_problem.ps')
psimage.save('gen_problem.png')

input("press any key to exit..")













    



                         
    

    
