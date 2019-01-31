n=3
def count(n):
    if n > 0:
        print(n)
        count(n-1)
    else:
        print("Blast off!")
count(3)
