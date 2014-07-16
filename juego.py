import sys

sys.path.append(".")
sys.path.append("..")
import pilasengine

pilas = pilasengine.iniciar(capturar_errores=False)
pilas.depurador.definir_modos(fisica=False)

import random



class EscenaJuego(pilasengine.escenas.Escena):

    def iniciar(self):
        enemigos = []
        pilas.fondos.Fondo("fondo.png")
        self.musica=pilas.musica.cargar("musica.mp3")
        self.musica.reproducir()

        class Puntaje(pilasengine.actores.Texto):

                def __init__(self, pilas, x=0, y=0):
                        pilasengine.actores.Texto.__init__(self, pilas, "0", x, y)
                        self.valor = 0
                        self.escala=2
                def aumentar(self):
                        self.valor += 1
                        self.texto = "TIME:" + str(self.valor)
                        

        p = Puntaje(pilas)
        p.y=219
        p.x=-296
        p.z=-50
        def aumentar_puntaje():
            p.aumentar()
        pilas.escena_actual().tareas.siempre(1,aumentar_puntaje)

        class protagonista(pilasengine.actores.Actor):

                def iniciar(self):
                        self.imagen="normal.png"
                        self.escala=1
                        #self.aprender(pilas.habilidades.MoverseConElTeclado)
                        self.definir_area_colision(0,0,80,125)
                        self.y=280

                def actualizar(self):
                        self.y-=1

                        velocidad_x = self.pilas.pad.x * 4
                        velocidad_y = self.pilas.pad.y * 4
                        if velocidad_x >0:
                            self.imagen="derecha.png"
                        if velocidad_x ==0:
                            self.imagen="normal.png"
                        if velocidad_x <0:	
                            self.imagen="izquierda.png"
                        if velocidad_y >0:
                            self.imagen="sopla arriba.png"
                        if velocidad_y <0:	
                            self.imagen="abajo.png"
	
                        self.x += velocidad_x
                        self.y += velocidad_y

                        if self.y<-320:
                                self.y=250
                        if self.y>320:
                                self.y=-250
                        if self.x<-400:
                                self.x=300
                        if self.x>400:
                                self.x=-300

        player = protagonista(pilas)

        class avion(pilasengine.actores.Actor):

                def iniciar(self):
                        self.imagen="eli 2.png"
                        self.escala=1
                        self.x=430
                        self.y=random.choice([230,130,30,-130,-230])
                        self.definir_area_colision(0,0,190,100)

                def actualizar(self):
                        self.x -=2
                        
                        if self.x<-450:
                                self.eliminar()


        def crear_avion():
            un_avion=avion(pilas)
            enemigos.append(un_avion)

        pilas.escena.tareas.siempre(2.8,crear_avion)

        class pajaro(pilasengine.actores.Actor):

                def iniciar(self):
                        self.imagen=pilas.imagenes.cargar_grilla("pajaro_animado_2.png",8)
                        self.escala=0.7
                        self.x=-430
                        self.y=random.choice([200,150,50,0,-50,-150,-200])
                        self.demora = 3
                        self.definir_area_colision(0,0,65,40)

                def actualizar(self):
                        self.x -=-2
                        self.demora -= 1
                        if self.x>350:
                                self.eliminar()

                        if self.demora == 0:
                                self.imagen.avanzar()
                                self.demora = 3

        def crear_pajaro():
            un_pajaro=pajaro(pilas)
            enemigos.append(un_pajaro)

        pilas.escena.tareas.siempre(2.8,crear_pajaro)

        class AnticipacionNube(pilasengine.actores.Actor):
            def iniciar(self):
                self.imagen = "nube 0.png"
                self.transparencia = 100
				
            def actualizar(self):
                self.transparencia -= 0.8

        nube=pilas.actores.Actor()
        nube.imagen="nube 0.png"
        nube.escala=1
        nube.definir_area_colision(0,0,180,67)

        def mover_nube():
                pos_y=random.choice([128,177,-128,-177,11])
                pos_x=random.choice([227,-225,-227,225,-83])
                nube.x = -600
                nube.y = -600
                a=AnticipacionNube(pilas)
                a.x = pos_x
                a.y = pos_y
                
                def mover():
                    nube.x = pos_x
                    nube.y = pos_y
                    a.eliminar()
                    
                pilas.escena.tareas.una_vez(2, mover)
				
        mover_nube()



        pilas.escena.tareas.siempre(5,mover_nube)
        pilas.escena.colisiones.agregar(player, nube, choque)
        pilas.escena.colisiones.agregar(player,enemigos, choque)


class EscenaGameOver(pilasengine.escenas.Escena):

    def iniciar(self):
        gameover=pilas.actores.Actor()
        gameover.imagen="gameover.png"
        gameover.z=-1000
        gameover.transparencia=100
        gameover.transparencia=[0]

        self.pulsa_boton.conectar(self.adelantar)

    def adelantar(self, data):
        escena = EscenaJuego(pilas)
        pilas.escenas.definir_escena(escena)



def choque(player, nube):
    player.eliminar()

    escena = EscenaGameOver(pilas)
    pilas.escenas.definir_escena(escena)



escena = EscenaJuego(pilas)
pilas.escenas.definir_escena(escena)
pilas.ejecutar()
