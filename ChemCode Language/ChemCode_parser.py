
import ply.yacc as yacc
import sys
from ChemCode_lexer import tokens
from chemlib import *




#Setting precedence to operations
precedence = (

    ('left', 'PLUS', 'MINUS'),
    ('left', 'MULTIPLY', 'DIVIDE')

)

def p_conv(p):
    '''
    conv : expression
         | var_assign
         | empty
    '''
    print(run(p[1]))

names ={}





def p_expression(p):
    '''
    expression : expression MULTIPLY expression
                    | expression DIVIDE expression
                    | expression PLUS expression
                    | expression MINUS expression
    '''




def p_expression_conv(p):
    '''
    expression : FLOAT
                | INT
    '''
    p[0]=p[1]

def p_expression_var(p):
    '''
    expression : TEXT
    '''
    p[0]=p[1]
    try:
        p[0] = names[p[1]]
    except LookupError:
        p[0] = p[1]


def p_var_assign(p):
    '''
    var_assign : TEXT EQUALS expression
    '''
    p[0]= ('=', p[1], p[3])
    names[p[1]] = p[3]


def p_expression_functions(p):
    '''
    expression : expression LANGLEBRA expression RANGLEBRA LPAR expression COMMA expression RPAR
               | expression LANGLEBRA expression RANGLEBRA LPAR expression COMMA expression COMMA expression COMMA expression RPAR
               | expression LANGLEBRA expression RANGLEBRA LPAR RPAR
               | expression LANGLEBRA expression COMMA expression RANGLEBRA LPAR expression RPAR
               | expression LANGLEBRA expression COMMA expression RANGLEBRA LPAR expression COMMA expression RPAR
    '''

    # TC - Temperature Converter
    if p[1] == 'TC':

        # Convert C and K to F
        if p[3] == 'F':
            if p[6] == 'C':
                p[0] = str((float(9/5) * p[8]) + 32 ) + ' °F'
                print("Formula used: °F = ((9/5) * °C) + 32")
            elif p[6] == 'K':
                p[0] = str(float(p[8]- 273.15) * float(9/5) + 32) + ' °F'
                print("Formula used: °F = ((K-273.15) * (9/5)) + 32")


        # Convert F and C to K
        if p[3] == 'K':
            if p[6] == 'F':
                p[0] = str(float(5/9)* float(p[8]-32) + 273.15) + ' K'
                print("Formula used: K = ((5/9) * (°F-32)) + 273.15")
            elif p[6] == 'C':
                p[0] = str(float(p[8]+273.15)) + ' K'
                print("Formula used: K = °C + 273.15")

        # Convert F and K to C
        if p[3] == 'C':
            if p[6] == 'F':
                p[0] = str(float(5/9) * float(p[8]-32)) + ' °C'
                print("Formula used: °C = (5/9) * (°F-32)")
            elif p[6] == 'K':
                p[0] = str(float(p[8]-273.15)) + ' °C'
                print("Formula used: °C = K - 273.15")

    # DMV - Density,Mass,Volume Operations
    elif p[1] == 'DMV':

        # Obtain Density when Mass(g) and Volume(mL) are known
        if p[3] == 'D':
            if ((p[6]== 'M') & (p[10] == 'V')):
                p[0] = str(float(p[8]) / float(p[12])) + ' g/mL'
                print("Formula used: Density = Mass(g) / Volume(mL)")
            elif ((p[6]== 'V') & (p[10]=='M')):
                p[0] = str(float(p[12]) / float(p[8])) + ' g/mL'
                print("Formula used: Density = Mass(g) / Volume(mL)")

        # Obtain Mass when Density(g/mL) and Volume(mL) are known
        if p[3] == 'M':
            if ((p[6] == 'D') & (p[10] == 'V')):
                p[0] = str(float(p[8]) * float(p[12])) + ' g'
                print("Formula used: Mass = Density(g/mL) * Volume(mL)")
            elif ((p[6] == 'V') & (p[10] == 'D')):
                p[0] = str(float(p[12]) * float(p[8])) + ' g'
                print("Formula used: Mass = Density(g/mL) * Volume(mL)")

        # Obtain Volume when Mass(g) and Density(g/mL) are known
        if p[3] == 'V':
            if ((p[6] == 'M') & (p[10] == 'D')):
                p[0] = str(float(p[8]) / float(p[12])) + ' mL'
                print("Formula used: Volume = Mass(g) / Density(g/mL)")
            elif ((p[6] == 'D') & (p[10] == 'M')):
                p[0] = str(float(p[12]) / float(p[8])) + ' mL'
                print("Formula used: Volume = Mass(g) / Density(g/mL)")


    # UC - Unit Converter
    elif p[1] == 'UC':

        # Convert Gallons, Quarts, Cubic meters, and Grams to Liters
        if p[3] == 'L':
            if p[6] == 'gal':
                p[0] = str(float(4 * p[8]) * float(1/1.057)) + ' L'
                print("Formula used: " + str(p[8]) + " gal * (4 qt / 1 gal) * (1 L / 1.057 qt)")
            elif p[6] == 'qt':
                p[0] = str(float(p[8]) * float(1/1.057)) + ' L'
                print("Formula used: " + str(p[8]) + " qt * (1 L / 1.057 qt)")
            elif p[6] == 'm3':
                p[0] = str(float(1000 * p[8])) + ' L'
                print("Formula used: " + str(p[8]) + " m^3 * (1 L / (10^-3) m^3)")
            elif p[6] == 'g':
                p[0] = str(float(p[8] / 1000)) + ' L'
                print("Formula used: " + str(p[8]) + " g * (1 mL / 1 g) * (1 L / 1000 mL )")


        # Convert Quarts, and Liters to Gallons
        if p[3] == 'gal':
            if p[6] == 'qt':
                p[0] = str(float(1/4) * float(p[8])) + ' gal'
                print("Formula used: " + str(p[8]) + " qt * (1 gal / 4 qt)")
            elif p[6] == 'L':
                p[0] = str( float( 1.057 * p[8]) * float(1/4)) + ' gal'
                print("Formula used: " + str(p[8]) + " L * (1.057 qt / 1 L) * (1 gal / 4 qt)")

        # Convert Gallons, and Liters to Quarts
        if p[3] == 'qt':
            if p[6] == 'gal':
                p[0] = str(float(4 * p[8])) + ' qt'
                print("Formula used: " + str(p[8]) + " gal * (4 qt / 1 gal)")
            elif p[6] == 'L':
                p[0] = str(float(1.057 * p[8])) + ' qt'
                print("Formula used: " + str(p[8]) + " L * (1.057 qt / 1 L)")

        # Convert Liters, Grams, Cubic centimeters,and Cubic inches to Cubic meters
        if p[3] == 'm3':
            if p[6] == 'L' :
                p[0]= str(float(p[8]/1000)) + ' m^3'
                print("Formula used: " + str(p[8]) + " L * ((10^-3) m^3 / 1 L)")
            elif p[6] == 'g':
                p[0] = str(float(p[8]/1000) / float(1000)) + ' m^3'
                print("Formula used: " + str(p[8]) + " g * (1 mL / 1 g) * (1 L / 1000 mL) * ((10^-3) m^3 / 1 L)")
            elif p[6] == 'cm3':
                p[0]= str(float(p[8]/1000000)) + ' m^3'
                print("Formula used: " + str(p[8]) + " cm^3 * (1 m / 100 cm)^3")
            elif p[6] == 'in3':
                p[0]= str(float(16.387064 * p[8]) * float(1/1000000)) + ' m^3'
                print("Formula used: " + str(p[8]) + " in^3 * (2.54 cm / 1 in )^3 * (1 m / 100 cm)^3")

        # Convert Liters, and Cubic meters to Grams
        if p[3] == 'g':
            if p[6] == 'L':
                p[0] = str(float(1000 * p[8])) + ' g'
                print("Formula used: " + str(p[8]) + " L * (1000 mL / 1 L ) * (1 g / 1 mL) ")
            elif p[6] == 'm3':
                p[0] = str(float(1000 * p[8]) * float(1000)) + ' g'
                print("Formula used: " + str(p[8]) + " m^3 * (1 L / (10^-3) m^3 ) * (1000 mL / 1 L) * (1 g / 1 mL)")

        # Convert Cubic meters, and Cubic inches to Cubic centimeters
        if p[3] == 'cm3':
            if p[6] == 'm3':
                p[0]= str(float(1000000 * p[8])) + ' cm^3'
                print("Formula used: " + str(p[8]) + " m^3 * (100 cm / 1 m)^3")
            elif p[6] == 'in3':
                p[0] = str(float(16.387064 * p[8])) + ' cm^3'
                print("Formula used: " + str(p[8]) + " in^3 * (2.54 cm / 1 in )^3")

        # Convert Cubic meters, and Cubic centimeters to Cubic inches
        if p[3] == 'in3':
            if p[6] == 'm3':
                p[0] = str(float(p[8] / 16.387064) * float(1000000)) + ' in^3'
                print("Formula used: " + str(p[8]) + " m^3 * (100 cm / 1 m)^3 * (1 in / 2.54 cm )^3")
            elif p[6] == 'cm3':
                p[0] = str(float(p[8] / 16.387064)) + ' in^3'
                print("Formula used: " + str(p[8]) + " cm^3 * (1 in / 2.54 cm )^3")


    #SE - Show Element
    elif p[1] == 'SE':

        if p[3] == 'H' or 'He' or 'Li' or 'Be' or 'B' or 'C' or 'N' or 'O' or 'F' or 'Ne' or 'Na' or 'Mg' or 'Al' \
                or 'Si' or 'P' or 'S' or 'Cl' or 'Ar' or 'K' or 'Ca' or 'Sc' or 'Ti' or 'V' or 'Cr' or 'Mn' or 'Fe'\
                or 'Co' or 'Ni' or 'Cu' or 'Zn' or 'Ga' or 'Ge' or 'As' or 'Se' or 'Br' or 'Kr' or 'Rb' or 'Sr' or 'Y'\
                or 'Zr' or 'Nb' or 'Mo' or 'Tc' or 'Ru' or 'Rh' or 'Pd' or 'Ag' or 'Cd' or 'In' or 'Sn' or 'Sb' or 'Te'\
                or 'I' or 'Xe' or 'Cs' or 'Ba' or 'La' or 'Ce' or 'Pr' or 'Nd' or 'Pm' or 'Sm' or 'Eu' or 'Gd' or 'Tb'\
                or 'Dy' or 'Ho' or 'Er' or 'Tm' or 'Yb' or 'Lu' or 'Hf' or 'Ta' or 'W' or 'Re' or 'Os' or 'Ir' or 'Pt'\
                or 'Au' or 'Hg' or 'Tl' or 'Pb' or 'Bi' or 'Po' or 'At' or 'Rn' or 'Fr' or 'Ra' or 'Ac' or 'Th' or 'Pa'\
                or 'U' or 'Np' or 'Pu' or 'Am' or 'Cm' or 'Bk' or 'Cf' or 'Es' or 'Fm' or 'Md' or 'No' or 'Lr' or 'Rf'\
                or 'Db' or 'Sg' or 'Bh' or 'Hs' or 'Mt' or 'Ds' or 'Rg' or 'Cn' or 'Nh' or 'Fl' or 'Mc' or 'Lv' or 'Ts'\
                or 'Og':
            print(p[3], "properties: ")
            p[0] = (Element(p[3]).properties)

    #BEQ1 - Balance Equation 1 (2 Reactants, 1 Product)
    elif p[1] == 'BEQ1':

        reactant1 = Compound(p[3])

        reactant2 = Compound(p[5])

        product1 = Compound(p[8])

        r = Reaction(reactants=[reactant1, reactant2], products=[product1])

        print("The unbalanced chemical equation provided is: ", r.formula)
        r.balance()
        print("The balanced chemical equation formula is: ")
        p[0] = r.formula

    #BEQ2 - Balance Equation 2 (2 Reactants, 2 Products)
    elif p[1] == 'BEQ2':

        reactant1 = Compound(p[3])

        reactant2 = Compound(p[5])

        product1 = Compound(p[8])

        product2 = Compound(p[10])

        r = Reaction(reactants=[reactant1, reactant2], products=[product1, product2])

        print("The unbalanced chemical equation provided is: ", r.formula)
        r.balance()
        print("The balanced chemical equation formula is: ")
        p[0] = r.formula

