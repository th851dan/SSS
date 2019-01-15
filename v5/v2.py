def quanfehler(max, min, n):
    return (max - min) / 2^n

ref = [1.039,2.001,3.06,4.07,5.082,5.998,7.01,8.022,8.986,9.999]
AD = [1.035156250, 1.992187500,3.007812500, 4.062500000, 5.078125000, 5.986328125, 7.050781250, 8.066406250, 9.082031250, 9.980468750]
phi = [1.09, 2, 3.08, 4.09, 5.09, 6.05, 7.06, 8.08, 9.09, 9.69]
def messfehler(ref, u):
    a = []
    for i in range(10):
        a.append(ref[i] - u[i])
    return a
mfAD = messfehler(ref, AD)
mfphi = messfehler(ref, phi)
print(mfAD)
print(mfphi)