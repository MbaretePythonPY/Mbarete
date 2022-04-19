#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import csv
import time
import datetime
import math
#from mbarete.mbarete import geometria as g
"""
 Ver versión de Linux con /etc/os-release
    El archivo /etc/os-release contiene datos de identificación del sistema operativo activo. 
    El formato de este archivo básico os-release es una lista separada por líneas nuevas de 
    asignaciones de variables compatibles a un entorno y alli podemos obtener la configuración 
    de los scripts de Shell. 
    El archivo os-release contiene datos definidos por el proveedor del sistema operativo y 
    como tal no deben ser modificados por el administrador ya que pueden afectar otros 
    servicios adicionales de la propia distribución.
    /*-*-*-*+
"""
from practicas.pruebas import object_prueba
class consola(object_prueba):
    """docstring for programador_consola"""
    def __init__(self, name='',fuente=['mbarete','consolas'],code='latin-1',info={},force=0):
        super(consola, self).__init__()
        self.name=name
        self.fuente=fuente
        self.code=code
        self.crearInfo(info=info,force=force)
        self.o=self.start()
        self.s = self.o['start']

    def start(self,name='',fuente=[]):
        if not name: name=self.name
        if not fuente: fuente=self.fuente
        import os
        if 'WINDIR' in os.environ:
            o={'OS':'windows','V':os.environ['OS']}
            o['name']=name+'.auto.cmd'
            o['cross']=r'%cross% '
            o['f']=''
            for d in fuente: o['f']+=d+'\\'
            o['start']=[
                '@ECHO off',
                'setlocal',
                'set "fuente='+o['f']+'"',
                r'set "cross=call %fuente%cmd_principal.cmd command"',
                r'call %fuente%cmd_principal.cmd inicio %fuente%'
                ]
            o['end']=['endlocal']
            o['to_var']=lambda v: r'%'+v+r'%'
            o['if_eq']=lambda a,b: 'IF "%'+str(a)+'%" == "'+str(b)+'" ('
            o['fi']=')'
            o['read']=lambda a: 'SET /p '+str(a)+'=Ingrese una Opcion:'
        elif 'SHELL' in os.environ:
            if os.environ['SHELL'].strip()=='/bin/bash':
                o={'OS':'linux','V':self.info['os_release_ID']}
                o['name']=name+'.auto.sh'
                o['cross']=r'cross '
                o['f']='./'
                for d in fuente: o['f']+=d+'/'
                o['start']=[
                    '#!/bin/bash',
                    'fuente='+o['f'],
                    'source "$fuente"bash_principal.sh'
                ]
                o['end']=['']
                o['to_var']=lambda v: r'$'+v
                o['if_eq']=lambda a,b: 'if [ "$'+str(a)+'" == "'+str(b)+'" ];then'
                o['fi']='fi'
                o['read']=lambda a: 'read -p "Ingrese una Opcion:" '+str(a)
            else:
                o={'OS':os.environ['SHELL'],'V':os.environ['SHELL']}
        elif 'ANDROID_ROOT' in os.environ:
            o={'OS':'android','V':os.environ['SHELL']}
        o['info']={v.split(':')[0]:v[len(v.split(':')[0])+1:] for v in self.getFile(o['f']+'info')}
        o['loop_num']=1
        o['for_num']=1
        o['while_num']=1
        return o
    def estructura_secuencial(self,c):
        if str == c.__class__: c=[c]
        #(script,commands,OS)
        for i in range(len(c)):
            for v in self.o['info']: c[i]=c[i].replace('$'+v[len(self.o['info']['prefijo']):],self.o['to_var'](v))
            c[i]=self.o['cross']+'"'+c[i].strip().replace(';;','; ;').replace(';;','; ;').replace('"',"'")+' "'
        self.s+=c
    def estructura_loop(self,menu):
        l='loop_'+str(self.o['loop_num'])
        vl='var_'+l
        self.o['loop_num']+=1
        if self.o['OS'] == 'windows':
            self.s+=[':'+l]
        if self.o['OS'] == 'linux':
            self.s+=[l+'=true']
            self.s+=['while [ $'+l+' == true ] ;do']

        if 'inicio' in menu: self.set(menu['inicio'])
        self.s+=['echo '+menu['cabezera']]
        for op in range(1,1+len(menu['lista'])): self.s+=['echo '+str(op)+'.'+menu['lista'][op-1]['opcion']]
        self.s+=['echo "  <<< ENTER PARA SALIR >>>"']
        self.s+=[self.o['read'](vl)]
        if self.o['OS'] == 'windows': self.s+=['if "%'+vl+'%"=="" (goto :eof)']
        if self.o['OS'] == 'linux': self.s+=['if [ -z $'+vl+' ];then '+l+'=false ;fi']
        for op in range(1,1+len(menu['lista'])):
            self.s+=[self.o['if_eq'](vl,op)]
            self.set(menu['lista'][op-1]['commands'])
            self.s+=[self.o['fi']]
        if self.o['OS'] == 'windows': self.s+=['goto :'+l]
        if self.o['OS'] == 'linux': self.s+=['done']
    def set(self,c):
        if dict == c.__class__:
            if ('inicio' in c) and ('cabezera' in c) and ('lista' in c):
                self.estructura_loop(c)
        else:
            self.estructura_secuencial(c)
    def save(self):
        self.setFile(self.o['name'],self.s+self.o['end'],echo=0)
    def crearInfo(self,info={},force=0):
        import os,sys,platform
        for cross in self.info: info[cross]=info[cross] if cross in info else self.info[cross]
        info['git_branch']=next((e[2:] for e in self.return_system("git branch")if '*' in e[0]),None)
        if info['git_branch']:
            git=self.return_system("git config --list",join={},sep='=')
            (info['git_repo_username'],info['git_repo_name'])=git['remote.origin.url'].split('/')[-2:]
            info['git_origin']= git['branch.master.remote'] if 'branch.master.remote' in git else 'origin'
            info['git_email']= git['user.email'] if 'user.email' in git else input('Ingrese su email de github:')
            info['git_username']= git['user.name'] if 'user.name' in git else input('Ingrese su username de github:')
            #info['git_']= git[''] if '' in git else ''
            
        info_default={
            'file':'info',
            'prefijo':'cross_',
            'git_repo_path':'',
            'sub_proyectos':'diseñoLibre',
            'pwd_practicas':'mbarete/practicas/home/',
            'pwd_consolas':'mbarete/consolas/',
            'temporal':self.info['tmp']+'temp_mbarete',
            'git_user.email':'mathiaslucasvidipy@gmail.com',
            'version':1.0,
            'modo_seguro':'false',
            'os_name':os.name 
        }
        for cross in info_default: info[cross]=info[cross] if cross in info else info_default[cross]
        info={k:(info['git_repo_path']+info[k]).replace('/',os.sep) if 'pwd_' in k[:4] else info[k] for k in info }
        info=self.getFile(info['pwd_consolas']+'info.'+info['OS'],join=info)
        print(info['OS']+'.'+info['V'])
        if os.name == 'nt':
            if info['OS']+'.'+info['V'] in os.listdir(info['pwd_consolas']):
                print(info['uname_sysname']+'.'+info['uname_release'])
        if os.name == 'posix':
            if info['OS']+'.'+info['V'] in os.listdir(info['pwd_consolas']):
                print(info['os_release_ID']+'.'+info['os_release_VERSION_CODENAME'])
        pwd=[info[k]+info['file'] for k in info if 'pwd_' in k[:4]]
        tmp=info['temporal']+'.'+info['file']
        info=[ (info['prefijo'] if k!='prefijo' else '')+k+':'+str(info[k]) for k in info ]
        self.setFile(tmp,valor=info,echo=0)
        for file in pwd: 
            if (not os.path.exists(file)) or force:
                self.setFile(file,valor=info,echo=0)
        for e in info:print(e)

