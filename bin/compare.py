def compare(instance,epsilon):
    cr_list = [plane[0] for plane in instance] # list of consumption rate
    r = ceil(log(max(cr_list),1+epsilon)) # number of classes
    print(r)
    for i in range(1,r+1):
        print((1+epsilon)**i)
    print('\n\n')
    L = 2**(floor(log(total_cr,2))+1)
    print(L)
    for i in range(1,L+1):
        print(epsilon*2**i/r)
