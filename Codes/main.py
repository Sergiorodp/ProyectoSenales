import pandas as pd
from sodapy import Socrata
import matplotlib
import matplotlib.pyplot as plt

# Consultar a la API de datos.gov.co para recolectar los datos actualizados de covid en todo colombia

# Unauthenticated client only works with public data sets. Note 'None'
# in place of application token, and no username or password:
client = Socrata("www.datos.gov.co", None)

# Example authenticated client (needed for non-public datasets):
# client = Socrata(www.datos.gov.co,
#                  MyAppToken,
#                  userame="user@example.com",
#                  password="AFakePassword")

# First 2000 results, returned as JSON from API / converted to Python list of
# dictionaries by sodapy.
results = client.get("gt2j-8ykr", offset = 800000 , limit = 835339)

# Convertir a pandas DataFrame
results_df = pd.DataFrame.from_records(results)
# print(results_df)

#Extraer variables de genero
sex = results_df['sexo'].sum(numeric_only = False)

# Organizar y graficar los datos de contagio pro genero en los ultimos 2 meses
def Genero():
    M = 0
    F = 0
    for i in sex:
        if(i == 'M'):
            M +=1
        elif(i == 'F'):
            F +=1
    gen = pd.DataFrame({'Genero': ['M','F'],'Contagios':[M,F]})
    gen.plot.bar(x='Genero',y='Contagios')
    gen.plot.barh(x='Genero',y='Contagios')
    gen = pd.DataFrame({'Contagios':[M,F]},index = ['M','F'])
    gen.plot.pie(y = 'Contagios',figsize=(5, 5))

# Organizar los datos por contagio
def myFunc(e):
  return e['Contagios']


# Sacar Los datos de contagios de las 20 ciudades más contagiadas
def Ciudad():
    global results

    ciudades = []
    contagios = []
    valores = []

    for i in range(len(results)):
        if(results[i]['ciudad_de_ubicaci_n'] not in ciudades):
            ciudades.append(results[i]['ciudad_de_ubicaci_n'])
            contagios.append({'Ciudad' : results[i]['ciudad_de_ubicaci_n'] , 'Contagios' : 1})
        for j in range(len(ciudades)):
            if(results[i]['ciudad_de_ubicaci_n'] == contagios[j]['Ciudad']):
                contagios[j]['Contagios'] += 1

    contagios.sort(key=myFunc, reverse=True)
    ciudades = []
    for i in range(20):
        ciudades.append(contagios[i]['Ciudad'])
        valores.append(contagios[i]['Contagios'])
    # print(contagios)
    city = pd.DataFrame({'Ciudad': ciudades,'Contagios':valores})
    city.plot.bar(x = 'Ciudad', y = 'Contagios')
    city.plot.barh(x = 'Ciudad', y = 'Contagios')
    city = pd.DataFrame({'Contagios':valores},index = ciudades)
    city.plot.pie(y = 'Contagios',figsize=(5, 5))
    

# Organizar los datos de contagios por cada mes

def Mes():
    # fecha_diagnostico
    # results = client.get("gt2j-8ykr", offset = 800000 , limit = 829679)
    mes2020 = ['enero','febrero','marzo','abril','mayo','junio','julio','agosto','septiembre','octubre','noviembre']
    contagios = [0,0,0,0,0,0,0,0,0,0,0]
    lim = 80000
    off = 0

    for k in range(10):
        try:
            if(lim < 800000):
                results = client.get("gt2j-8ykr", offset = off , limit = lim)
            else:
                lim = 829679
                results = client.get("gt2j-8ykr", offset = off , limit = lim)

            for i in range(len(results)):
                try:
                    fecha = results[i]['fecha_de_notificaci_n'][5:7]
                    contagios[int(fecha) - 1] += 1
                    # print(fecha)
                except: 
                    print('no tiene fecha de diagnostico')
            off += 80000
            lim += 80000
        except:
            pass
    meses = pd.DataFrame({'Mes': mes2020,'Contagios':contagios})
    meses.plot.bar(x = 'Mes', y = 'Contagios')

Genero()
Ciudad()
Mes()
plt.show()




