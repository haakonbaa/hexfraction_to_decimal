def divisjon(a, b, presisjon):
    num = ""
    while len(num) < presisjon:
        c = a // b
        num += str(c)
        a = 10*(a-b*c)
    return num

def sum(l):
    s = 0
    n = ""
    for i in range(len(l[1])-1,-1,-1):
        for j in range(0,len(l)):
            s += int(l[j][i])
        c = s % 10
        n = str(c) + n
        s = s // 10
    return n

def hex_til_tital(h,presisjon):
    d = []
    h = h.replace(".","")
    for i in range(len(h)):
        d.append(divisjon(int(h[i],16),16**(i+1),presisjon) )
    return sum(d)


print(hex_til_tital("243f6a8885a308d313198a2e03707344a4093822299f3",200))
