import random
import turtle
from enum import Enum

# const
male = True
female = False

class GeneT(Enum):
    ABO = 0
    P = 1
    Q = 2
    R = 3
    S = 4

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

def writeTxt(turtlebot, centerCoord, xs, ys, ffont, txt, scolor = "black", alignoption = "center"):
    ys = ys - ffont[1] * 2.75
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

    

    pType = random.randint(1, 3)
    selectedG = list()
    if (pType == 1):
        selectedG.append(GeneT.ABO)
        selectedG.append(GeneT.P)
        selectedG.append(GeneT.S)


    # Gene : ABO, P, Q, R, S = (0, 1, 2, 3, 4)
    # 상염색체 | {AA 1 Aa 2 aa 3}
    
    # ABO | {AA 2 AO 1 BB 6 BO 3 OO 0 AB 4}
    # Consider A as 1, B as 3

    # 
    # 성염색체 | {X'X' 1 2 X'X 3 4 XX 5 6 X'Y 1 2 3 XY 4 5 6}

    # Gene Phase 1 : 조부모들의 유전형을 임의로 결정한다.
    for typ in selectedG:
        for i in range(1, 5):
            targetP = familyT.find(i)
            r = random.random()
            x = 0
            if (typ == GeneT.ABO): # 복대립 ABO
                if r < 1/6:
                    x = 1
                elif r < 2/6:
                    x = 2
                elif r < 3/6:
                    x = 3
                elif r < 4/6:
                    x = 4
                elif r < 5/6:
                    x = 5
                else:
                    x = 6
            elif (typ == GeneT.S): # 성염색체
                if r < 1/6:
                    x = 1
                elif r < 2/6:
                    x = 2
                elif r < 3/6:
                    x = 3
                elif r < 4/6:
                    x = 4
                elif r < 5/6:
                    x = 5
                else:
                    x = 6
            else: # 상염색체
                if r < 0.3:
                    x = 1
                elif r < 0.8:
                    x = 2
                else:
                    x = 3
            
            targetP.genes[typ] = x  
    
    # Gene Phase 2 : 자식들한테 유전시킨다.
    for i in range(0, 2):
        fatherP = familyT.find(1 + 2 * i)
        motherP = familyT.find(2 + 2 * i)
        for j in range(5 + leftN * i, 5 + leftN + rightN * i):
            targetP = familyT.find(j)
            targetP.genes = geneHeredity(fatherP, motherP, selectedG, targetP.sex)
    fatherP = familyT.find(4 + leftN)
    motherP = familyT.find(4 + leftN + 1)
    targetP = familyT.find(4 + leftN + rightN + 1)
    targetP.genes = geneHeredity(fatherP, motherP, selectedG)

    boxtxt = dict() #dictionary : int id -> str
    intxt = dict() #dictionary : int id -> str
    fillT = dict()
    # boxtxt[key], intxt[key] = "Text" 로 mapping 추가 가능
    # boxtxt : Number
    # intxt : 내용

    gfactor = 1 # gene factor
    hfactor = 1 # hint factor

    # intxt에 넣을거 넣으면됨

    for i in range(1, 4 + leftN + rightN + 2):
        targetP = familyT.find(i)
        boxtxt[i] = str(i)

        if (pType == 1): #ABO, P, S
            # In-Box : ABO, Fill : P, S 복합
            # AA, Aa : 발현, aa : 미발현
            tmp = targetP.genes[GeneT.ABO]
            if (tmp == 0):
                intxt[i] = "O"
            elif (tmp == 1 or tmp == 2):
                intxt[i] = "A"
            elif (tmp == 3 or tmp == 6):
                intxt[i] = "B"
            else:
                intxt[i] = "AB"
            
            # 여자 : 2 이하일 때 발현 / 남자 : 3 이하일 때 발현
            fillT[i] = (targetP.genes[GeneT.P] <= 2) * 2 + (targetP.genes[GeneT.S] <= (2 + 1 * (targetP.sex == male))) * 1 + 1 
            
            
        
        intxt[i] = 1 # 박스안에 채워질 애들
        fillT[i] = 1 # 채색수


    # end of problem gen

    return (familyT, aux, (boxtxt, intxt, fillT))

