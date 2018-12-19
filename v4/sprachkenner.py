import numpy as np

refhoch = np.load('experiment 2a/refhoch.npy')
reftief = np.load('experiment 2a/reftief.npy')
refrechts = np.load('experiment 2a/refrechts.npy')
reflinks = np.load('experiment 2a/reflinks.npy')
def spracherkenner(name,person):
    for i in range(1,6):
        test = np.load('Spek/spek'+str(name)+str(i)+'t'+str(person)+'.npy')
        korrcoefh = np.corrcoef(refhoch, y = test)
        korrcoeft = np.corrcoef(reftief, y = test)
        korrcoefr = np.corrcoef(refrechts, y = test)
        korrcoefl = np.corrcoef(reflinks, y = test)
        a = np.max([np.mean(korrcoefh), np.mean(korrcoeft), np.mean(korrcoefr), np.mean(korrcoefl)])
        if a == np.mean(korrcoefh):
            print('hoch')
        elif a == np.mean(korrcoeft):
            print('tief')
        elif a == np.mean(korrcoefr):
            print('rechts')
        elif a == np.mean(korrcoefl):
            print('links')
            
spracherkenner('links','p')
print("----")
spracherkenner('links','s')


#def spracherkenner(ref, test):
#    return np.corrcoef(ref, y = test),