def buscarVariableDeEntorno(search=[],info={}):
    import os
    dir(os)
    variables_de_entorno={env:os.environ[env] for env in os.environ}
    print("Search:",True if search else False)
    for variable in variables_de_entorno:
        if search:
            v=next((variable for s in search if s.lower() in variable.lower()),None)
            if v:
                print("%s: %s" % (v, variables_de_entorno[v]))
        else:
            print("%s: %s" % (variable, variables_de_entorno[variable]))

def programador_init():
    auto=consola(name='subir_push',fuente=['mbarete','consolas'],info={'git_repo_path':os.getcwd()+os.sep},force=1)

def git_push():
    #"comando principla;confirmarComando;banderas;archivoDeSalida;observacion"
    auto=consola(name='subir_push',fuente=['mbarete','consolas'])
    print(auto.o['info'])
    commands=[
        'git status;false;;',
        'git add -A;;;',
        'git commit;;m="commit automatico desde LinuxLite bash";output',
        "git push origin $branch;true;;",
        "git status;false;;"
    ]
    auto.set(commands)
    auto.save()
def git_pull():
    auto=consola(name='bajar_pull',fuente=['mbarete','consolas'])
    #print(auto.o)
    auto.set("git pull; ; ; ;trae datos del repositorio remoto y luego mezcla los cambios con el repositorio local")
    menu={
        'inicio':'git status;false;;;',
        'cabezera':'Si obtuvo algun error, por favor ingrese un numero de las siguientes opciones',
        'lista':[{
            'opcion':'No importan los cambios locales y desea sobrescribirlos',
            'commands':[
                "git fetch;false;;;solo traerá datos del repositorio remoto del 'branch' actual",
                "git reset --hard HEAD;false;;;restablecerá el branch a su último estado committed",
                r"git merge '@{u}';false;;;para mezclar los cambios con el repositorio local"
                ]
            },{
            'opcion':'Te importan los cambios y te gustaría mantenerlos después de traer los cambios remotos',
            'commands':[
                "git fetch;false;;;solo traerá datos del repositorio remoto del 'branch' actual",
                "git stash;false;;;significa guardar los cambios 'uncommitted' por un momento para traerlos nuevamente más tarde",
                r"git merge '@{u}'; ;;;para mezclar los cambios con el repositorio local",
                "git stash pop;false;;;para recuperar los cambios guardados en el último stash, este comando también elimina el 'stash commit' hecho con 'git stash'"
                ]
            },{
            'opcion':'Deseas descargar los cambios remotos pero aún no aplicarlos',
            'commands':[
                "git fetch --all;false;;;para obtener los cambios de todos los branches.",
                "git fetch --prune;true;;;limpiar algunas de las ramas que ya no existen en el repositorio remoto."
                ]
            }
        ]
    }
    auto.set(menu)
    auto.save()
