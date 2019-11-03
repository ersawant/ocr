from flask import render_template, url_for, flash, redirect, request
from flaskblog import app, db, bcrypt
from flaskblog.forms import RegistrationForm, LoginForm
from flask_login import login_user, current_user, logout_user, login_required
from werkzeug.utils import secure_filename
from flaskblog.models import User, Problem_statement, Submissions, Allsubs
from datetime import datetime
from flask import send_file
import time
import camelot
import pandas as pd
import base64
import os
import pandas as pd
from rouge import Rouge
rouge = Rouge()




def datetime_from_utc_to_local(utc_datetime):
    now_timestamp = time.time()
    offset = datetime.fromtimestamp(now_timestamp) - datetime.utcfromtimestamp(now_timestamp)
    return utc_datetime + offset





@app.route("/", methods=['GET', 'POST'])

def home():
    
    #return render_template('use_case.html',tables=[df.to_html(classes='data')], titles=df.columns.values)
    return render_template('use_case.html')
@app.route("/get_test_file", methods=['GET', 'POST'])

def get_test_file():
    with open("C:/Users/Dell/Favorites/Flask/29th july 2019 to 4th septe 2019_2-2.pdf", "rb") as data_file:
        data = data_file.read()
    encoded_data = base64.b64encode(data).decode('utf-8')
    return render_template("test.html", encoded_data=encoded_data)


@app.route('/upload_file', methods=['POST','GET'])
def upload_file():
    if request.method == 'POST':
        if request.files:
            file = request.files["file"]

        if file :
            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'],
                      filename))
                      
            #flash('File successfully uploaded')
            
        else:
            flash('Allowed file types are txt, pdf, png, jpg, jpeg, gif'
                  )
            return redirect(request.url)
    df=myscript(file)
    df.to_csv("C:/Users/Dell/Favorites/Flask/flaskblog/file_exports/exportlineitem.csv", index = False)
    return render_template('use_case.html',tables=[df.to_html(classes='data',index=False)], titles=df.columns.values)

@app.route('/export_file', methods=['POST','GET'])
def export_file():
    df=pd.read_csv('C:/Users/Dell/Favorites/Flask/flaskblog/file_exports/exportlineitem.csv')
    #df=myscript(file)
    df.to_json(r'C:/Users/Dell/Favorites/Flask/flaskblog/file_exports/exportlineitem.json')
    flash('File successfully exported')
    return render_template('use_case.html',tables=[df.to_html(classes='data',index=False)], titles=df.columns.values)





def myscript(file):
    import pandas as pd
    
    print(file.filename)
    tables = camelot.read_pdf((os.path.join(app.config['UPLOAD_FOLDER'],file.filename)),flavor='stream', strip_text=' .\n')
    pdf_1=tables[0].df
    pdf_2 = pdf_1.iloc[4:]


    part_number_yn = []
    for i in range(pdf_2.shape[0]):
        if pdf_2.iloc[i, 0] != '':
            part_number_yn.append(i)
       

    part_number_df = pd.DataFrame(pdf_2.iloc[part_number_yn, 0])
    qty_shipped_df = pd.DataFrame(pdf_2.iloc[part_number_yn, 4])
    amount_df = pd.DataFrame(pdf_2.iloc[part_number_yn, 8])

    qty_shipped_df_num = []
    for i in range(qty_shipped_df.shape[0]):
        qty_shipped_df_num.append(int(qty_shipped_df.iloc[i,0])/1000)
    qty_shipped_df_num = pd.DataFrame(qty_shipped_df_num)

    amount_df_num = []
    for i in range(amount_df.shape[0]):
        amount_df_num.append(int(amount_df.iloc[i,0])/100)
    amount_df_num = pd.DataFrame(amount_df_num)

    part_number_df2 = []
    for i in range(part_number_df.shape[0]):
        part_number_df2.append(part_number_df.iloc[i,0])
    part_number_df2 = pd.DataFrame(part_number_df2)

    df_except_desc = pd.concat([part_number_df2, qty_shipped_df_num, amount_df_num], axis = 1)
    df_except_desc.columns = ['Item', 'QTY', 'Line Amount']

    
    desc_list = []
    for i in range(len(part_number_yn)):
        start_i = part_number_yn[i]
        if i == len(part_number_yn) - 1:
            end_i = pdf_2.shape[0]
        else:
            end_i = part_number_yn[i+1]
     
        desc = ''
        d = 0
        for j in range(end_i)[start_i:end_i]:
            d = d +1
            if d == 1:
                desc = desc + str(pdf_2.iloc[j,2])
            else:
                desc = desc + ' ' + str(pdf_2.iloc[j,2])
        desc_list.append(desc)
       

    desc_df = pd.DataFrame(desc_list)
    desc_df = desc_df.rename(columns = {0 : "Description"})
    final_df = pd.concat([df_except_desc, desc_df], axis = 1)

    #final_df.to_csv("C:/Users/Dell/Favorites/Flask/flaskblog/test.csv", index = False)
    #df = pd.read_csv('C:/Users/Dell/Favorites/Flask/flaskblog/test.csv', sep=',', engine='python')
    df = final_df
    df=df.fillna(" ")
    return df
    
def about():
    return render_template('about.html', title='About')






@app.route('/add_use_case',methods = ['POST', 'GET'])

def add_use_case():
   if request.method == 'POST':
       p_statement = request.form['statement']
       if(p_statement == ""):
       	flash('Empty value', 'danger')
       	return redirect(url_for('home'))
       res = Problem_statement.query.filter_by(statement=p_statement).first()
       if (res != None):
           flash('Problem statement already exists', 'danger')
           return redirect(url_for('home'))
       print(p_statement)
       ps = Problem_statement(statement= p_statement)
       db.session.add(ps)
       db.session.commit()
       flash('Problem Statement added successfully', 'success')
   return redirect(url_for('home'))




@app.route('/delete_use_case',methods = ['POST', 'GET'])

def delete_use_case():
   if request.method == 'POST':
       p_statement = request.form['statement']
       print(p_statement)
       Problem_statement.query.filter(Problem_statement.statement == p_statement).delete()
       db.session.commit()
       flash('Problem Statement deleted successfully', 'success')
   return redirect(url_for('home'))





# @app.route('/id=<key>')
# def show_post(key):
#     res = Problem_statement.query.filter_by(id=key).first()
#     if(res == None):
#         return redirect(url_for('home'))
#     return render_template('dashboard.html')





ALLOWED_EXTENSIONS = set(['csv', 'xlsx'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS





@app.route('/dashboard', methods = ['GET','POST'])

def dashboard():
    # if request.method=="POST":
    subs = Submissions.query.all()
    subs=sorted(subs, key = lambda x:x.score, reverse=True)

    return render_template('dashboard.html', title = 'Dashboard', subs=subs)
