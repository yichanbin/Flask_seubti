from flask import Flask,session, render_template, redirect,request,url_for
import random
import threading
import string
from func import INIT,getdf,RecommandList,decimal_to_binary
import threading

questions, keyword, style, num,Result_List, Dataframe_List=INIT()
app = Flask(__name__)
app.secret_key = ''.join(random.choice(string.ascii_letters + string.digits + string.punctuation) for _ in range(10))

@app.route('/')
def home():
    return render_template('home.html')
    
@app.route('/page1', methods=['GET', 'POST'])
def page1():
    total=[0.0,0.0,0.0,0.0]
    if request.method  == 'POST':
        for i in range(5):
            session['total']=request.form.get(str(i),type=float)
            total[keyword[i]]+=session['total']
        session.pop('total', None)
        return redirect(url_for("page2",total=total))
    
    else:
        return render_template('page1.html',questions=questions)

@app.route('/page2', methods=['GET', 'POST'])
def page2():
    session['total']= request.args.get('total')
    total=session['total']
    if request.method  == 'POST':
        for i in range(5,10):
            session['n']=request.form.get(str(i),type=float)
            total[keyword[i]]+=session['n']
        session.pop('total', None)
        session.pop('n', None)
        return redirect(url_for("page3",total=total))
    
    else:
        return render_template('page2.html',questions=questions)

@app.route('/page3', methods=['GET', 'POST'])
def page3():
    session['total']= request.args.get('total')
    total=session['total']
    if request.method  == 'POST':
        for i in range(10,15):
            session['n']=request.form.get(str(i),type=float)
            total[keyword[i]]+=session['n']
        session.pop('total', None)
        session.pop('n', None)
        return redirect(url_for("page4",total=total))
    
    else:
        return render_template('page3.html',questions=questions)

@app.route('/page4', methods=['GET', 'POST'])
def page4():
    session['total']= request.args.get('total')
    total=session['total']
    if request.method  == 'POST':
        for i in range(15,20):
            session['n']=request.form.get(str(i),type=float)
            total[keyword[i]]+=session['n']
        for i in range(4):
            style[i]=round(total[i]/(float(num[i]))) 
        session.pop('total', None)
        session.pop('n', None)
        return redirect(url_for("waiting"))
    else:
        return render_template('page4.html',questions=questions)

@app.route('/waiting')
def waiting():
    thread = threading.Thread(target=set_df)
    thread.start()
    return render_template('waiting.html')

@app.route('/result', methods=['GET', 'POST'])
def result():
    global Result_type 
    global style
    global All_Recommand_List
    All_Recommand_List =set_list()
    print(style)
    print(len(All_Recommand_List))
    Random_Recommand_List=random.sample(All_Recommand_List, 10)
    Result_type = next((item for item in Result_List if item['style'] == style), None)
    if request.method == 'POST':
        if request.form['button'] == "AdditionalList":
            return redirect(url_for("AdditionalList"))
        elif request.form['button'] == "Allhachi":
            return redirect(url_for("Allhachi"))
    else:
        return render_template('result.html',imagename="img/"+Result_type['name']+".png",name=Result_type['name'],explain1=Result_type["explain1"],explain2=Result_type["explain2"],explain3=Result_type["explain3"],List=Random_Recommand_List, base_url = "https://www.google.com/search?q=")

@app.route('/AdditionalList',methods=['GET', 'POST'])
def AdditionalList():
     if request.method == 'POST':
         return redirect(url_for("result"))
     else:
        return render_template('AdditionalList.html',name=Result_type['name'],count=len(All_Recommand_List),List=All_Recommand_List,base_url="https://www.google.com/search?q=")

@app.route('/Allhachi', methods=['GET', 'POST'])
def Allhachi():
    global style
    if request.method == 'POST':
        card_value= int(request.form.get('card_value'))
        session['card_value'] =card_value
        style=decimal_to_binary(session['card_value'])
        session.pop('card_value', None)
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
    print(len(Dataframe_List))
    return ''

def set_list():
    global Dataframe_List
    global style
    list=[]
    for i in range(12):
        list+=RecommandList(Dataframe_List[i],style)
    return list

if __name__ == '__main__':
    app.run()
