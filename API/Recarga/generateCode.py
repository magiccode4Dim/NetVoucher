import random
from uuid import uuid4

INTERVAL_BEGIN = 100000000000
INTERVAL_END =  999999999999

def generate_unique_code_byrandom(codelist):
        availablesotps = list()
        for codeOb in codelist:
            availablesotps.append(codeOb.code)
        while True:    
            newcode = random.randint(INTERVAL_BEGIN,INTERVAL_END)
            if newcode not in availablesotps:
                return str(newcode)


#gera chaves de agentes para criacao de contas
#pode utilizar uma ou mais listas como base
def generate_random_key_byuuid(baseLists):
    availablestokens = list()
    for baseList in baseLists:
        for t in baseList:
            availablestokens.append(t.code)
    while True:
        rand_token = uuid4()
        token = str(rand_token)
        if token not in availablestokens:
            return token