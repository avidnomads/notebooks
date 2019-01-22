from collections import defaultdict
from operator import itemgetter


class Rational:
    """
    Class for storing and operating on decimal strings which
    may include a fractional part
    """
    
    """Multiplication table for single digit numbers"""
    multTable = {
        str(d_one): {
            str(d_two): d_one*d_two for d_two in range(10)
        } 
        for d_one in range(10)
    }
    
    def __init__(self, string):
        if string[0] == '-':
            self.isNegative = True
            string = string[1:]
        else:
            self.isNegative = False
        string = string.strip('0')
        self.stringRep = string
        dotIndex = string.find('.')
        if dotIndex < 0:
            self.highestPower = len(string)-1
        else:
            self.highestPower = dotIndex-1
        self.digits = [d for d in string if d != '.']
        
    def __repr__(self):
        if self.isNegative:
            return '<Rational: -' + self.stringRep + '>'
        return '<Rational: ' + self.stringRep + '>'
    
    @classmethod
    def fromDigits(cls, digits, highestPower, negative=False):
        """Use list of digits and highest power to construct Rational"""
        
        s = ''.join([str(digit) for digit in digits])
        if highestPower < 0:
            s = '.' + '0'*(-1-highestPower) + s
        else:
            dotIndex = highestPower + 1
            if dotIndex < len(digits):
                s = s[:dotIndex] + '.' + s[dotIndex:]
        if negative:
            s = '-' + s
        return cls(s)
    
    @property
    def digitPowers(self):
        """List of tuples containing digits and corresponding powers of ten"""
        
        return [(d, self.highestPower-i) for i, d in enumerate(self.digits)]
    
    def asFloat(self):
        if self.isNegative:
            return -1*float(self.stringRep)
        return float(self.stringRep)
    
    def __mul__(self, other):
        """Multiply two Rationals by the grid method"""
        
        # 1. Compute products of individual digits, tracking powers of ten
        products = [
            (Rational.multTable[selfDigit][otherDigit], selfPower + otherPower)
            for selfDigit, selfPower in self.digitPowers
            for otherDigit, otherPower in other.digitPowers
        ]
        productsByPower = defaultdict(int)
        for product, power in products:
            productsByPower[power] += product
        
        # 2. Loop over components, adding runover to the next digit until
        #    all components are in the range 0-9
        lowestPower = min(productsByPower.keys())
        highestPower = max(productsByPower.keys())
        currentPower = lowestPower
        while currentPower <= highestPower:
            currentProduct = productsByPower[currentPower]
            if currentProduct > 9:
                productsByPower[currentPower] = currentProduct % 10
                productsByPower[currentPower+1] += currentProduct // 10
                if currentPower == highestPower:
                    highestPower += 1
            currentPower += 1
        
        # 3. Construct and return the Rational from the components
        components = list(productsByPower.items())
        components.sort(reverse=True, key=itemgetter(0))
        digits = [c[1] for c in components]
        hp = components[0][0]
        isNegative = (self.isNegative and not other.isNegative) or (not self.isNegative and other.isNegative)
        return Rational.fromDigits(digits, highestPower=hp, negative=isNegative)
        

