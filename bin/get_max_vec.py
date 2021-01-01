def get_max_vec(instace,epsilon): # return the vector corresponds to the structured instance
    cr_list = [plane[0] for plane in instance] # list of consumption rate
    r = ceil(log(max(cr_list),1+epsilon)) # number of classes
    class_list = [] #records the type of each plane
    N = [] # number of planes for each class
    for j in range(len(instance)):
        class_list.append(floor(log(cr_list[j],1+epsilon))) #plane -> class
    for i in range(r):
        N.append(class_list.count(i))
    return N
