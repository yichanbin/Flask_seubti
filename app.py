from flask import Flask,session, render_template, redirect,request,url_for
import random
import threading
import string
from func import INIT,getdf,RecommandList,decimal_to_binary,generate_secret_key
import threading

questions, keyword, num,Result_List, Dataframe_List=INIT()
trapic=0
app = Flask(__name__)
app.secret_key = generate_secret_key()

@app.route('/')
def home():
    global trapic
    trapic+=1
    print(trapic+"\n\n")
    return render_template('home.html')
    
@app.route('/page1', methods=['GET', 'POST'])
def page1():
    
    total=[0.0,0.0,0.0,0.0]
    if request.method  == 'POST':
        for i in range(5):
            session['n']=request.form.get(str(i),type=float)
            total[keyword[i]]+=float(session['n'])
        session.pop('n', None)
        session['total'] = ','.join(map(str, total))
        return redirect(url_for("page2"))
    
    else:
        print("page 1 Connection established successfully.\n")
        return render_template('page1.html',questions=questions)


@app.route('/page2', methods=['GET', 'POST'])
def page2():
    data_str = session.get('total')
    total = list(map(float, data_str.split(',')))
    if request.method  == 'POST':
        for i in range(5,10):
            session['n']=request.form.get(str(i),type=float)
            total[keyword[i]]+=float(session['n'])
        session.pop('total', None)
        session['total'] = ','.join(map(str, total))
        session.pop('n', None)
        return redirect(url_for("page3"))
    
    else:
        print("page 2 Connection established successfully.\n")
        return render_template('page2.html',questions=questions)

@app.route('/page3', methods=['GET', 'POST'])
def page3():
    data_str = session.get('total')
    total = list(map(float, data_str.split(',')))
    if request.method  == 'POST':
        for i in range(10,15):
            session['n']=request.form.get(str(i),type=float)
            total[keyword[i]]+=float(session['n'])
        session.pop('total', None)
        session['total'] = ','.join(map(str, total))
        session.pop('n', None)
        return redirect(url_for("page4"))
    
    else:
        print("page 3 Connection established successfully.\n")
        return render_template('page3.html',questions=questions)

@app.route('/page4', methods=['GET', 'POST'])
def page4():
    style=[0,0,0,0]
    data_str = session.get('total')
    total = list(map(float, data_str.split(',')))
    if request.method  == 'POST':
        for i in range(15,20):
            session['n']=request.form.get(str(i),type=float)
            total[keyword[i]]+=float(session['n'])
        for i in range(4):
            style[i]=round(total[i]/(float(num[i]))) 
        session.pop('total', None)
        session.pop('n', None)
        session['style'] = ','.join(map(str, style))
        return redirect(url_for("waiting"))
    else:
        print("page 4 Connection established successfully.\n")
        return render_template('page4.html',questions=questions)

@app.route('/waiting')
def waiting():
    thread = threading.Thread(target=set_df)
    thread.start()
    return render_template('waiting.html')

@app.route('/result', methods=['GET', 'POST'])
def result():
    global Result_type 
    data_str = session.get('style')
    style = list(map(int, data_str.split(',')))
    All_Recommand_List =set_list(style)
    Random_Recommand_List=random.sample(All_Recommand_List, 10)
    Result_type = next((item for item in Result_List if item['style'] == style), None)
    if request.method == 'POST':
        if request.form['button'] == "AdditionalList":
            return redirect(url_for("AdditionalList"))
        elif request.form['button'] == "Allhachi":
            return redirect(url_for("Allhachi"))
    else:
        print("result Connection established successfully.\n")
        return render_template('result.html',imagename="img/"+Result_type['name']+".png",name=Result_type['name'],explain1=Result_type["explain1"],explain2=Result_type["explain2"],explain3=Result_type["explain3"],List=Random_Recommand_List, base_url = "https://www.google.com/search?q=")

@app.route('/AdditionalList',methods=['GET', 'POST'])
def AdditionalList():
     data_str = session.get('style')
     style = list(map(int, data_str.split(',')))
     All_Recommand_List =set_list(style)
     if request.method == 'POST':
         return redirect(url_for("result"))
     else:
        print("AdditionalList Connection established successfully.\n")
        return render_template('AdditionalList.html',name=Result_type['name'],count=len(All_Recommand_List),List=All_Recommand_List,base_url="https://www.google.com/search?q=")

@app.route('/Allhachi', methods=['GET', 'POST'])
def Allhachi():
    if request.method == 'POST':
        card_value= int(request.form.get('card_value'))
        session['card_value'] =card_value
        style=decimal_to_binary(session['card_value'])
        session.pop('card_value', None)
        session['style'] = ','.join(map(str, style))
        return redirect(url_for("result"))
    else:
        print("Allhachi Connection established successfully.\n")
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
    print("Data Connection established successfully.")
    return ''

def set_list(style):
    global Dataframe_List
    list=[]
    for i in range(12):
        list+=RecommandList(Dataframe_List[i],style)
    return list

if __name__ == '__main__':
    app.run()
