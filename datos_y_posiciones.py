import threading


from threading import Thread
 
class CustomThread(Thread):
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs={}, Verbose=None):
        Thread.__init__(self, group, target, name, args, kwargs)
        self._return = None
 
    def run(self):
        if self._target is not None:
            self._return = self._target(*self._args, **self._kwargs)
             
    def join(self, *args):
        Thread.join(self, *args)
        return self._return




def posicion_de_nave(state):

    posicion_nave = (0,0)
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
    return  posicion_nave

def posicion_aliens(state):
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
                        lista.append(y)
                        lista.append(int((pos_x+final)/2))
                        pos_x=0

                        negro = True
                    else:
                        negro = True

    while(len(lista)<(35*2)):
        lista.append(0)
        lista.append(0)
    return  lista

def posicion_balas_propias(state):
        #balas del personaje
    balas = []
    
    rango = [16, 170]
    colores = {}

    for y in range(20,159):
        for x in range(16,144):
            color = state[y][x]
            valor =str(color[0])+"-"+str(color[1])+"-"+str(color[2])
            if( valor == "210-164-74" ):  
                balas.append(x)
                balas.append(y)
    while(len(balas)< 20):
        balas.append(0)
        balas.append(0)
    return balas



def posicion_balas_enemigas_y_nave_des(state):
    #posicion balas enemigas
    pos_enem_balas = []
    colores_bala=["228-111-111"]
    #enemigo mas cercano que se desplaza hacia abajo
    enemigo = [0,0]

    info = {}
    for y in reversed(range(90, 190)):

        for x in range(16,144):      
            color = state[y][x]
            valor =str(color[0])+"-"+str(color[1])+"-"+str(color[2])
            if valor in colores_bala:
                color1 = state[y+1][x]
                valor1 = str(color1[0])+"-"+str(color1[1])+"-"+str(color1[2])
                color2 = state[y+1][x]
                valor2 = str(color2[0])+"-"+str(color2[1])+"-"+str(color2[2])     
                if(valor1 in colores_bala or valor2 in colores_bala):
                    pos_enem_balas+=[x,y]

            elif( enemigo[0] == 0 and valor != "0-0-0"  and valor !="210-164-74" and valor !="214-214-214" and valor !="236-236-236"):
                
                next_col = x
                for rec in range(1,10):
                    color1 = state[y][x+rec]
                    valor1 = str(color1[0])+"-"+str(color1[1])+"-"+str(color1[2])
                    if(valor1 != "0-0-0"  and valor1 !="210-164-74" and valor1 !="214-214-214" and valor1 !="236-236-236" and valor1 not in colores_bala):
                        next_col = x + rec
                enemigo = [y, int((x+next_col)/2)]
    while(len(pos_enem_balas) <18):
        pos_enem_balas.append(0)
        pos_enem_balas.append(0)
    
    return pos_enem_balas + enemigo
    


def obtener_datos(state):

    d_t1, d_t2, d_t3, d_t4 =[[],[],[],[]]

    t1 = CustomThread(target=posicion_de_nave, args=([state]))
    t2 = CustomThread(target=posicion_aliens,args=([state]))
    t3 = CustomThread(target=posicion_balas_propias,args=([state]))
    t4 = CustomThread(target=posicion_balas_enemigas_y_nave_des, args=([state]))

    t1.start()
    t2.start()
    t3.start()
    t4.start()


    d_t1 =t1.join()
    d_t2 = t2.join()
    d_t3 =t3.join()
    d_t4 =t4.join()


    return[d_t1[0], d_t1[1]]+ d_t3 + d_t2 +d_t4


def analisis_imagen(state):
     #mi posicion
    posicion_nave = (0,0)
    negro = True
    pos_x = 0
    for y in range(len(state[181])):
        color = state[181][y]
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
                        lista.append(y)
                        lista.append(int((pos_x+final)/2))
                        pos_x=0

                        negro = True
                    else:
                        negro = True

    #balas del personaje
    balas = []
    
    rango = [16, 170]
    colores = {}

    for y in range(20,159):
        for x in range(16,144):
            color = state[y][x]
            valor =str(color[0])+"-"+str(color[1])+"-"+str(color[2])
            if( valor == "210-164-74" ):  
                balas.append(x)
                balas.append(y)
    while(len(balas)< 20):
        balas.append(0)
        balas.append(0)
    


    balas_enemiga = {}
    #posicion balas enemigas
    pos_enem_balas = []
    colores_bala=["228-111-111"]
    #enemigo mas cercano que se desplaza hacia abajo
    enemigo = [0,0]

    info = {}
    for y in reversed(range(90, 190)):

        for x in range(16,144):      
            color = state[y][x]
            valor =str(color[0])+"-"+str(color[1])+"-"+str(color[2])
            if valor in colores_bala:
                color1 = state[y+1][x]
                valor1 = str(color1[0])+"-"+str(color1[1])+"-"+str(color1[2])
                color2 = state[y+1][x]
                valor2 = str(color2[0])+"-"+str(color2[1])+"-"+str(color2[2])     
                if(valor1 in colores_bala or valor2 in colores_bala):
                    pos_enem_balas+=[x,y]

            elif( enemigo[0] == 0 and valor != "0-0-0"  and valor !="210-164-74" and valor !="214-214-214" and valor !="236-236-236"):
                
                next_col = x
                for rec in range(1,10):
                    color1 = state[y][x+rec]
                    valor1 = str(color1[0])+"-"+str(color1[1])+"-"+str(color1[2])
                    if(valor1 != "0-0-0"  and valor1 !="210-164-74" and valor1 !="214-214-214" and valor1 !="236-236-236" and valor1 not in colores_bala):
                        next_col = x + rec
                enemigo = [y, int((x+next_col)/2)]
                

    while(len(pos_enem_balas) <18):
        pos_enem_balas.append(0)
        pos_enem_balas.append(0)

    while(len(pos_enem_balas) >18):
        pos_enem_balas.pop(len(pos_enem_balas)-1)

    while(len(balas)< 20):
        balas.append(0)
        balas.append(0)
    while(len(balas) >20):
        balas.pop(len(balas)-1)


    while(len(lista)<(35*2)):
        lista.append(0)
        lista.append(0)

    while(len(lista) >70):
        lista.pop(len(list)-1)

       
    return [posicion_nave[0],posicion_nave[1]] + balas + lista + pos_enem_balas + enemigo

