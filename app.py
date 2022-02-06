from flask import Flask, render_template, request

from traitement.stat_on_data import count_homme_femme, count_groupe_politique, count_region
from traitement.recherche_wiki import recherche_wikipedia
from pyspark.ml.classification import  DecisionTreeClassificationModel
from pyspark.ml.linalg import Vectors
from pyspark.sql import SparkSession
import random



def get_predicion(row):
    spark = SparkSession.builder \
        .master("local") \
        .appName("Data Exploration") \
        .getOrCreate()
    test0 = spark.createDataFrame([(Vectors.dense(row[0], row[1], row[2]),)], ["features"])
    DTmodel = DecisionTreeClassificationModel.load(
        "/home/massino/Bureau/projetAssembleNationale/new/Projet_assemble_nationale_ABD/traitement/models/DT")
    print("model load")
    print(DTmodel.toDebugString)

    return DTmodel.predict(test0.head().features)
def rand_color(T):
  for i in range(0, T):
    color = []
    random_number = random.randint(0, 16777215)
    hex_number = str(hex(random_number))
    hex_number = '#' + hex_number[2:]
    color.append(hex_number)
  return color


app = Flask(__name__)


@app.route('/', methods=["GET", "POST"])
def index():
    if request.method == 'POST':
        if request.form['motcle'] !="":
            resultat, image = recherche_wikipedia(request.form['motcle'] )
            return render_template('resultat_Recherche.html', acteur=resultat.title,wiki=resultat.summary,img=image)
    return render_template('main.html')






@app.route('/contact')
def contact():
    return render_template('contact.html')




@app.route('/ia')
def IA():
    return render_template('IA.html')


@app.route('/stat')
def stat():
    groupepolitique=[]
    membre=[]
    region=[]
    count=[]

    hommes,femmes=count_homme_femme()
    df=count_groupe_politique()
    for i in range(0,len(df.collect())):
        if df.collect()[i][0] == None:
            groupepolitique.append("inconnu")
        else:
            groupepolitique.append(df.collect()[i][0])
        membre.append(df.collect()[i][1])

    df=count_region()
    for i in range(0,len(df.collect())):
        region.append(df.collect()[i][0])
        count.append(df.collect()[i][1])


    return render_template('stat.html',homme=hommes,femme=femmes,values=membre,labels=groupepolitique,region=region,count=count)