class Number():
    """
    For storing and operating on integers represented by a
    decimal string and a sign bit
    """
    
    """Table of additions of numbers 0-10"""
    addTable = {
        str(d_one): {
            str(d_two): str(d_one + d_two) for d_two in range(11)
        } 
        for d_one in range(11)
    }
    
    """Table of products of single digit numbers"""
    multTable = {
        str(d_one): {
            str(d_two): str(d_one*d_two) for d_two in range(10)
        } 
        for d_one in range(10)
    }
    
    """Table of plus-ones for each digit < 9"""
    incTable = {str(d): str(d+1) for d in range(9)}
    
    """Table of minus-ones for each digit > 0"""
    decTable = {str(d): str(d-1) for d in range(1, 10)}
    
    """Table of nine's complements for each digit"""
    ninesTable = {str(d): str(9-d) for d in range(10)}
    
    def __init__(self, string, isNegative=False, preReversed=False):
        s = string
        if not preReversed:
            s = s[::-1]
        s = s.rstrip('-')
        if s == '0'*len(s):
            s = '0'
        else:
            s = s.rstrip('0')
            
        self.string = s
        self.isNegative = isNegative
        
    def __repr__(self):
        if self.isNegative:
            return '-' + self.string[::-1]
        return self.string[::-1]
    
    def asInt(self):
        return int(str(self))
    
    def negated(self):
        return Number(self.string, isNegative=(not self.isNegative), preReversed=True)
        
    def __len__(self):
        return len(self.string)
    
    @staticmethod
    def addDigits(a, b, carry='0'):
        if carry == '0':
            return Number.addTable[a][b]
        return Number.addTable[a][ Number.addTable[b]['1'] ]
        
    def __add__(self, other):
        # Handling cases other than self, other both positive
        if not self.isNegative and other.isNegative:
            return self - other.negated() # self - (-other)
        elif self.isNegative and not other.isNegative:
            return other - self.negated() # other - (-self)
        elif self.isNegative and other.isNegative:
            return (self.negated() + other.negated()).negated() # -(-self + -other)
        
        s = self.string
        o = other.string
        d = len(s) - len(o)
        if d > 0:
            o += '0'*d
        if d < 0:
            s += '0'*abs(d) 
            
        newDigits = []
        carry = '0'
        for ds, do in zip(s, o):
            r = Number.addDigits(ds, do, carry)
            if len(r) > 1:
                carry = '1'
            else:
                carry = '0'
            newDigits.append(r[-1])
        if carry == '1':
            newDigits.append('1')
        return Number(''.join(newDigits), preReversed=True)
    
    def __eq__(self, other):
        if self.isNegative != other.isNegative:
            return self.string == '0' and other.string == '0'
        return self.string.rstrip('0') == other.string.rstrip('0')
    
    def __lt__(self, other):
        """Return self < other"""
        
        if self.isNegative != other.isNegative:
            return self.isNegative
        if len(self) < len(other):
            return True
        if len(self) > len(other):
            return False
        
        # Numbers have same sign and equal lengths
        for i in range(len(self)-1, -1, -1):
            if self.string[i] < other.string[i]:
                return True
        return False
    
    @staticmethod
    def addOne(s, isReversed=True):
        """Add one to a decimal string. Note: automatically strips extra zeros"""
        
        if isReversed:
            if s[-1] == '0':
                s = s.rstrip('0')
            for i, d in enumerate(s):
                if d != '9':
                    return ''.join(['0'*i, Number.incTable[d], s[i+1:]])
            # If here, string is all 9s
            return ''.join(['0'*len(s), '1'])
        else:
            if s[0] == '0':
                s = s.lstrip('0')
            i = len(s) - 1
            while i > -1:
                if s[i] != '9':
                    return ''.join([s[:i], Number.incTable[s[i]], '0'*(len(s) - i - 1)])
                i -= 1
            # If here, string is all 9s
            ''.join(['1', '0'*len(s)])
    
    @staticmethod
    def subtractTenPower(s, power, isReversed=True):
        """Subtract power of ten from a decimal string"""
    
        L = len(s)
        if L < power + 1:
            return (
                Number(s, preReversed=isReversed) -
                Number(''.join(['0'*power, '1']), preReversed=True)
            ).string
        
        if isReversed:
            i = power
            while i < L:
                if s[i] != '0':
                    return ''.join([
                        s[:power], '9'*(i - power), Number.decTable[s[i]], s[i+1:]
                    ])
                i += 1
            raise ValueError('Unexpected trailing zeros: ' + s)
        else:
            i = L - power - 1
            while i > -1:
                if s[i] != '0':
                    return ''.join([
                        s[:i], Number.decTable[s[i]], '9'*(L-power-1-i), s[L-power:]
                    ])
                i -= 1
            raise ValueError('Unexpected leading zeros: ' + s)
            
    @staticmethod
    def ninesComplement(s):
        return ''.join([Number.ninesTable[d] for d in s])
    
    def __sub__(self, other):
        """Compute self-other by method of ten's complement"""
        
        # Handling cases other than self, other both positive
        if not self.isNegative and other.isNegative:
            return self + other.negated() # self + (-other)
        elif self.isNegative and not other.isNegative:
            return (self.negated() + other).negated() # -((-self) + other)
        elif self.isNegative and other.isNegative:
            return (self.negated() - other.negated()).negated() # -((-self) - (-other))
        
        # Note: other.string is reversed
        nco = Number.ninesComplement(other.string)
        nco = Number.addOne(nco, isReversed=True)
        t = (self + Number(nco, preReversed=True)).string
        
        B = len(other)
        if len(t) > B:
            return Number(Number.subtractTenPower(t, B), preReversed=True)
        else:
            t += '0'*(B - len(t))
            nct = Number.ninesComplement(t)
            nct = Number.addOne(nct)
            return Number(nct, isNegative=True, preReversed=True)