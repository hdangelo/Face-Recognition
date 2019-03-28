class flabianos:
    """ Lista de invitados a la cena del señor en el laboratorio """

    def __init__(self):
        self.Invitados=['Hernan','Sergio','Sebastia','Mario','Efra']

    def TuSiTuNo(self,EllosSi):        
        if EllosSi in self.Invitados:
            return('Bienvenido {}'.format(EllosSi))
        else:
            return('Lo siento {}, no te conozco'.format(EllosSi))
