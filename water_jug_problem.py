def w_p(cap1,cap2,goal):
    stack=[]
    v=set()

    stack.append((0,0))
    v.add((0,0))
    act=[]
    while stack:
        j1,j2=stack.pop()
        act.append((j1,j2))

        if j1==goal or j2 == goal:
            print("perfect solution found")
            for act in act:
                print(act)
            return True
        
        rules =[
            (cap1,j2),#filling jug one
            (j1,cap2),#filling jug two
            (0,j2),#empty jug1
            (j1,0),#empty jug2
            (j1 - min(j1,cap2 -j2),j2+ min(j1,cap2-j2)),#pour jug 1 into jug2 untill jug2 is full
            (j1 +min(j2,cap1-j1),j2 -min(j2,cap1-j1)),#pour jug 2 untill jug 1 is full
            (0, j1 + j2) if j1 + j2 <= cap2 else (j1 + j2 - cap2, cap2),  # Pour Jug 1 into Jug 2 until empty
            (j1 + j2, 0) if j1 + j2 <= cap1 else (cap1, j1 + j2 - cap1)  #  Pour Jug 2 into Jug 1 until empty
        ]

        for state in rules:
            if state not in v:
                v.add(state)
                stack.append(state)
    print("no solution found")
    return False
jug_1=7
jug_2=3
target=2
w_p(jug_1,jug_2,target)            