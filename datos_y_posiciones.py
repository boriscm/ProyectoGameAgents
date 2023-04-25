
def analisis_imagen(state):
     #mi posicion
    posicion_nave = (-1,-1)
    negro = True
    pos_x = 0
    for y in range(len(state[181])):
        color = state[181   ][y]
        valor =str(color[0])+"-"+str(color[1])+"-"+str(color[2])
        if( valor != "0-0-0"  and valor !="210-164-74"):
            if(negro):
                pos_x+=y
                negro = False
        else:
            if(not negro):
                posicion_nave = (181, int((pos_x+y-1)/2))
                pos_x=0
                break

            negro = True
    
    
    
    
    posiciones = {}

    #posicion de cada alien y numero de aliens por fila
    filas = [23,35,47,59,71,83]
    filas_aliens = {}
    lista = []
    negro = True
    pos_x = 0
    distancia = 0
    for y in filas:
        filas_aliens[y] = 0
        final = 0
        for x in range(len(state[y])):
            color = state[y][x]
            valor =str(color[0])+"-"+str(color[1])+"-"+str(color[2])

            if(valor == "0-0-0"):
                distancia+=1

            if( valor != "0-0-0"  and valor !="210-164-74"):
                distancia = 0
                final = x

                if(negro):
                    pos_x+=x
                    filas_aliens[y] +=1
                    negro = False
            
            else:

                if(distancia >5):
                    if(not negro):
                        posiciones[len(posiciones)] = (y, int((pos_x+final)/2))
                        lista.append(int((pos_x+final)/2))
                        pos_x=0

                        negro = True
                    else:
                        negro = True


    while(len(lista)<35):
        lista.append(-1)

       
    return [posicion_nave[1]]+lista

