#aesthetic changes > display nice string instead of list

#what kind of metrics could allow to stop automatically texts or group of texts that diverge more or less strongly from the norm corpus (in this case omnes)

#conditionnal formating

#plotting

#store each name value in a dict with relative count in text, hand and omnes
#the higher the difference between 
#better to have only one df 


import plotly.figure_factory as ff


import streamlit as st
import pandas as pd
import ast
#import seaborn as sns

st.title('PAPY NGRAM VIEWER')

#load omnes

#we want it in session state
#st.header('OMNES')
uploaded_zip = st.file_uploader("load omnes")
if (uploaded_zip is not None):
    zf = zipfile.ZipFile(uploaded_zip)

print(type(zf))
st.stop()

df = pd.read_csv('~/Desktop/out/omnes.csv')
#with st.expander('show'):
#    st.write(df)

#present texts by hand
hands = {
    'Abraamios':[18423,19717,21421,36165],
    'Andreas':[18403],
    'Dioscorus':[19026,19696,19703,19732],
    'Hermauos':[21049,19709,19710,37327,21422],
    'Isak':[18453,18976,18453,19341],
    'Kyros1':[18427,17962,17963,18179],
    'Kyros3':[19039,19040,21424],
    'Menas':[18662,18797,16251,36280],
    'Pilatos':[19023,18875,19021,18876,18430,19678],
    'Victor':[17959,37346,19029,18432,19342,19343]
}


def find_percent(an_int,another_int):
    return an_int/another_int

#to show values bit prettier way
def showValueNotList(a_list):
    #a_list = ast.literal_eval(a_list)
    #st.write(type(a_list))
    #return type(a_list)
    try:
        a_list = ast.literal_eval(a_list)
        return ''.join(a_list)
        #st.write(type(a_list))
        #return 0
    except:
        return 0


def color_negative_red(val):
    """
    Takes a scalar and returns a string with
    the css property `'color: red'` for negative
    strings, black otherwise.
    """
    color = 'red' if val < 0.2 else 'black'
    return 'color: %s' % color
#prob with 765518,38264

chosen_ngram = st.slider('choose ngram size',1,15,2)
percent = st.checkbox('display values in %',False)


#st.stop()
df = df[[f'{chosen_ngram}gramName',f'{chosen_ngram}gramNumber']]
df[f'{chosen_ngram}gramName'] = df[f'{chosen_ngram}gramName'].apply(showValueNotList)

#st.write(df.index.tolist())
#st.line_chart(df[f'{chosen_ngram}gramNumber'],y=df.index.tolist())



for el in hands.keys():
    st.header(f'TEXTS WRITTEN BY {el}')
    dfh = pd.read_csv(f'out/{el}.csv')
    dfh = dfh[[f'{chosen_ngram}gramName',f'{chosen_ngram}gramNumber']]
    dfh[f'{chosen_ngram}gramName'] = dfh[f'{chosen_ngram}gramName'].apply(showValueNotList)
    for n in hands[el]:
        st.subheader(f'{n}')
        df2 = pd.read_csv(f'out/{n}.csv')
        df3 = df2[[f'{chosen_ngram}gramName',f'{chosen_ngram}gramNumber']]
        df3[f'{chosen_ngram}gramName'] = df3[f'{chosen_ngram}gramName'].apply(showValueNotList)
        col1,col2,col3 = st.columns(3)
        
        if not percent:
            with st.expander('show individual tables'):
                with col1:
                    st.write('text level') 
                    st.write(df3)
                with col2:
                    st.write('author level')
                    st.write(dfh)
                with col3:
                    st.write('omnes')
                    st.write(df)
            
            #here we merge the dfs
            
            #for memory reasons we only keep first 1k tokens
            
            df3 = df3.head(100)
            
            df3 = df3.merge(dfh, left_on=f'{chosen_ngram}gramName', right_on=f'{chosen_ngram}gramName')
            del dfh
            
            #st.write(df3.shape)
            df3 = df3.merge(df, left_on=f'{chosen_ngram}gramName', right_on=f'{chosen_ngram}gramName')
            st.write(df3)
        else:
            ngram_inText = sum(df3[f'{chosen_ngram}gramNumber'].tolist())
            ngram_inHand = sum(dfh[f'{chosen_ngram}gramNumber'].tolist())
            ngram_inOmnes = sum(df[f'{chosen_ngram}gramNumber'].tolist())

            #st.write(ngram_inOmnes)
            #3st.write(ngram_inHand)
            #st.write(ngram_inText)

            with col1:
                st.write('text')
                df3[f'{chosen_ngram}gramNumber'] = df3[f'{chosen_ngram}gramNumber'].apply(lambda x: find_percent(x,ngram_inText))
                st.write(df3)
            with col2:
                st.write('author')
                dfh[f'{chosen_ngram}gramNumber'] = dfh[f'{chosen_ngram}gramNumber'].apply(lambda x: find_percent(x,ngram_inHand))
                st.write(dfh)
            with col3:
                st.write('omnes')
                df[f'{chosen_ngram}gramNumber'] = df[f'{chosen_ngram}gramNumber'].apply(lambda x: find_percent(x,ngram_inOmnes))
                st.write(df)
                
            df3 = df3.head(100)
            
            df3 = df3.merge(dfh, left_on=f'{chosen_ngram}gramName', right_on=f'{chosen_ngram}gramName')
            del dfh
            
            #st.write(df3.shape)
            df3 = df3.merge(df, left_on=f'{chosen_ngram}gramName', right_on=f'{chosen_ngram}gramName')
            #df3[f'{chosen_ngram}gramNumber'] = df3[f'{chosen_ngram}gramNumber'].to_frame().style.applymap(color_negative_red)
            
            
            
            #here we create two more series
            # reprendre ici avant expose
            #df3['suprisingTextAuthorRatio'] = 
            #df3['suprisingTextOmnesRatio'] = 
            #df3[''] = 
            
            
            st.write(df3)
                
            #data = [df3[f'{chosen_ngram}gramNumber'],dfh[f'{chosen_ngram}gramNumber'],df[f'{chosen_ngram}gramNumber']]
            #group_labels = ['1','2','3']
            #fig = ff.create_distplot(
            #data, group_labels)
            #st.plotly_chart(fig)            
            #st.plot(df[f'{chosen_ngram}gramNumber'])



#do it for one text then for all
#df2 = pd.read_csv('out/18423.csv')
#dfh = pd.read_csv('out/Abraamios.csv')

#st.write(df2)

#old that must be included into for loops
#st.write(chosen_ngram)