# discover help understand our chemistry programming language
def p_discover(p):
    '''
        expression : DISCOVER
    '''

    if p[1]== 'discover':
        p[0]= "\n        WELCOME TO CHEMCODE !!!"\
        "\n\n  Chemcode allows the following operations: "\
        "\n\n  1) Density,Mass,Volume measurements: "\
        "\n     For obtaining Volume(mL) use the following: " \
               "DMV<V>(M,Value of Mass(g),D,Value of Density(g/mL)) or DMV<V>(D,Value of Density(g/mL),M,Value of Mass(g))"\
        "\n     For obtaining Mass(g) use the following: " \
               "DMV<M>(V,Value of Volume(mL),D,Value of Density(g/mL)) or DMV<M>(D,Value of Density(g/mL),V,Value of Volume(mL))"\
        "\n     For obtaining Density(g/mL) use the following: " \
               "DMV<D>(V,Value of Volume(mL),M,Value of Mass(g)) or DMV<D>(M,Value of Mass(g),V,Value of Volume(mL))"\
        "\n\n 2) Temperature Converter: "\
        "\n     For obtaining Temperature in Farenheit use the following: "\
        "\n     From Celsius to Farenheit use: TC<F>(C,degree in Celsius)" \
        "\n     From Kelvin to Farenheit use: TC<F>(K,Unit Kelvin Value)" \
        "\n\n     For obtaining Temperature in Celsius use the following: "\
        "\n     From Farenheit to Celsius use: TC<C>(F,degree in Farenheit)"\
        "\n     From Kelvin to Celsius use: TC<C>(K,Unit Kelvin Value)"\
        "\n\n     For obtaining Temperature in Kelvin use the following: "\
        "\n     From Farenheit to Kelvin use: TC<K>(F,degree in Farenheit)"\
        "\n     From Celsius to Kelvin use: TC<K>(C,degree in Celsius)"\
        "\n\n 3) Unit Converter for most used units of measurement in chemistry: "\
        "\n     For obtaining Liters use the following: " \
        "\n     From Gallons to Liters use: UC<L>(gal,number of gallons )" \
        "\n     From quarts to Liters use: UC<L>(qt,number of quarts)" \
        "\n     From cubic meters to Liters use: UC<L>(m3,number of cubic meters)" \
        "\n     From grams to Liters use: UC<L>(g,number of grams)" \
        "\n\n     For obtaining gallons use the following: " \
        "\n     From quarts to gallons use: UC<gal>(qt,number of quarts )" \
        "\n     From Liters to gallons use: UC<gal>(L,number of Liters)" \
        "\n\n     For obtaining quarts use the following: " \
        "\n     From gallons to quarts use: UC<qt>(gal,number of gallons )" \
        "\n     From Liters to quarts use: UC<qt>(L,number of Liters)" \
        "\n\n     For obtaining cubic meters use the following: " \
        "\n     From Liters to cubic meters use: UC<m3>(L,number of Liters )" \
        "\n     From grams to cubic meters use: UC<m3>(g,number of grams)" \
        "\n     From cubic centimeters to cubic meters use: UC<m3>(cm3,number of cubic centimeters)" \
        "\n     From cubic inches to cubic meters use: UC<m3>(in3,number of cubic inches)" \
        "\n\n     For obtaining grams use the following: " \
        "\n     From Liters to grams use: UC<g>(L,number of Liters )" \
        "\n     From cubic meters to grams use: UC<g>(m3,number of cubic meters)" \
        "\n\n     For obtaining cubic centimeters use the following: " \
        "\n     From cubic meters to cubic centimeters use: UC<cm3>(m3,number of cubic meters )" \
        "\n     From cubic inches to cubic centimeters use: UC<cm3>(in3,number of cubic inches)" \
        "\n\n     For obtaining cubic inches use the following: " \
        "\n     From cubic meters to cubic inches use: UC<in3>(m3,number of cubic meters )" \
        "\n     From cubic centimeters to cubic inches use: UC<in3>(cm3,number of cubic centimeters)"\
        "\n\n 4) Show Chemical Elements from Periodic Table: "\
        "\n     Use the following Expression: SE<Symbol of the Element>() " \
        "\n     For example, if you want to know the properties of Hydrogen use this expression: SE<H>()" \
        "\n\n 5) Balance Chemical Equations: " \
        "\n      For Balancing Chemical Equations we have two cases: "\
        "\n     .For two reactants and one product use the following: BEQ1<reactant1,reactant2>(product1)" \
        "\n      Example: For the unbalanced equation 1O₂ + 1N₁O₁ --> 1N₁O₂, use this expression: BEQ1<O2,NO>(NO2)" \
        "\n     .For two reactants and two products use the following: BEQ2<reactant1,reactant2>(product1,product2)" \
        "\n      Example: For the unbalanced equation 1C₁H₄ + 1O₂ --> 1C₁O₂ + 1H₂O₁, use this expression: BEQ2<CH4,O2>(CO2,H2O)" \

def p_empty(p):
    '''
    empty :
    '''
    p[0] = None

def p_error(p):
    print("Syntax Error!")

parser = yacc.yacc()
env = {}

def run(p):
    global env
    if type(p) == tuple:
        if p[0]=='+':
            return run(p[1]) + run(p[2])
        elif p[0]=='-':
            return run(p[1]) - run(p[2])
        elif p[0]=='/':
            return run(p[1]) / run(p[2])
        elif p[0]=='*':
            return run(p[1]) * run(p[2])
        elif p[0]=='=':
            env[p[1]] = run(p[2])
            return env
        elif p[0]=='var':
            if p[1] not in env:
                return "Undefined variable found!"
            return env[p[1]]
    else:
        return p

while True:
    try:
        s = input('>> ')
    except EOFError:
        break
    parser.parse(s)




