# Oppgave A

n = float(input("Gi inn er desimaltall: "))
d = int(input("Antall desimaler i avrunding: "))
# deler eller ganger tallet slik at det kan "ceil-es" (tilsvarende: (x-0.5)//1+1 )
# ganger eller deler tallet slik at det blir like stort som det var orginalt
print(f"Avrundet til {d} desimaler {((n*(10**d)-0.5)//1+1)/(10**d)}")

# Oppgave B

a = input("Oppgi heltallsdelen av tallet (det foran punktum): ")
b = input("Oppgi desimaldelen av tallet (det bak punktum): ")
d = int(input("Oppgi ønsket antall desimaler i avrunding: "))

len_a, len_b = len(a), len(b)
a, b = int(a), int(b)

# lager en stor int av 'a' og 'b' som er str(a) + str(b)
# Denne kan enkelt avrundes med round funksjonen
c = str(round(b + a * (10 ** len_b),-len_b+d))
# Setter komma på riktig plass og gjør om til float
n = float(c[:len_a] + "." + c[len_a:])
print(f"{a}.{b} avrundet til {d} desimaler blir {n}")
