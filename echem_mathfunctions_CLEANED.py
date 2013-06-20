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

""" Function that removes single pixel outliers. It does this by checking each
    datapoint with two neighbors and checking if it is bigger than both of its
    neighbors times critratiotoneighbors. If it is, then it replaces the value
    by averaging the two neighbors."""
def removesinglepixoutliers(arr,critratiotoneighbors=1.5):
    # Only checks the array without the ends because the ends don't have both
    # a datapoint to the left and the right. It compares this to arrays that
    # are offset by 2 at either the end or beginning. This makes sure to compare
    # each datapoint with the datapoint to its right and to its left. 
    c=numpy.where((arr[1:-1]>(critratiotoneighbors*arr[:-2]))*(arr[1:-1]>(critratiotoneighbors*arr[2:])))
    # We get the index of the points that match both of the comparisons above.
    # We add 1 to account for the fact that indexing was off by 1 since we
    # did not account for either end
    c0=c[0]+1
    arr[c0]=(arr[c0-1]+arr[c0+1])/2
    return arr