# familyT : Class Family | Tree of family
# headcenterCoord : lefthigh coordinate
# treeSize : size of Tree

def ABOAnalysis(aboFactor):
    if (aboFactor % 2 == 0):
        if (aboFactor == 4):
            return (3, 1)
        else:
            return (aboFactor/2, aboFactor/2)
    else:
        if (aboFactor == 1):
            return (1, 0)
        elif (aboFactor == 3):
            return (3, 0)

# 아래 3개 함수는 안 건드리는게 정신건강에 이롭습니다
# 잘 짜놨겠거니 하고 건들지마세요 제발

def geneHeredity(father, mother, selectedG, sex): # return by dict
    ret = dict()
    for typ in selectedG:
        r = random.random()
        F = father.genes[typ]
        M = mother.genes[typ]
        x = 0
        if (typ == GeneT.ABO): # memo : A = 1, B = 3, O = 0
            mABO = ABOAnalysis(M)
            fABO = ABOAnalysis(F)
            mF = -1
            fF = -1
            if (r < 0.25):
                mF = mABO[0]
                fF = fABO[0]
            elif (r < 0.5):
                mF = mABO[0]
                fF = fABO[1]
            elif (r < 0.75):
                mF = mABO[1]
                fF = fABO[0]
            else:
                mF = mABO[1]
                fF = fABO[1]
            x = mF + fF
            
        elif (typ == GeneT.S):
            if (sex == male): # male : XY, X는 부모 염색체를 물려받음
                if (M <= 2) : # X'X'
                    x = 1
                elif (M <= 4): # X'X
                    if (r < 0.5):
                        x = 1
                    else:
                        x = 4
                else: # XX
                    x = 4
            else: #female : XX. 하나의 X는 어머니, 다른 하나의 X는 아버지
                if (M <= 2): # 어머니가 X'X'라면
                    x = 2 #확정 X'X'
                elif (M <= 4): # 어머니가 X'X라면
                    if (r < 0.5):
                        x = 2
                    else:
                        x = 4
                else: #어머니가 XX라면
                    x = 4
                if (F >= 4):
                    x = x + 2
        else :
            if (F + M == 2): # AA - AA
                x = 1 # AA only
            elif (F + M == 3): ## AA - Aa
                if (r < 0.5):
                    x = 1
                else:
                    x = 2
            elif (F + M == 4 and F * M == 3): ## AA - aa
                x = 2
            elif (F + M == 4 and F * M == 4): ## Aa - Aa
                if (r < 0.25):
                    x = 1
                elif (r < 0.5):
                    x = 3
                else:
                    x = 2
            elif (F + M == 5) : ## Aa - aa
                if (r < 0.5):
                    x = 2
                else:
                    x = 3
            else: # aa - aa
                x = 3
        ret[typ] = x
    return ret

def drawS(bot, shp, center, mCenter, xs, ys, bs, fillcode, font, txtN, txtDict):
    txtcolor = ""
    if (fillcode == 6):
        txtcolor = "white"
    else:
        txtcolor = "black"
    drawShape(bot, shp, (center[0] - xs * bs, center[1] + ys * bs), bs / 2, fillcode)
    writeTxt(bot, center, xs * bs, ys * bs, font, txtN, color=txtcolor)
    writeTxt(bot, mCenter, xs * bs, ys * bs, font, txtDict, color = txtcolor)

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
writeTxt(bot, (descPart.left, descPart.head), 0, 0, ("Arial", 20, "normal"), "Hello, This is test text", 0, "left")

testF = familyTreeGen(list())
drawTree(bot, testF, (treePart.centerAlign(0, 0, 300, 150)), 30)




input("press any key to exit..")













    



                         
    

    
