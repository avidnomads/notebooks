import math
import matplotlib.pyplot as plt
import numpy as np
from customnumbers import Complex

def DFTdirect(x):
    """Compute the DFT of series from the definition"""
    
    N = len(x)
    X = []
    for k in range(N):
        X_k = Complex(0,0)
        for n in range(N):
            a = 2*math.pi*k*n/N
            X_k += x[n]*Complex(math.cos(a), -math.sin(a))
        X.append(X_k)
    return X
    
def IDFTdirect(X):
    """Compute inverse DFT from the definition"""
    
    N = len(X)
    x = []
    for n in range(N):
        x_n = Complex(0,0)
        for k in range(N):
            a = 2*math.pi*k*n/N
            x_n += X[k]*Complex(math.cos(a), math.sin(a))
        x.append((1/N)*x_n)
    return x
    
def testDFT(DFTfn, IDFTfn, TOL=10**-6):
    """Test that IDFT(DFT(x)) = x, within tolerance"""
    
    N_TESTS = 100
    LEN = 100
    
    seqs = [randomSeq(LEN, -1000, 1000) for _ in range(N_TESTS)]
    passed = 0
    failed = 0
    failed_seqs = []
    for x in seqs:
        case_failed = False
        
        y_1 = IDFTfn(DFTfn(x))
        y_2 = DFTfn(IDFTfn(x))
        for a, b, c in zip(x, y_1, y_2):
            if (
                abs(a.re - b.re) > TOL or abs(a.im - b.im) > TOL or
                abs(a.re - c.re) > TOL or abs(a.im - c.im) > TOL
            ):
                case_failed = True
                break
        
        if case_failed:
            failed += 1
            failed_seqs.append(x)
        else:
            passed += 1
    
    print('----')
    print('testDFT results:')
    print('Passed {} out of {} cases.'.format(passed, passed+failed))
    return failed_seqs
    
def testDFTmultiply(DFTfn, IDFTfn):
    """Test DFT multiplication algorithm"""
    
    N_TESTS = 1000
    
    nums = [np.random.randint(1, 10**8) for _ in range(N_TESTS)]
    passed = 0
    failed = 0
    failed_cases = []
    for a,b in zip(nums, reversed(nums)):
        stringsReversed = (np.random.random() < 0.5)
        if stringsReversed:
            c = DFTmultiply(
                str(a)[::-1], str(b)[::-1], DFTdirect, IDFTdirect,
                stringsReversed=stringsReversed
            )
        else:
            c = DFTmultiply(
                str(a), str(b), DFTdirect, IDFTdirect,
                stringsReversed=stringsReversed
            )
        true_product = str(a*b)
        if true_product != c:
            failed += 1
            failed_cases.append((a, b))
        else:
            passed += 1
    
    print('----')
    print('testDFTmultiply results:')
    print('Passed {} out of {} cases.'.format(passed, passed+failed))
    return failed_cases
    
def DFTmultiply(x, y, DFTfn, IDFTfn, stringsReversed=False):
    """Compute product of two numbers using DFT algorithm
    
    Args: 
    x, y -- decimal strings
    DFTfn, IDFTfn -- functions to compute transform and inverse transform
    stringsReversed -- bool indicating if x, y are reversed (i.e. in ascending order)
    
    Return: decimal string of x*y in usual order (i.e. in descending order)
    """
    
    #NOTE: theoretically this should actually happen in the Cooley-Tukey DFT fn, 
    #but more efficient to do here
    # 1. Convert decimal strings to lists of digits, pad with zeros so that length
    #    is a power of 2
    N_1 = len(x)
    N_2 = len(y)
    p = math.log(N_1 + N_2, 2)
    N = 2**math.ceil(p)
    
    if stringsReversed:
        x_seq = [int(d) for d in x] + [0]*(N - N_1) 
        y_seq = [int(d) for d in y] + [0]*(N - N_2)
    else:
        x_seq = [int(d) for d in x[::-1]] + [0]*(N - N_1) 
        y_seq = [int(d) for d in y[::-1]] + [0]*(N - N_2)
    
    # 2. Compute DFT of sequences and multiply them elementwise
    X = DFTfn(x_seq)
    Y = DFTfn(y_seq)
    C = [a*b for a,b in zip(X,Y)]
    
    # 3. Compute inverse DFT to get coefficients of product polynomial
    c = IDFTfn(C)
    c_seq = [round(s.re) for s in c]
    
    # 4. Do carry operation and return cleaned decimal string
    carry = 0
    c_seq_carry = []
    for digit in c_seq:
        s = digit + carry
        new_digit, carry = s % 10, s//10
        c_seq_carry.append(new_digit)
    
    r = ''.join([str(d) for d in c_seq_carry])
    r = r.rstrip('0')[::-1]
    return r

def plotDFT(x):
    """Plot sequence x and its DFT in the complex plane"""
    
    X = DFTdirect(x)
    plt.plot([c.re for c in x], [c.im for c in x], 'ro')
    plt.plot([c.re for c in X], [c.im for c in X], 'bo')
    plt.show()
    
def randomSeq(n, a, b):
    """Random Complex seq, length n, with components in range [a, b)"""
    
    return [
        Complex(a + np.random.random()*(b-a), a + np.random.random()*(b-a))
        for _ in range(n)
    ]
    
    
if __name__ == '__main__':
    failed = testDFTmultiply(DFTdirect, IDFTdirect)
    if failed:
        print(failed)
