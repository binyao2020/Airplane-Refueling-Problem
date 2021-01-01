def dynamic_prog(instance,epsilon):
    instance_dict = sort_volume(instance,epsilon)
    apx_vec_list = get_apx_vecs(instance,epsilon)
    val_list = [0 for apx_vec in apx_vec_list] # stores the value for each vector
    pred_list = [0 for apx_vec in apx_vec_list] # stores the index of predecessor for each vector
    total_cr_list = [0 for apx_vec in apx_vec_list]
    for i in range(len(apx_vec_list)):
        for j in range(i):
            vec = apx_vec_list[i]
            pred_vec = apx_vec_list[j]
            flag = True
            for k in range(r):
                if pred_vec[k] > vec[k]:
                    flag = False
            if flag == False:
                continue
            else:
                add_value = 0
                u = total_cr_list[j]
                for k in range(r):
                    for l in range(pred_vec[k]+1,vec[k]+1):
                        u += (1+epsilon)**(k+1)
                        add_value += instance_dict[k][l][1]/u
                if val_list[j]+add_value > val_list[i]:
                    val_list[i] = val_list[j]+add_value
                    pred_list[i] = j
                    total_cr_list[i] = u
    return val_list,pred_list
