def greedy(f,p,m,h):
    c = 0
    while (c < m):
        fxy = -f(p)
        fpxpy = -f([p[0] + h, p[1]])
        fpxmy = -f([p[0] - h, p[1]])
        fpxyp = -f([p[0], p[1] + h])
        fpxym = -f([p[0], p[1] - h])
        if fpxpy >= fxy and fpxpy >= fpxmy and fpxpy >= fpxyp and fpxpy >= fpxym:
            p = [p[0] + h, p[1]]
        elif fpxmy >= fxy and fpxmy >= fpxpy and fpxmy >= fpxyp and fpxmy >= fpxym:
            p = [p[0] - h, p[1]]
        elif fpxyp >= fxy and fpxyp >= fpxmy and fpxyp >= fpxpy and fpxyp >= fpxym:
            p = [p[0], p[1] + h]
        elif fpxym >= fxy and fpxym >= fpxmy and fpxym >= fpxpy and fpxym >= fpxyp:
            p = [p[0], p[1] - h]
        else:
            break
        c += 1
        print(f'Step {c}: f(p)={fxy:.2f} p={p}')
    return p
