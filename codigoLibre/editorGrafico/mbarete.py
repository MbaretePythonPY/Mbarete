#!/usr/bin/env python
# -*- coding: latin-1 -*-
# archivo generado por Dise�o Libre para Dise�adorDeEtiquetas

#Modulos importados
import os, math, sqlite3
from PIL import Image, ImageTk

info={
    'autor':'Lucas Mathias Villalba Diaz',
    'name':'Dise�adorGrafico',
    'text':'Dise�ador de Imagenes y Etiquetas',
    'descripcionBreve':'Dise�ador de IMAGENES',
    'descripcionLarga':'Dise�ador graficos para imagenes y etiquetas, generados a partir de un archivo externo CSV',
    'img':'logo.png',
    'enlace':'mathiaslucasvidipy@gmail.com',
    'etiquetas':['default', 'inicio', 'graficos', 'PNG', 'GENERADOR', 'IMAGENES']
}
widgets={
    'Dise�adorDeEtiquetasPanel':{
        'inputType':'panel',#OBLIGATORIO
        'etiquetas':['id','Inicio','default','panel','Dise�adorDeEtiquetas'],
        'name':'Dise�adorGrafico',#OBLIGATORIO
        'text':'Inicio Dise�ador Grafico',#OBLIGATORIO
        'anchor':'o',
        'inputs':{
            'inicio':{
                'inputType':'Button',
                'command':'manager',
                'text':'Administrador'
            }
        }
    },
    'Dise�adorDeEtiquetasFrame':{
        'inputType':'Frame',#OBLIGATORIO
        'etiquetas':['id','Inicio','Frame','Dise�adorDeEtiquetas'],
        'name':'Dise�adorDeEtiquetasFrame',#OBLIGATORIO
        'text':'Frame Dise�ador de Etiquetas',#OBLIGATORIO
        'inputs':{
            'inicio':{
                'inputType':'Button',
                'command':'manager',
                'text':'Administrador'
            }
        }
    }
}

def command(admin,G,info,ec,geo):
    print(info['subProyecto'])
    print('Info:',info['info'])
    print('Widgest:',info['widget'])
    print('Comandos',info['command']) 
    G.command[info['command']['manager']]=lambda : admin.transicion(G,admin.manager)
