
async def par(numero):
    if numero == 0:
        return 0
    elif numero % 2 == 0:
        return True
    else:
        return False

    
def formata(number):
    a = f"{number:,}"
    maketrans = a.maketrans
    final = a.translate(maketrans(',.', '.,', ' '))
    return final.replace(',', ", ")
