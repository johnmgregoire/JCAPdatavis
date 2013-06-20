""" Calculate the steadystate mean. This is done by breaking the x into
    pieces each of the size of TestPts. We try to add more and more test
    points to the range that will produce our steadystate mean. This is done
    without adding more noise by checking the value of the standard deviation
    of that range weighted accordingly. The value of WeightExp is in order to
    weight the importance of std and the number of points. """
def CalcArrSS(x, WeightExp=1., TestPts=10):
    p=WeightExp
    i=TestPts
    s0=x[:i].std()/i**p+1
    while x[:i].std()/i**p<s0 and i<len(x):
        s0=x[:i].std()/i**p
        i+=TestPts
    return x[:i].mean()
