"""
    Tabla de significado de las constantes en PreApp

    Autores: Leonel Guerrero, Ka Fung
    Fecha: 22/11/2022
"""

EQUIV       = 'c_{1}'   # == 
RIGHTARROW  = 'c_{2}'   # =>
LEFTARROW   = 'c_{3}'   # <=
OR          = 'c_{4}'   # v
AND         = 'c_{5}'   # ^
NOTEQUIV    = 'c_{6}'   # !==
NOT         = 'c_{7}'   # ~
TRUE        = 'c_{8}'   # T
FALSE       = 'c_{9}'   # F

SUPSUB      = 'c_{10}'  # NO SE QUE ES ESTOOOOOOOOOOOOOO

FORALL1     = 'c_{11}'  # Para todo sin 
FORALL2     = 'c_{12}'  # Para todo con 
EXIST1      = 'c_{13}'  # Existe sin
EXIST2      = 'c_{14}'  # Existe con
EQUAL       = 'c_{15}'  # =
IN          = 'c_{16}'  # Pertenece a
NOTIN       = 'c_{17}'  # No pertenece a
EMPTYSET    = 'c_{18}'  # Conjunto vacio

SET1        = 'c_{19}'  # Conjunto con elementos (NO SE COMO LLAMAR ESTO
SET2        = 'c_{20}'  # Conjunto con un elemento

COMMA       = 'c_{21}'  # ,
BIGCUP      = 'c_{22}'  # Union
BIGCAP      = 'c_{23}'  # Interseccion
CUP         = 'c_{24}'  # Union
CAP         = 'c_{25}'  # Interseccion
SUBSET      = 'c_{26}'  # Subconjunto (sin igual)
SUBSETEQ    = 'c_{27}'  # Subconjunto (con igual)
SUPSET      = 'c_{28}'  # Superconjunto (sin igual)
SUPSETEQ    = 'c_{29}'  # Superconjunto (con igual)
SETMINUS    = 'c_{30}'  # Diferencia

TUPLE       = 'c_{31}'  # Tupla 
CROSSPROD   = 'c_{32}'  # Producto cruz

PAREN       = 'c_{33}'  # Parentesis
CIRC        = 'c_{34}'  # Composicion
POWERSET    = 'c_{35}'  # Conjunto de partes
INTSET      = 'c_{36}'  # Conjunto de enteros
BOOLSET     = 'c_{37}'  # Conjunto de booleanos
SUPERSCRIPT = 'c_{38}'  # Superindice
IDENTITY    = 'c_{39}'  # Función identi
ABORT       = 'c_{40}'  # Abort

SUPERE      = 'c_{41}'  # Elevado a la epsilon (NO SE COMO LLAMAR ESTO)

ZERO        = 'c_{42}'  # Cero
ONE         = 'c_{43}'  # Uno
TWO         = 'c_{44}'  # Dos
THREE       = 'c_{45}'  # Tres
FOUR        = 'c_{46}'  # Cuatro
FIVE        = 'c_{47}'  # Cinco
SIX         = 'c_{48}'  # Seis
SEVEN       = 'c_{49}'  # Siete
EIGHT       = 'c_{50}'  # Ocho
NINE        = 'c_{51}'  # Nueve

SSET        = 'c_{52}'  # S(a1)
PSET        = 'c_{53}'  # P(a1)

CONCAT      = 'c_{54}'  # Concatenacion
PLUS        = 'c_{55}'  # Suma
MINUS       = 'c_{56}'  # Resta
TIMES       = 'c_{57}'  # Multiplicacion

MODIFARRAY  = 'c_{58}'  # Modificacion de arreglo
RANGEARRAY  = 'c_{59}'  # Rango de arreglo

UNARYMINUS  = 'c_{60}'  # Negacion unaria
DOM         = 'c_{61}'  # Dominio
NOTEQUAL    = 'c_{62}'  # !=
LESS        = 'c_{63}'  # <
LEQ         = 'c_{64}'  # <=
GREATER     = 'c_{65}'  # >
GEQ         = 'c_{66}'  # >=

PI          = 'c_{67}'  # Pi

# ---------------------------------------------------------------------------
# Alias para tipos de datos
INT = 'int'
BOOL = 'bool'
STR = 'str'
ARRAY = 'array'
ANY = 'any'     # ANY es que puede ser entero o booleano

INTDICT = {
    0: ZERO,
    1: ONE,
    2: TWO,
    3: THREE,
    4: FOUR,
    5: FIVE,
    6: SIX,
    7: SEVEN,
    8: EIGHT,
    9: NINE
}

BOOLDICT = {
    'true': TRUE,
    'false': FALSE
}

TYPEDICT = {
    INT: INTSET,
    BOOL: BOOLSET,
}