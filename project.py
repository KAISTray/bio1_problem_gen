import random

##const
male = True
female = False

# description / notes
"""
Person class : Id(Int), Sex(Boolean), Genes(List), Mother(Person)
Father(Person), Spouse(Person), Children(Set(Person))
Family class : Set(Person) //Hh, Tt, ABO, etc..


문제 제시유형

1. 가계도


"""
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


def genProblem(type):
    if (type == 1):
        print("temp")
    else:
        print("tempp")


def familyTreeProblem():
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
    rightP = random.randrage(0, rightN)

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
    
    #Family.marriage()
                         
    

    
