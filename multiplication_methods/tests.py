"""
Test the major components of Number class in numbers.py
"""


import numpy as np
import pprint
from customnumbers import Number


SEP = '-'*8

class TestResults:
    def __init__(self, name, passed, failed, failCases):
        self.name = name
        self.passed = passed
        self.failed = failed
        self.total = passed + failed
        self.failCases = failCases
        
    @classmethod
    def fromCaseLists(cls, name, trueCases, testCases):
        """Construct TestResults from lists of cases which whould be equal"""
        
        equal = 0
        unequal = 0
        unequalCases = []
        for a, b in zip(trueCases, testCases):
            if a == b:
                equal += 1
            else:
                unequal += 1
                unequalCases.append((a, b))
                
        return TestResults(name, equal, unequal, unequalCases)
        
    def __repr__(self):
        return (
            '<{0} test results: {1} passed out of {2}>'
            .format(self.name, self.passed, self.total)
        )
        
    def report(self):
        if self.failCases:
            failCaseText = (
                'First 5 failed cases:\n' +
                pprint.pformat(self.failCases[:5])
            )
        else:
            failCaseText = 'No failed cases.'\
            
        print('\n'.join([
            SEP,
            '{0} test results:'.format(self.name),
            'Passed {0} out of {1}'.format(self.passed, self.total),
            failCaseText
        ]))
        

def baseTest():
    """Test Number construction, Number.__repr__, Number.asInt"""
    
    NTESTS = 100
    ints = np.random.randint(low=0, high=10, size=NTESTS)
    testInts = []
    for x in ints:
        if np.random.random() > 0.5:
            testInts.append(-1*x)
        else:
            testInts.append(x)
    testNums = [
        Number(str(abs(x)), isNegative=(x < 0)).asInt()
        for x in testInts
    ]
    trueCases, testCases = testInts, testNums
    return TestResults.fromCaseLists('Base Number', trueCases, testCases)
    
def staticTest():
    """
    Test static methods: addDigits, addOne, subtractTenPower,
    and ninesComplement
    """
    
    NINTS = 100
    trueCases, testCases = [], []
    testPosInts = np.random.randint(low=1000, high=100000, size=NINTS)
    
    # Test addDigit
    for x in range(10):
        for y in range(10):
            if np.random.random() > 0.5:
                carry = 0
            else:
                carry = 1
            trueCases.append(x + y + carry)
            testCases.append(
                int(Number.addDigits(str(x), str(y), str(carry)))
            )
    
    # Test addOne
    trueCases += [x+1 for x in testPosInts] * 2
    testCases += [int(Number.addOne(str(x), isReversed=False))
                    for x in testPosInts]
    testCases += [int(Number.addOne(str(x)[::-1])[::-1])
                    for x in testPosInts]
    
    # Test subtractTenPower
    for x in testPosInts:
        maxB = len(str(x))-1
        minB = 0
        B = np.random.randint(low=minB, high=maxB+1)
        trueCases.append(x - 10**B)
        reverseChoice = np.random.random()
        if reverseChoice > 0.5:
            testCases.append(
                int(Number.subtractTenPower(str(x), B, isReversed=False))
            )
        else:
            testCases.append(
                int(Number.subtractTenPower(str(x)[::-1], B, isReversed=True)[::-1])
            )
    
    # Test ninesComplement
    trueCases += [int( '9'*len(str(x)) ) - x            for x in testPosInts]
    testCases += [int( Number.ninesComplement(str(x)) ) for x in testPosInts]
    
    return TestResults.fromCaseLists('Static Methods', trueCases, testCases)

def additionTest():
    """Test Number.__add__ for positive arguments"""
    
    NTESTS = 1000
    testPosInts = np.random.randint(low=0, high=100000, size=NTESTS)
    testPosNums = [Number(str(x)) for x in testPosInts]
    intSums = [a+b           for a, b in zip(testPosInts, reversed(testPosInts))]
    numSums = [(a+b).asInt() for a, b in zip(testPosNums, reversed(testPosNums))]
    trueCases, testCases = intSums, numSums
    return TestResults.fromCaseLists('Addition', trueCases, testCases)

def subtractionTest():
    """Test Number.__sub__ for positive arguments"""
    
    NTESTS = 1000
    testPosInts = np.random.randint(low=0, high=100000, size=NTESTS)
    testPosNums = [Number(str(x)) for x in testPosInts]
    intDiffs = [a-b           for a, b in zip(testPosInts, reversed(testPosInts))]
    numDiffs = [(a-b).asInt() for a, b in zip(testPosNums, reversed(testPosNums))]
    trueCases, testCases = intDiffs, numDiffs
            
    return TestResults.fromCaseLists('Subtraction', trueCases, testCases)
    
def arithmeticRoutingTest():
    """
    Test correct routing for non-positive arguments in
    Number.__add__ and Number.__sub__
    """
    
    NTESTS = 1000
    testInts = np.random.randint(low=-10000, high=10000, size=NTESTS)
    testNums = [Number(str(x), isNegative=(x < 0)) for x in testInts]
    intSums =  [a+b           for a, b in zip(testInts, reversed(testInts))]
    numSums =  [(a+b).asInt() for a, b in zip(testNums, reversed(testNums))]
    intDiffs = [a-b           for a, b in zip(testInts, reversed(testInts))]
    numDiffs = [(a-b).asInt() for a, b in zip(testNums, reversed(testNums))]
    trueCases = intSums + intDiffs
    testCases = numSums + numDiffs
    
    return TestResults.fromCaseLists('Arithmetic routing', trueCases, testCases)
    
def decimalDecomposeTest():
    """Test Number.decimalDecompose"""
    
    NTESTS = 1000
    testInts = np.random.randint(low=0, high=100000, size=NTESTS)
    testNums = [Number(str(x), isNegative=False) for x in testInts]
    trueCases, testCases = [], []
    for x, xn in zip(testInts, testNums):
        B = np.random.randint(low=0, high=2*len(xn))
        trueCases.append([x % 10**B, x//10**B])
        testCases.append([t.asInt() for t in xn.decimalDecompose(B)])
    
    return TestResults.fromCaseLists('Decimal decomposition', trueCases, testCases)


baseTest().report()
staticTest().report()    
additionTest().report()
subtractionTest().report()
arithmeticRoutingTest().report()
decimalDecomposeTest().report()
