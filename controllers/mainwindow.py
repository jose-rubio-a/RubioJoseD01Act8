from random import randint
import time
from pynput import keyboard
from PySide2.QtWidgets import QMainWindow, QHeaderView, QTableWidgetItem, QApplication
from views.Ui_main import Ui_MainWindow
from PySide2.QtCore import Slot

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.columnasTablas()
        self.interrupcion = False
        self.pausa = False
        self.continuar = True
        self.error = False
        self.boolEjecucion = False
        self.booltablaBCP = False

        def pulsa(tecla):
            if tecla == keyboard.KeyCode.from_char('i') or tecla == keyboard.KeyCode.from_char('I'):
                if not self.pausa and self.boolEjecucion:
                    self.interrupcion = True
            elif tecla == keyboard.KeyCode.from_char('p') or tecla == keyboard.KeyCode.from_char('P'):
                if not self.pausa and self.boolEjecucion:
                    self.pausa = True
            elif tecla == keyboard.KeyCode.from_char('c') or tecla == keyboard.KeyCode.from_char('C'):
                if (self.pausa and self.boolEjecucion) or self.booltablaBCP:
                    self.continuar = False
            elif tecla == keyboard.KeyCode.from_char('e') or tecla == keyboard.KeyCode.from_char('E'):
                if not self.pausa and self.boolEjecucion:
                    self.error = True
            elif tecla == keyboard.KeyCode.from_char('t') or tecla == keyboard.KeyCode.from_char('T'):
                if not self.pausa and self.boolEjecucion:
                    self.booltablaBCP = True
                else:
                    self.mostrar_tablaBCP()
            elif tecla == keyboard.KeyCode.from_char('n') or tecla == keyboard.KeyCode.from_char('N'):
                self.crear_proceso()
                
        self.escuchador = keyboard.Listener(pulsa)
        self.escuchador.start()

        self.numeroProcesos = 0
        self.procesoActual = 1
        self.numeroEjecucion = 0
        self.tiempoTotal = 0
        self.listaRegistro = []
        self.listaEjecuccion = []
        self.listaTerminados = []
        self.listabloqueados = []
        self.tablaBCP = []

        self.ui.Empezar_pushButton.clicked.connect(self.empezar)
        self.ui.iniciar_pushButton.clicked.connect(self.iniciar)
    
    def llenarTablaRegistro(self):
        self.ui.captura_tableWidget.setRowCount(len(self.listaRegistro))

        for (index_row, row) in enumerate(self.listaRegistro):
            self.ui.captura_tableWidget.setItem(index_row,0,QTableWidgetItem(str(row['Id'])))
            self.ui.captura_tableWidget.setItem(index_row,1,QTableWidgetItem(str(row['operacion'])))
            self.ui.captura_tableWidget.setItem(index_row,2,QTableWidgetItem(str(row['tiempo'])))
    
    def llenarTablaEjecucion(self):
        self.ui.ejecuccion_tableWidget.setRowCount(len(self.listaEjecuccion))

        for (index_row, row) in enumerate(self.listaEjecuccion):
            self.ui.ejecuccion_tableWidget.setItem(index_row,0,QTableWidgetItem(str(row['Id'])))
            self.ui.ejecuccion_tableWidget.setItem(index_row,1,QTableWidgetItem(str(row['operacion'])))
            self.ui.ejecuccion_tableWidget.setItem(index_row,2,QTableWidgetItem(str(row['tiempo'])))
            self.ui.ejecuccion_tableWidget.setItem(index_row,3,QTableWidgetItem(str(row['restante'])))

    def llenarTablaTerminados(self):
        self.ui.finalizados_tableWidget.setRowCount(len(self.listaTerminados))

        for (index_row, row) in enumerate(self.listaTerminados):
            self.ui.finalizados_tableWidget.setItem(index_row,0,QTableWidgetItem(str(row['Id'])))
            self.ui.finalizados_tableWidget.setItem(index_row,1,QTableWidgetItem(str(row['operacion'])))
            self.ui.finalizados_tableWidget.setItem(index_row,2,QTableWidgetItem(str(row['resultado'])))
            self.ui.finalizados_tableWidget.setItem(index_row,3,QTableWidgetItem(str(row['tiempo_llegada'])))
            self.ui.finalizados_tableWidget.setItem(index_row,4,QTableWidgetItem(str(row['tiempo_finalizacion'])))
            self.ui.finalizados_tableWidget.setItem(index_row,5,QTableWidgetItem(str(row['tiempo_retorno'])))
            self.ui.finalizados_tableWidget.setItem(index_row,6,QTableWidgetItem(str(row['tiempo_respuesta'])))
            self.ui.finalizados_tableWidget.setItem(index_row,7,QTableWidgetItem(str(row['tiempo_espera'])))
            self.ui.finalizados_tableWidget.setItem(index_row,8,QTableWidgetItem(str(row['tiempo_servicio'])))
    
    def llenarTablaBloqueados(self):
        self.ui.bloqueados_tableWidget.setRowCount(len(self.listabloqueados))

        for (index_row, row) in enumerate(self.listabloqueados):
            self.ui.bloqueados_tableWidget.setItem(index_row,0,QTableWidgetItem(str(row['Id'])))
            self.ui.bloqueados_tableWidget.setItem(index_row,1,QTableWidgetItem(str(row['operacion'])))
            self.ui.bloqueados_tableWidget.setItem(index_row,2,QTableWidgetItem(str(row['bloqueado'])))
    
    def llenarTablaBCP(self):
        self.ui.BCP_tableWidget.setRowCount(len(self.tablaBCP))

        for (index_row, row) in enumerate(self.tablaBCP):
            self.ui.BCP_tableWidget.setItem(index_row, 0,QTableWidgetItem(str(row['Id'])))
            self.ui.BCP_tableWidget.setItem(index_row, 1,QTableWidgetItem(str(row['operacion'])))
            self.ui.BCP_tableWidget.setItem(index_row, 2,QTableWidgetItem(str(row['resultado'])))
            self.ui.BCP_tableWidget.setItem(index_row, 3,QTableWidgetItem(str(row['restante'])))
            self.ui.BCP_tableWidget.setItem(index_row, 4,QTableWidgetItem(str(row['bloqueado'])))
            self.ui.BCP_tableWidget.setItem(index_row, 5,QTableWidgetItem(str(row['tiempo_llegada'])))
            self.ui.BCP_tableWidget.setItem(index_row, 6,QTableWidgetItem(str(row['tiempo_finalizacion'])))
            self.ui.BCP_tableWidget.setItem(index_row, 7,QTableWidgetItem(str(row['tiempo_retorno'])))
            self.ui.BCP_tableWidget.setItem(index_row, 8,QTableWidgetItem(str(row['tiempo_respuesta'])))
            self.ui.BCP_tableWidget.setItem(index_row, 9,QTableWidgetItem(str(row['tiempo_espera'])))
            self.ui.BCP_tableWidget.setItem(index_row, 10, QTableWidgetItem(str(row['tiempo_servicio'])))
    
    def columnasTablas(self):
        self.ui.captura_tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.ui.ejecuccion_tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.ui.finalizados_tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.ui.bloqueados_tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.ui.BCP_tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        
    def bloqueados(self):
        for proceso in reversed(self.listabloqueados):
            proceso['bloqueado'] -= 1
            if proceso['bloqueado'] == 0:
                proceso['bloqueado'] = 0
                self.listaEjecuccion.append(self.listabloqueados.pop(self.listabloqueados.index(proceso)))
            self.llenarTablaBloqueados()
            self.llenarTablaEjecucion()
    
    def transicion(self):
        while len(self.listaEjecuccion) + len(self.listabloqueados) < 5 and len(self.listaRegistro):
            proceso = self.listaRegistro.pop(0)
            proceso['tiempo_llegada'] = self.tiempoTotal
            self.listaEjecuccion.append(proceso)
            self.llenarTablaRegistro()
            self.llenarTablaEjecucion()
    
    def calcular_tiempos(self, proceso):
        proceso['tiempo_finalizacion'] = self.tiempoTotal
        proceso['tiempo_retorno'] = proceso['tiempo_finalizacion'] - proceso['tiempo_llegada']
        proceso['tiempo_respuesta'] = proceso['tiempo_ejecucion'] - proceso['tiempo_llegada']
        proceso['tiempo_espera'] = proceso['tiempo_retorno'] - proceso['tiempo_servicio']
        return proceso
    
    def mostrar_tablaBCP(self, procesoEjecucion=None, j=None):
        self.tablaBCP.clear()
        self.tablaBCP.extend(self.listaRegistro)
        if self.boolEjecucion:
            procesoEjecucion['tiempo_servicio'] = procesoEjecucion['tiempo'] - j
            procesoEjecucion['tiempo_espera'] = self.tiempoTotal - procesoEjecucion['tiempo_llegada'] - procesoEjecucion['tiempo_servicio']
            self.tablaBCP.append(procesoEjecucion)
        for proceso in self.listaEjecuccion:
            proceso['tiempo_servicio'] = proceso['tiempo'] - proceso['restante']
            proceso['tiempo_espera'] = self.tiempoTotal - proceso['tiempo_llegada'] - proceso['tiempo_servicio']
            self.tablaBCP.append(proceso)
        for proceso in self.listabloqueados:
            proceso['tiempo_servicio'] = proceso['tiempo'] - proceso['restante']
            proceso['tiempo_espera'] = self.tiempoTotal - proceso['tiempo_llegada'] - proceso['tiempo_servicio']
            self.tablaBCP.append(proceso)
        self.tablaBCP.extend(self.listaTerminados)
        self.llenarTablaBCP()
    
    def ejecucion(self):
        self.boolEjecucion = True
        while len(self.listaEjecuccion) or len(self.listabloqueados):
            self.transicion()
            self.interrupcion = False
            self.error = False
            if len(self.listaEjecuccion):
                proceso = self.listaEjecuccion.pop(0)
                if not proceso['bandera_ejecucion']:
                    if self.tiempoTotal == 0:
                        proceso['tiempo_ejecucion'] = self.tiempoTotal
                        proceso['bandera_ejecucion'] = True
                    else:
                        proceso['tiempo_ejecucion'] = self.tiempoTotal
                        proceso['bandera_ejecucion'] = True
                self.llenarTablaEjecucion()
                self.ui.Id_label.setText(str(proceso['Id']))
                self.ui.operacion_label.setText(proceso['operacion'])
                self.ui.tiempo_label.setText(str(proceso['tiempo']))
                i = 0
                j = proceso['restante']
                while i <= proceso['restante']:
                    self.bloqueados()
                    self.ui.transcurrido_lcdNumber.display(i)
                    self.ui.restante_lcdNumber.display(j)
                    self.ui.total_lcdNumber.display(self.tiempoTotal)
                    QApplication.processEvents()
                    time.sleep(1)
                    if self.pausa:
                        while self.continuar:
                            pass
                        self.pausa = False
                        self.continuar = True
                    elif self.booltablaBCP:
                        self.mostrar_tablaBCP(proceso, j)
                        while self.continuar:
                            pass
                        self.booltablaBCP = False
                        self.continuar = True
                    elif self.interrupcion:
                        proceso['restante'] = j
                        proceso['bloqueado'] = 9
                        self.listabloqueados.append(proceso)
                        self.llenarTablaBloqueados()
                        self.ui.Id_label.setText("")
                        self.ui.operacion_label.setText("")
                        self.ui.tiempo_label.setText("")
                        self.ui.transcurrido_lcdNumber.display(0)
                        self.ui.restante_lcdNumber.display(0)
                        self.tiempoTotal += 1
                        break
                    elif self.error:
                        proceso['resultado'] = "Error"
                        proceso['tiempo_servicio'] = proceso['tiempo'] - j
                        proceso = self.calcular_tiempos(proceso)
                        self.tiempoTotal += 1
                        break
                    if self.numeroEjecucion == 0 or i != 0:
                        self.tiempoTotal += 1
                    i += 1
                    j -= 1
                if not self.interrupcion and not self.error:
                    operacion = proceso['operacion'].split()
                    resultado = 0
                    if operacion[1] == "+":
                        resultado = int(operacion[0]) + int(operacion[2])
                    elif operacion[1] == "-":
                        resultado = int(operacion[0]) - int(operacion[2])
                    elif operacion[1] == "*":
                        resultado = int(operacion[0]) * int(operacion[2])
                    elif operacion[1] == "/":
                        resultado = int(operacion[0]) / int(operacion[2])
                    else:
                        resultado = int(operacion[0]) % int(operacion[2])
                    proceso['resultado'] = resultado
                    proceso['tiempo_servicio'] = proceso['tiempo']
                    proceso = self.calcular_tiempos(proceso)
                    proceso['tiempo_finalizacion'] -= 1
                    proceso['tiempo_retorno'] -= 1
                    proceso['tiempo_espera'] -= 1
                    proceso['restante'] = 0
                if not self.interrupcion:
                    self.listaTerminados.append(proceso)
                    self.llenarTablaTerminados()
                    self.ui.Id_label.setText("")
                    self.ui.operacion_label.setText("")
                    self.ui.tiempo_label.setText("")
                    self.ui.transcurrido_lcdNumber.display(0)
                    self.ui.restante_lcdNumber.display(0)
                self.numeroEjecucion += 1
            else:
                self.bloqueados()
                QApplication.processEvents()
                time.sleep(1)
                self.tiempoTotal += 1
                self.ui.total_lcdNumber.display(self.tiempoTotal)
        self.boolEjecucion = False

    @Slot()
    def empezar(self):
        procesos = self.ui.N_Procesos.value()
        if procesos > 0:
            self.ui.Empezar_pushButton.setEnabled(False)
            self.numeroProcesos = procesos
            self.agregar()

    def crear_proceso(self):
        random = randint(1, 5)
        if random == 1:
            signo = "+"
        elif random == 2:
            signo = "-"
        elif random == 3:
            signo = "*"
        elif random == 4:
            signo = "/"
        else:
            signo = "%"
        n2 = randint(1, 100)
        n1 = randint(0, 100)
        operacion = str(n1) + ' ' + signo + ' ' + str(n2)
        tiempo = randint(6, 16)
        restante = tiempo
        Id = self.procesoActual
        self.procesoActual += 1
        proceso = {
            "Id": Id,
            "operacion": operacion,
            "tiempo": tiempo,
            "restante": restante,
            "bloqueado": None,
            "resultado": None,
            "tiempo_llegada": None,
            "tiempo_finalizacion": None,
            "tiempo_retorno": None,
            "tiempo_respuesta": None,
            "tiempo_espera": None,
            "tiempo_servicio": None,
            "tiempo_ejecucion": None,
            "bandera_ejecucion": False
        }
        if not self.boolEjecucion:
            self.listaRegistro.append(proceso)
            self.llenarTablaRegistro()
        else:
            if (len(self.listaEjecuccion) + len(self.listabloqueados) < 4) or (len(self.listaEjecuccion) + len(self.listabloqueados) < 5 and self.ui.Id_label.text() == ""):
                proceso['tiempo_llegada'] = self.tiempoTotal
                self.listaEjecuccion.append(proceso)
                self.llenarTablaEjecucion()               
            else:
                self.listaRegistro.append(proceso)
                self.llenarTablaRegistro()

    def agregar(self):
        for i in range(self.numeroProcesos):
            self.crear_proceso()
        self.ui.iniciar_pushButton.setEnabled(True)
    
    @Slot()
    def iniciar(self):
        self.ui.iniciar_pushButton.setEnabled(False)
        self.ui.N_Procesos.setEnabled(False)
        self.transicion()
        self.ejecucion()