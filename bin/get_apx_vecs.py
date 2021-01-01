def get_apx_vecs(instance,epsilon): # return a set of all approximate vectors
    cr_list = [plane[0] for plane in instance] # list of consumption rate
    r = ceil(log(max(cr_list),1+epsilon)) # number of classes
    N = get_max_vec(instance,epsilon)
    vec_list = get_vecs(instance,epsilon)
    apx_vec_list = [tuple([0 for i in range(r)])]
    vec_list.pop(0)
    for vec in vec_list:
        total_cr = sum((1+epsilon)**j*vec[j] for j in range(r))
        C_star = 2**(floor(log(total_cr,2)))
        base = epsilon*C_star/r
        apx_vec = tuple([min(floor(ceil((1+epsilon)**(j+1)*vec[j]/base)*base/(1+epsilon)**(j+1)),N[j]) for j in range(r)])
        if apx_vec not in apx_vec_list:
            apx_vec_list.append(apx_vec)
        else:
            print('Awesome!!!')
    return apx_vec_list