def git_branch():
    """
    10 Comandos de Git Que Todo Desarrollador Debería Saber
        Nora Gonzalo Ciordia
        Nota: Para entender este artículo, tienes que conocer lo básico acerca de Git.
    1. git clone <https://link-con-nombre-del-repositorio>
        Git clone es un comando para descargarte el código fuente existente desde un repositorio remoto (como Github, por ejemplo). 
        git clone <https://link-con-nombre-del-repositorio>

    2. git branch <nombre-de-la-rama>
        Las ramas (branch) son altamente importantes en el mundo de Git. Podemos usar el comando git branch para crearlas, listarlas y eliminarlas.
        Creando una nueva rama:
            git branch <nombre-de-la-rama>

        Para enviar (push) la nueva rama al repositorio remoto, necesitarás usar el siguiente comando:
            git push <nombre-remoto> <nombre-rama>

        Visualización de ramas:
            git branch --list

        Borrar una rama:
            git branch -d <nombre-de-la-rama>

    3. git checkout <nombre-de-la-rama>
        Para trabajar en una rama, primero tienes que cambiarte a ella. También lo podemos usar para chequear archivos y commits.
        Hay algunos pasos que debes seguir para cambiarte exitosamente entre ramas:
            Los cambios en tu rama actual tienen que ser confirmados o almacenados en el guardado rápido (stash) antes de que cambies de rama.
            La rama a la que te quieras cambiar debe existir en local. 

        Hay también un comando de acceso directo que te permite crear y cambiarte a esa rama al mismo tiempo,(-b viene de rama (branch)):
            git checkout -b <nombre-de-tu-rama>

    4. git status
        Podemos encontrar información como:
            Si la rama actual está actualizada
            Si hay algo para confirmar, enviar o recibir (pull).
            Si hay archivos en preparación (staged), sin preparación(unstaged) o que no están recibiendo seguimiento (untracked)
            Si hay archivos creados, modificados o eliminados 

    5. git add -A
        Necesitamos usar el comando git add para incluir los cambios del o de los archivos en tu siguiente commit.
        Añadir un único archivo:
            git add <archivo>
        Añadir todo de una vez:
            git add -A
        Importante: El comando git add no cambia el repositorio y los cambios que no han sido guardados hasta que no utilicemos el comando de confirmación git commit.

    6. git commit -m "mensaje de confirmación"
        Una vez que se llega a cierto punto en el desarrollo, queremos guardar nuestros cambios (quizás después de una tarea o asunto específico). 
        Git commit es como establecer un punto de control en el proceso de desarrollo al cual puedes volver más tarde si es necesario.
            git commit -m "mensaje de confirmación"
        Importante: Git commit guarda tus cambios únicamente en local.

    7. git push <nombre-remoto> <nombre-de-tu-rama>
        Git push envía tus commits al repositorio remoto.
            git push <nombre-remoto> <nombre-de-tu-rama>

        De todas formas, si tu rama ha sido creada recientemente, puede que tengas que cargar y subir tu rama con el siguiente comando:
            git push --set-upstream <nombre-remoto> <nombre-de-tu-rama>
            or
            git push -u origin <nombre-de-tu-rama>
        Importante: Git push solamente carga los cambios que han sido confirmados.

    8. git pull <nombre-remoto>
        El comando git pull se utiliza para recibir actualizaciones del repositorio remoto. 
            git pull <nombre-remoto>
        Esta operación puede generar conflictos que tengamos que resolver manualmente.

    9. Git revert
        A veces, necesitaremos deshacer los cambios que hemos hecho. 
        Hay varias maneras para deshacer nuestros cambios en local y/o en remoto (dependiendo de lo que necesitemos), 
        pero necesitaremos utilizar cuidadosamente estos comandos para evitar borrados no deseados.

        Una manera segura para deshacer nuestras commits es utilizar git revert. 
        Para ver nuestro historial de commits, primero necesitamos utilizar el  git log --oneline:
        Entonces, solo necesitamos especificar el código de comprobación que encontrarás junto al commit que queremos deshacer:
            git revert 3321844

        Después de esto, verás una pantalla como la de abajo -tan solo presiona shift + q para salir
        El comando git revert deshará el commit que le hemos indicado, pero creará un nuevo commit deshaciendo la anterior
        La ventaja de utilizar git revert es que no afecta al commit histórico. 
        Esto significa que puedes seguir viendo todos los commits en tu histórico, incluso los revertidos.

        Otra medida de seguridad es que todo sucede en local a no ser que los enviemos al repositorio remoto. 
        Por esto es que git revert es más seguro de usar y es la manera preferida para deshacer los commits.

    10. Git merge
        Cuando ya hayas completado el desarrollo de tu proyecto en tu rama y todo funcione correctamente, 
        el último paso es fusionar la rama con su rama padre (dev o master). 
        Esto se hace con el comando git merge.

        Git merge básicamente integra las características de tu rama con todos los commits realizados a las ramas dev (o master).  
        Es importante que recuerdes que tienes que estar en esa rama específica que quieres fusionar  con tu rama de características.

        Por ejemplo, cuando quieres fusionar tu rama de características en la rama dev:
        Primero, debes cambiarte a la rama dev:
            git checkout dev
        Antes de fusionar, debes actualizar tu rama dev local:
            git fetch
        Por último, puedes fusionar tu rama de características en la rama dev:
            git merge <nombre-de-la-rama>

        Pista: Asegúrate de que tu rama dev tiene la última versión antes de fusionar otras ramas, si no, te enfrentarás a conflictos u otros problemas no deseados.

    """

def buscador():
    import os,shutil
    #for root, dirs, files in os.walk('../'): print(root,dirs,files)
    muestra=['123.jpg','132_456.jpg','4566_444_.jpg','1_1235_.jpg','123456_456123_465.jpg','789789_789789_789789.jpg']
    search=['132.jpg','465.jpg','456.jpg','789.jpg']
    #find for root, dirs, files in os.walk('../'):
    for f in muestra:
        i=f.replace(".jpg","").split("_")
        i=next((f for e in search if e.replace(".jpg","") in i),None)
        print(i)


if 'main' in __name__:
    from practicas.pruebas import main_pruebas
    pruebas={
        1:{'titulo':"Lista o buscar informacion del sistema",'f':lambda: crearInfo(search=[])},
        2:{'titulo':"programando en shell secuencial para GIT_PUSH",'f':git_push},
        3:{'titulo':"programando en shell un bucle loop para GIT_PULL",'f':git_pull},
        4:{'titulo':"mostrar valores de start('nombre_de_archivo'):",'f':lambda: print(consola.start(name='nombre_de_archivo'))},
        5:{'titulo':"buscar",'f':buscador},
        6:{'titulo':"crearInfo con class consola",'f':programador_init}
        }
    main_pruebas(pruebas,sys.argv)