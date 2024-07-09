
def howManyGroups(n,m):
    
    #can only be one way of group n = 0 elements
    if n == 0:
        return 1
    
    #cannot group if elements per group is not given, or if there are negative elements
    if m == 0 or n < 0:
        return 0
    
    #recursion step from looking at pattern of groups
    return howManyGroups(n, m-1) + howManyGroups(n-m, m)
