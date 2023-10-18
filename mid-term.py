# Import libraries
import pandas as pd
import prince
import altair as alt
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

################################ 1. DATA PREPARATION ################################
data = pd.read_csv('./Starbucks satisfactory survey.csv')

rename_dict = {
    '1. Your Gender' : 'Gender',
    '2. Your Age' : 'Age',     
    '3. Are you currently....?' : 'Profession',
    '4. What is your annual income?' : 'Income',
    '5. How often do you visit Starbucks?' : 'Visit Frequency',
    '6. How do you usually enjoy Starbucks?' : 'Prefered Form of Consumption',
    '7. How much time do you normally  spend during your visit?' : 'Time Spent on Visit',
    "8. The nearest Starbucks's outlet to you is...?" : 'Distance to Store',
    '9. Do you have Starbucks membership card?' : 'Membership',
    '10. What do you most frequently purchase at Starbucks?' : 'Most consumed Product',
    '11. On average, how much would you spend at Starbucks per visit?' : 'Spend per Visit',
    '12. How would you rate the quality of Starbucks compared to other brands (Coffee Bean, Old Town White Coffee..) to be:' : 'Quality Rate',
    '13. How would you rate the price range at Starbucks?' : 'Price Range Rate',
    '14. How important are sales and promotions in your purchase decision?' : 'Sales and Promotion Importance',
    '15. How would you rate the ambiance at Starbucks? (lighting, music, etc...)' : 'Ambiance Rate',
    '16. You rate the WiFi quality at Starbucks as..' : 'WiFi Quality Rate',
    '17. How would you rate the service at Starbucks? (Promptness, friendliness, etc..)' : 'Service Rate',
    '18. How likely you will choose Starbucks for doing business meetings or hangout with friends?' : 'Likely for Meetings or Hangouts',
    '19. How do you come to hear of promotions at Starbucks? Check all that apply.' : 'Form of communication to Promotions',
    '20. Will you continue buying at Starbucks?' : 'Recurrent Costumer'
}

data = data.rename(rename_dict,axis=1)

data['Prefered Form of Consumption'] = data['Prefered Form of Consumption'].replace({'Never':'None','never':'None','Never buy':'None','Never ':'None','I dont like coffee':'None',np.nan:'None'})
data['Most consumed Product'] = data['Most consumed Product'].replace({'Never buy any':'Nothing','never':'Nothing','Never':'Nothing','Jaws chip ':'Jaws Chip','cake ':'Cake'})
data['Form of communication to Promotions'] = data['Form of communication to Promotions'].replace({np.nan:'Never hear'})

int_columns = ['Quality Rate','Price Range Rate','Ambiance Rate','WiFi Quality Rate','Service Rate','Likely for Meetings or Hangouts','Sales and Promotion Importance']
for column in int_columns:
    data[column] = data[column].astype(object)

data['Age'] = data['Age'].replace({'Below 20' : '1. Below 20',
                                    'From 20 to 29' : '2. From 20 to 29',
                                    'From 30 to 39' : '3. From 30 to 39',
                                    '40 and above' : '4. 40 and Above'})

data['Income'] = data['Income'].replace({'Less than RM25,000' : '1. Less than RM25,000',
                                        'RM25,000 - RM50,000' : '2. RM25,000 - RM50,000',
                                        'RM50,000 - RM100,000' : '3. RM50,000 - RM100,000',
                                        'RM100,000 - RM150,000' : '4. RM100,000 - RM150,000',
                                        'More than RM150,000' : '5. More than RM150,000'})

data['Spend per Visit'] = data['Spend per Visit'].replace({'Zero' : '1. Zero',
                                        'Less than RM20' : '2. Less than RM20',
                                        'Around RM20 - RM40' : '3. Around RM20 - RM40',
                                        'More than RM40' : '4. More than RM40'})

################################ STREAMLIT: TABS ################################
# Create a menu bar with tabs
selected_tab = st.sidebar.radio("Select a tab:", ["Analysis", "DataFrame"], index=0)

