import pandas as pd
from flask import Flask,request, render_template,url_for
from flask_cors import CORS

#loading csv into dataframe
df=pd.read_csv('recommendation.csv',low_memory=False)

app = Flask(__name__)
CORS(app) 

#home page
@app.route('/')
def index():
    return render_template("index.html") 

#product code introduction
@app.route('/introduction')
def introduction():
    product_list=df['Product'].values.tolist()
    return render_template("introduction.html",product_list=product_list) 

#similar products recommendation (web)
@app.route('/recommend',methods=['POST'])
def recommend():
    if request.method=="POST":
        input=request.form.get("comp_select")

    #recommnedation value 'FeatureMappedAmount' is loaded
    score=df[df['Product']==input]['FeatureMappedAmount'].values[0]
    #looking for 5 similar products (including product itself)
    df_similar_products=df.iloc[(df['FeatureMappedAmount']-score).abs().argsort()[:5]]
    # inital product is excluded
    similar_products_index_list=df_similar_products.index.tolist()[1:]
    
    product_code_initial_index=df_similar_products.index.tolist()[0]

    initial_value=df.loc[product_code_initial_index,'Product']+'\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0'+df.loc[product_code_initial_index,'description_supplier']
    #generation of similar products list
    values=[]
    
    for i in similar_products_index_list:
        #value=df.loc[i,'Product']
        value=df.loc[i,'Product']+'\xa0\xa0\xa0\xa0\xa0\xa0\xa0\xa0'+df.loc[i,'description_supplier']
        #result=value+'  '+description
        values.append(value)

    return render_template("recommend.html",values=values,initial_value=initial_value)

#similar products recommendation (curl)
@app.route('/recommendation',methods=['POST']) 
def recommendation(): 
    
    product_dict={}
    
    if request.method == 'POST':
        #json data is received
        data=request.get_json()
    #product is extracted from json_data    
    input=data['product']
    #recommnedation value 'FeatureMappedAmount' is loaded
    score=df[df['Product']==input]['FeatureMappedAmount'].values[0]
    #looking for 5 similar products (including product itself)
    df_similar_products=df.iloc[(df['FeatureMappedAmount']-score).abs().argsort()[:5]]
    # inital product is excluded
    similar_products_index_list=df_similar_products.index.tolist()[1:]
    
    #generation of similar products dictionnary
    keys=[]
    
    for i in range(1,5):
        keys.append('Product'+str(i))
    
    values=[]
    
    for i in similar_products_index_list:
        value=df.loc[i,'Product']
        values.append(value)
    
    for k in keys:
       
        product_dict[k]= values[keys.index(k)]  
               
    return product_dict

if __name__ == '__main__': 
  
    # run() method of Flask class runs the application  
    # on the local development server. 
    app.run() 

