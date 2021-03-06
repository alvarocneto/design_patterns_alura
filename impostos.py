from abc import ABCMeta, abstractclassmethod


def IPVX(metodo_funcao):
    """Exemplo de implementação de decorator"""
    def decorador(self, orcamento):
        return metodo_funcao(self, orcamento) + 50
    return decorador


class Imposto(metaclass=ABCMeta):
    def __init__(self, outro_imposto=None):
        self.__outro_imposto = outro_imposto

    @abstractclassmethod
    def calcula(self, orcamento):
        pass

    def calculo_do_outro_imposto(self, orcamento):
        if self.__outro_imposto is None:
            return 0
        else:
            return self.__outro_imposto.calcula(orcamento)


class Template_de_imposto_condicional(Imposto, metaclass=ABCMeta):

    def calcula(self, orcamento):
        if self.deve_usar_maxima_taxacao(orcamento):
            return self.maxima_taxacao(orcamento) + self.calculo_do_outro_imposto(orcamento)
        else:
            return self.minima_taxacao(orcamento) + self.calculo_do_outro_imposto(orcamento)

    @abstractclassmethod
    def deve_usar_maxima_taxacao(self, orcamento):
        pass

    @abstractclassmethod
    def maxima_taxacao(self, orcamento):
        pass

    @abstractclassmethod
    def minima_taxacao(self, orcamento):
        pass


class ISS(Imposto):
    @IPVX
    def calcula(self, orcamento):
        return orcamento.valor * 0.1 + self.calculo_do_outro_imposto(orcamento)


class ICMS(Imposto):
    def calcula(self, orcamento):
        return orcamento.valor * 0.06 + self.calculo_do_outro_imposto(orcamento)


class ICPP(Template_de_imposto_condicional):

    def deve_usar_maxima_taxacao(self, orcamento):
        return orcamento.valor > 500

    def maxima_taxacao(self, orcamento):
        return orcamento.valor * 0.07

    def minima_taxacao(self, orcamento):
        return orcamento.valor * 0.05


class IKCV(Template_de_imposto_condicional):

    def deve_usar_maxima_taxacao(self, orcamento):
        return orcamento.valor > 500 and self.__tem_item_maior_que_100(orcamento)

    def maxima_taxacao(self, orcamento):
        return orcamento.valor * 0.1

    def minima_taxacao(self, orcamento):
        return orcamento.valor * 0.06

    def __tem_item_maior_que_100(self, orcamento):
        for item in orcamento.obter_itens():
            if item.valor > 100:
                return True
        return False



