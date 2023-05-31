from flask import Flask, render_template, redirect,request,url_for
import random
import threading
from func import INIT,getdf,RecommandList,decimal_to_binary
import threading

questions, keyword, total, style, num,Result_List, Dataframe_List=INIT()
application = Flask(__name__)


@application.route('/')
def home():
    return render_template('home.html')

@application.route('/page1', methods=['GET', 'POST'])
def page1():
    if request.method  == 'POST':
        for i in range(5):
            total[keyword[i]]+=request.form.get(str(i),type=float)
        return redirect(url_for("page2"))
    
    else:
        return render_template('page1.html',questions=questions)

@application.route('/page2', methods=['GET', 'POST'])
def page2():
    if request.method  == 'POST':
        for i in range(5,10):
            total[keyword[i]]+=request.form.get(str(i),type=float)
        return redirect(url_for("page3"))
    
    else:
        return render_template('page2.html',questions=questions)

@application.route('/page3', methods=['GET', 'POST'])
def page3():
    if request.method  == 'POST':
        for i in range(10,15):
            total[keyword[i]]+=request.form.get(str(i),type=float)
        return redirect(url_for("page4"))
    
    else:
        return render_template('page3.html',questions=questions)

@application.route('/page4', methods=['GET', 'POST'])
def page4():
    if request.method  == 'POST':
        for i in range(15,20):
            total[keyword[i]]+=request.form.get(str(i),type=float)

        for i in range(4):
            style[i]=round(total[i]/(float(num[i]))) 

        
        return redirect(url_for("waiting"))
    else:
        return render_template('page4.html',questions=questions)

@application.route('/waiting')
def waiting():
    thread = threading.Thread(target=set_df)
    thread.start()
    return render_template('waiting.html')

@application.route('/result', methods=['GET', 'POST'])
def result():
    global Result_type 
    global style
    global All_Recommand_List
    All_Recommand_List =set_list()
    Random_Recommand_List=random.sample(All_Recommand_List, 10)
    Result_type = next((item for item in Result_List if item['style'] == style), None)
    if request.method == 'POST':
        if request.form['button'] == "AdditionalList":
            return redirect(url_for("AdditionalList"))
        elif request.form['button'] == "Allhachi":
            return redirect(url_for("Allhachi"))
    else:
        return render_template('result.html',imagename="img/"+Result_type['name']+".png",name=Result_type['name'],explain1=Result_type["explain1"],explain2=Result_type["explain2"],explain3=Result_type["explain3"],List=Random_Recommand_List, base_url = "https://www.google.com/search?q=")

@application.route('/AdditionalList',methods=['GET', 'POST'])
def AdditionalList():
     if request.method == 'POST':
         return redirect(url_for("result"))
     else:
        return render_template('AdditionalList.html',name=Result_type['name'],count=len(All_Recommand_List),List=All_Recommand_List,base_url="https://www.google.com/search?q=")

@application.route('/Allhachi', methods=['GET', 'POST'])
def Allhachi():
    global style
    if request.method == 'POST':
        card_value = int(request.form.get('card_value'))
        style=decimal_to_binary(card_value)
        return redirect(url_for("result"))
    else:
        return render_template('Allhachi.html',list=Result_List)

def set_df():
    global Dataframe_List
    getDF=getdf()
    Dataframe_List.append(getDF.Museum())
    Dataframe_List.append(getDF.MountainPark())
    Dataframe_List.append(getDF.Zoo_Botanical_RecreationForest())
    Dataframe_List.append(getDF.TraditionalMarkets())
    Dataframe_List.append(getDF.CulturalHeritage())
    Dataframe_List.append(getDF.EcologicalCulturalStreet())
    Dataframe_List.append(getDF.SightseeingStreet())
    Dataframe_List.append(getDF.LibraryLecture())
    Dataframe_List.append(getDF.CulturalSpace())
    Dataframe_List.append(getDF.FutureHeritage())
    Dataframe_List.append(getDF.CulturalEvent())
    Dataframe_List.append(getDF.PublicEducationalServices())
    return ''

def set_list():
    global Dataframe_List
    global style
    list=[]
    for i in range(12):
        list+=RecommandList(Dataframe_List[i],style)
    return list

if __name__ == '__main__':
    application.run()