# Display content based on the selected tab
if selected_tab == "Analysis":
    # st.header("Analysis Tab")
    # Analysis content here
    st.title('Understanding Starbucks Customers :coffee:')
    
    ################################ STREAMLIT: 1. SOCIO-DEMO ################################
    st.header('Socio-demographics variables', divider='rainbow')
    st.subheader('Frequency distribution (n=122)')
    feature = st.selectbox(
        'Select a variable',
        ('Gender', 'Age', 'Profession', 'Income'),
        index=1
        )
          
    fig = plt.figure(figsize=(10,5))
    if (feature == 'Income'):
        plt.xticks(rotation=90)
    
    # This If below is just to avoid the hue color swicht around
    if (feature == 'Profession'):
        pass
    else:
        data = data.sort_values(by=feature)
        
    g = sns.histplot(data=data, 
                 x=feature, hue="Recurrent Costumer", multiple="stack", shrink=.8, 
                 palette={'Yes':'#6F8DE0','No':'#C0C0C0'})
    g.set_xlabel(feature, fontsize=14)
    g.set_ylabel("Count", fontsize=14)
    st.pyplot(fig)
   
    ################################ STREAMLIT: 2. MCA ################################
    st.header('Multi Correspondence Analysis', divider='rainbow')
    ###########
    
    # survey = pd.read_csv('./Starbucks satisfactory survey encode cleaned.csv')
    
    selected_columns = st.multiselect(
        'Select variables to plot (Recurrent Costumer is always selected))',
        ['Gender', 'Age', 'Profession', 'Income'],
        ['Age'])
    
    if (selected_columns == []):
        selected_columns = ['Age']
        st.write('Age is selected by default')
    
    selected_columns = ['Recurrent Costumer'] + selected_columns
    
    mca_data = data[selected_columns]
    mca = prince.MCA()
    mca.fit(mca_data)
    
    # extract the column coordinate dataframe, and change the column names
    cc = mca.column_coordinates(mca_data).reset_index()
    cc.columns = ['name', 'x', 'y']
    
    # extract the row coordinates dataframe, and change the column names
    rc = mca.row_coordinates(mca_data).reset_index()
    rc.columns = ['name', 'x', 'y']
    
    # combine the dataframes
    crc_df = pd.concat([cc, rc], ignore_index=True)
    #print(cc)
    #print(crc_df)
    
    # plot and annotate
    points = mca.plot(mca_data)
    
    # filter rows whose name start with 'recurrent'
    cc_recurrent = cc[cc['name'].str.startswith('Recurrent')]
    cc_other = cc[~cc['name'].str.startswith('Recurrent')]
    
    c_points = alt.Chart(cc_other).mark_point(filled=True).encode(
        x='x',
        y='y',
        color=alt.value('blue'),
        size=alt.value(150)
    )
    
    customizations = alt.Chart(cc_other, title="The shorter distance, the more similar they are").mark_circle().encode(
        alt.X('x').axis(labels=False).title('Dim 1'),
        alt.Y('y').axis(labels=False).title('Dim 2')
    )
       
    annot1 = alt.Chart(cc).mark_text(
        align='left',
        baseline='middle',
        fontSize = 17,
        dx = 10
    ).encode(
        x='x',
        y='y',
        text='name',
    )
    
    annot_visit = alt.Chart(cc_recurrent).mark_point(filled=True).encode(
        x='x',
        y='y',
        color=alt.value('red'),
        size=alt.value(150)
        )


    
    altair_chart = alt.layer(c_points + annot1 + annot_visit + customizations).configure_axis(
        grid=True, bandPosition=0.5, gridOpacity=0.05, gridColor='#000000')
    
    altair_chart = (c_points + annot1 + annot_visit + customizations).properties(
        width=700,
        height=700
    ).interactive().configure(background='#FFFFFF').configure_axis(labelColor='black')
    
    st.altair_chart(altair_chart, use_container_width=False, theme="streamlit")
    

st.altair_chart(altair_chart, use_container_width=False, theme="streamlit")


