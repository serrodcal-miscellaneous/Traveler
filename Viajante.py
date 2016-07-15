import math
import random

andalucia={"almeria": (409.5,93), "cadiz": (63,57), "cordoba": (198,207), "granada": (309,127.5), "huelva": (3,139.5), "jaen": (295.5,192), "malaga": (232.5,75), "sevilla": (90,135)}

def sorteo(probabilidad):
    return (random.random() < probabilidad)

def distancia_euc2D(c1, c2, coords):
    coord_c1 = coords[c1]
    coord_c2 = coords[c2]
    return math.hypot(coord_c1[0]-coord_c2[0], coord_c1[1]-coord_c2[1])

def distanciaTotal(circuito, coords):
    return sum(distancia_euc2D(circuito[i], circuito[i+1], coords) for i in range(len(circuito)-1)) + distancia_euc2D(circuito[-1], circuito[0], coords)

class Problema_Busqueda_Local(object):

    def __init__(self, mejor = lambda x,y: x<y):
        self.mejor = mejor

    def genera_estado_inicial(self):
        pass

    def genera_sucesor(self, estado):
        pass

    def valoracion(self, estado):
        pass

class Viajante_BL(Problema_Busqueda_Local):

    def __init__(self, ciudades, distancias):
        super(Viajante_BL, self).__init__()
        self.ciudades = ciudades
        self.distancias = distancias

    def genera_estado_inicial(self):
        circuito = list(self.ciudades)
        random.shuffle(circuito)
        return circuito

    def genera_sucesor(self, estado):
        num = len(estado)
        origen = random.choice(range(num))
        lon = random.choice(range(2, num+1))
        res = estado[origen:] + estado[0:origen]
        return res[lon-1::-1] + res[lon:]

    def valoracion(self, estado):
        return distanciaTotal(estado, self.distancias)

def aceptar_e_s(candidato, valor, T, mejor):
    return (mejor(candidato, valor) or sorteo(math.exp(-abs(candidato-valor)/T)))

def enfriamiento_simulado(problema, t_inicial, factor_descenso, n_enfriamientos, n_iteraciones):
    actual=problema.genera_estado_inicial()
    valor_actual=problema.valoracion(actual)
    mejor=actual
    valor_mejor=valor_actual
    T=t_inicial
    for _ in range(n_enfriamientos):
        for _ in range(n_iteraciones):
            candidata = problema.genera_sucesor(actual)
            valor_candidata = problema.valoracion(candidata)
            if aceptar_e_s(valor_candidata, valor_actual, T, problema.mejor):
                actual=candidata
                valor_actual=valor_candidata
                if problema.mejor(valor_actual, valor_mejor):
                    mejor = actual
                    valor_mejor = valor_actual
            T *= factor_descenso
        return (mejor, valor_mejor)

if __name__ == '__main__':
    viajante_andalucia = Viajante_BL(andalucia.keys(), andalucia)
    print (enfriamiento_simulado(viajante_andalucia, 1000, 0.95, 100, 100))