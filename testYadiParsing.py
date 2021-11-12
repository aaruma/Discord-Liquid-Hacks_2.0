import json

with open('data.json') as f:
    read = json.load(f)
    if ('Work' in read):
        print("YES")

        # shud print the whole thing for each calendar
        for j in read['Work']:
            # print(j)
            # shud print all the event info combined
            for k in j:
                # print(k)
                print(j[k]['Description'])
                continue


    # for i in read:
    #     # print(i)
    #     for k in read[i]:            
    #         # print(k)
    #         for l in k:
    #             # print(l)
    #         # for k in j:
    #             # print(j[k]['Description'])

