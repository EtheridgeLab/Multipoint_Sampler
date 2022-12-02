
# This function returns a time duration based on a distance entered by the user

distance = int      # Length entered by user
seconds = int       # Time necessary to prime based on tubing length

def set_time_auto(distance): 

    while True:
        if 0 < distance <= 25:
            seconds = 8 #80
            break
        elif 25 < distance <= 50:
            seconds = 14 #140
            break
        elif 50 < distance <= 75:
            seconds = 20 #200
            break
        elif 75 < distance <= 100:
            seconds = 25 #250
            break
 
    return seconds


# min = ''
# adv_st = ''
# hr = ''
 
# if min + adv_st > 59:
#     if min <= 9:
#         gen_st = str(hr + 1) + ':' + '0' + str(min + adv_st - 60)
#     else:
#         gen_st = str(hr + 1) + ':' + str(min + adv_st - 60)
# else:
#     if min <= 9:
#         gen_st = str(hr) + ':' + '0' + str(min + adv_st)
#     else:
#         gen_st = str(hr) + ':' + str(min + adv_st)