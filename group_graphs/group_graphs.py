class Power:
    """ A power x^n of a generator x """
    
    def __init__(self, x, n):
        self.x = x
        self.n = n
        
    def __repr__(self):
        return f'<Power: { str(self) }>'
        
    def __str__(self):
        return f'{ self.x }{ self.n }'
    
    def flattened(self):
        n = abs(self.n)
        sign = 1 if self.n > 0 else -1
        return [(self.x, sign)] * n
    
    def __eq__(self, other):
        return self.x == other.x and self.n == other.n
    
    def __lt__(self, other):
        if self.x != other.x:
            return self.x < other.x
        return self.n < other.n
        
    
class Word:
    """ A word represented as a list of Powers """
    
    def __init__(self, powers=None):
        if not powers:
            # Note: if we use default powers=[], the powers list is 
            # shared between all Word objects
            powers = []
        self.powers = powers
        
    def __repr__(self):
        return f'<Word: { str(self) }>'
    
    def __str__(self):
        return ''.join((str(p) for p in self.powers)) if self.powers else '1'
    
    def __len__(self):
        return sum([abs(p.n) for p in self.powers])
    
    def flattened(self):
        """ Return a representation of the word as a list tuples
            (generator, exponent) where exponent is 1 or -1
            
            Example: 'x2yx-1' -> ['x', 'x', 'y', 'x'], [1, 1, 1, -1]
        """
        
        return [t for p in self.powers for t in p.flattened()]
    
    def __lt__(self, other):
        if len(self) != len(other):
            return len(self) < len(other)
        for sp, op in zip(self.powers, other.powers):
            if sp != op:
                return sp < op
        return False
    
    @classmethod
    def fromList(cls, arr):
        """ Build word from list of (x, n) tuples """
        
        word = cls()
        for x, n in arr:
            word.extend_right(Power(x, n))
        return word
    
    def copy(self):
        """ Return a copy """
        
        return Word(powers=[copy.copy(p) for p in self.powers])
        
    def _simplify_right(self):
        """ Call after extend to combine rightmost powers """
        
        canCombine = (
            len(self.powers) > 1 
            and self.powers[-2].x == self.powers[-1].x
        )
        if canCombine:
            self.powers[-2].n += self.powers[-1].n
            self.powers.pop()
            if self.powers[-1].n == 0:
                self.powers.pop()
    
    def extend_right(self, power):
        """ Extend word on the right by one power """
        
        if power.n != 0:
            self.powers.append(power)
            self._simplify_right()
            
    def copy_extend_right(self, x, n):
        """ Return a new word extended on the right by one power """
        
        word = self.copy()
        word.extend_right(Power(x, n))
        return word