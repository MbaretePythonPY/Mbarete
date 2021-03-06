#!/bin/bash
suma(){
    local resultado=$(($1+$2))
    echo $resultado
}

sigue(){
    read -p "Hacer '$1'.Enter para SI, [n o N] para NO?:" mi_var
    if [ -z $mi_var ];then
        echo true
    elif [ $mi_var == "N" ];then
        echo false
    elif [ $mi_var == "n" ];then
        echo false
    else
        echo true
    fi
}

super_comand(){   
    if [ "$principal" == " " ];then
        echo ERROR: debes darle valor a la variable 'principal'
    else
        if [ ${#my_array[@]} != 0 ];then
            echo Los ${#my_array[@]} parametros para "'$principal'" son:
            for i in ${!my_array[@]};do
                echo "  -$i ES IGUAL A ${my_array[$i]}"
            done
            if [ $confirmar == true ];then
                if [ $(sigue "MANTENER los Parametros") == false ];then
                    for i in ${!my_array[@]};do
                        read -p "Ingrese el Nuevo Valor para '-$i':" mi_cambio
                        my_array[$i]=$mi_cambio
                    done
                fi
            fi    
        fi
        argumento=''
        for i in ${!my_array[@]};do
            argumento="$argumento -$i ${my_array[$i]}"
        done
        principal="$principal $argumento"
        
        if [ $confirmar == false ];then
            ejecutar=true
        elif [ $(sigue "'$principal'. Obs:$obs") == true ];then
            ejecutar=true
        else
            ejecutar=false
        fi
        #echo $cross_modo_seguro
        if [ $cross_modo_seguro == true ];then
            ejecutar=false
            echo MODO SEGURO: "'$principal', Obs:$obs"
        fi

        if [ $ejecutar == true ];then
            echo "'$principal'. Obs:$obs"
            #truco para poder ejecutar cualquier linea
            echo "#!$SHELL" > $t
            echo "$principal" >> $t
            chmod +x $t
            source $t
            rm $t
        fi
    fi
    confirmar=true
    my_array=()
    principal=''
}
#Operator    Description
#    ! EXPRESSION    The EXPRESSION is false.
#    -n STRING   The length of STRING is greater than zero.
#    -z STRING   The lengh of STRING is zero (ie it is empty).
#    STRING1 = STRING2   STRING1 is equal to STRING2
#    STRING1 != STRING2  STRING1 is not equal to STRING2
#    INTEGER1 -eq INTEGER2   INTEGER1 is numerically equal to INTEGER2
#    INTEGER1 -gt INTEGER2   INTEGER1 is numerically greater than INTEGER2
#    INTEGER1 -lt INTEGER2   INTEGER1 is numerically less than INTEGER2
#    -d FILE     FILE exists and is a directory.
#    -e FILE     FILE exists.
#    -r FILE     FILE exists and the read permission is granted.
#    -s FILE     FILE exists and it's size is greater than zero (ie. it is not empty).
#    -w FILE     FILE exists and the write permission is granted.
#    -x FILE     FILE exists and the execute permission is granted.
#Operador Booleano
#    and - &&
#    or - ||

#Control de flujos if
#    if [ <some test> ]
#    then
#        <commands>
#    elif [ <some test> ]
#    then
#        <different commands>
#    else
#        <other commands>
#    fi
