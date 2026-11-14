from .reta import Reta

class RetaR2(Reta):

    __slots__ = ("_ponto_inicial", "_ponto_final")

    
    def __init__(self, ponto_inicial, ponto_final):
        self.ponto_inicial = ponto_inicial
        self.ponto_final = ponto_final

    @Reta.ponto_inicial.setter
    def ponto_inicial(self, ponto_inicial):
        try:
            x_inicial, y_inicial = ponto_inicial
            x_inicial = float(x_inicial)
            y_inicial = float(y_inicial)

            if len(ponto_inicial) == 2:
                self._ponto_inicial = (x_inicial, y_inicial)

            else:
                raise ValueError("O ponto deve ter uma coordenada X e uma coordenada Y.")

        except ValueError as erro:
            raise ValueError(f"Erro de execução: {erro}")

    @property
    def ponto_final(self):
        return self._ponto_final

    @ponto_final.setter
    def ponto_final(self, ponto_final):
        try:
            x_final, y_final = ponto_final
            x_final = float(x_final)
            y_final = float(y_final)

            if len(ponto_final) == 2:
                self._ponto_final = (x_final, y_final)

            else:
                raise ValueError("O ponto deve ter uma coordenada X e uma coordenada Y.")

        except ValueError as erro:
            print(f"Erro na execução: {erro}")
        
    @property
    def vetor_diretor(self):
        x_inicial, y_inicial = self.ponto_inicial
        x_final, y_final = self.ponto_final

        return x_final - x_inicial, y_final - y_inicial

    def equacao_reduzida(self):
        try:
            x_inicial, y_inicial = self.ponto_inicial
            
            x_final, y_final = self.ponto_final

            if x_final == x_inicial:
                return f"X = {x_inicial}"

            if self.ponto_inicial == self.ponto_final:
                raise ValueError("Os pontos não podem ser idênticos.")
            
            m = (y_final - y_inicial) / (x_final - x_inicial)

            b = y_inicial - m * x_inicial

            return f"y = {m}x {b:+}"
        except ValueError as erro:
            print(f"Erro na execução")


    def equacao_simetrica(self):
        x_inicial, y_inicial = self.ponto_inicial
                
        x_final, y_final = self.ponto_final

        x_vet_dir,y_vet_dir = self.vetor_diretor

        if x_inicial and y_final >= 0:
            return f"{x_final} - {x_inicial} / {x_vet_dir} = {y_final} - {y_inicial} / {y_vet_dir}"
        elif x_inicial <= 0:
            return f"{x_final} - ({x_inicial}) / {x_vet_dir} = {y_final} - {y_inicial} / {y_vet_dir}"
        elif y_inicial <= 0:
            return f"{x_final} - {x_inicial} / {x_vet_dir} = {y_final} - ({y_inicial}) / {y_vet_dir}"
        elif x_inicial and y_inicial <= 0:
            return f"{x_final} - ({x_inicial}) / {x_vet_dir} = {y_final} - ({y_inicial}) / {y_vet_dir}"
        