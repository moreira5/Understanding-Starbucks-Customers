# Import libraries
import pandas as pd
import prince
import altair as alt
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from wordcloud import WordCloud 

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


################################ STREAMLIT: SIBE-BAR ################################
st.sidebar.header("Understanding Starbucks Customers :coffee:")
st.sidebar.subheader("Sidebar Menu:")
selected_tab = st.sidebar.radio("Select a tab:", [":bookmark_tabs: Overview", ":bar_chart: Analysis"], index=0)

################################ STREAMLIT: 1. OVERVIEW ################################
if selected_tab == ":bookmark_tabs: Overview":
    st.markdown("# Overview :bookmark_tabs:")
    
    tab1_1, tab1_2, tab1_3 = st.tabs(["Goal", "Survey Questions", "Database"])
    
################################ STREAMLIT: 1.1. GOAL ################################
    with tab1_1:
       st.header("Survey's Goal:")
       st.write("""
        Analyze a Starbucks Customer to understand the characteristics 
        of recurrent and non-recurrent customers.   \n
        The big-picture question aimed to answer is:  \n 
        - What differentiates recurrent customers from non-recurrent 
        customers at Starbucks, and why does it matter?  \n 
        This can help Starbucks improve its customer experience, tailor its 
        offerings, and increase customer loyalty.
        """
        )

################################ STREAMLIT: 1.2. QUESTIONS ################################
    with tab1_2:
       st.header("Columns name in database : Survey Questions")
       st.markdown("1. **Gender** : Your Gender")
       st.markdown("2. **Age** : Your Age")     
       st.markdown("3. **Profession** : Are you currently....?")
       st.markdown("4. **Income** : What is your annual income?")
       st.markdown("5. **Visit Frequency** : How often do you visit Starbucks?")
       st.markdown("6. **Prefered Form of Consumption** : How do you usually enjoy Starbucks?")
       st.markdown("7. **Time Spent on Visit** : How much time do you normally  spend during your visit?")
       st.markdown("8. **Distance to Store** : The nearest Starbuckss outlet to you is...?")
       st.markdown("9. **Membership** : Do you have Starbucks membership card?")
       st.markdown("10. **Most consumed Product** : What do you most frequently purchase at Starbucks?")
       st.markdown("11. **Spend per Visit** : On average, how much would you spend at Starbucks per visit?")
       st.markdown("12. **Quality Rate** : How would you rate the quality of Starbucks compared to other brands (Coffee Bean, Old Town White Coffee..)?")
       st.markdown("13. **Price Range Rate** : How would you rate the price range at Starbucks?")
       st.markdown("14. **Sales and Promotion Importance** : How important are sales and promotions in your purchase decision?")
       st.markdown("15. **Ambiance Rate** : How would you rate the ambiance at Starbucks? (lighting, music, etc...)")
       st.markdown("16. **WiFi Quality Rate** : You rate the WiFi quality at Starbucks as..")
       st.markdown("17. **Service Rate** : How would you rate the service at Starbucks? (Promptness, friendliness, etc..)")
       st.markdown("18. **Likely for Meetings or Hangouts** : How likely you will choose Starbucks for doing business meetings or hangout with friends?")
       st.markdown("19. **Form of communication to Promotions** : How do you come to hear of promotions at Starbucks? Check all that apply.")
       st.markdown("20. **Recurrent Costumer** : Will you continue buying at Starbucks?")

################################ STREAMLIT: 1.3. DATABASE ################################
    with tab1_3:
        st.header('Database')
        st.write(data)


################################ STREAMLIT: 2. ANALYSIS ################################
else:
    st.markdown("# Analysis :bar_chart:")
    tab2_1, tab2_2, tab2_3,  tab2_4 = st.tabs(["Socio-demographics variables", "Multi Correspondence Analysis (MCA)", "Quality rates", "WordCloud"])

################################ STREAMLIT: 2.1. SOCIO-DEMO ################################
    with tab2_1:
        st.header('Socio-demographics variables')
        st.subheader('Frequency distribution (n=122)', divider='rainbow')
        feature = st.selectbox(
            'Select a variable',
            ('Gender', 'Age', 'Profession', 'Income'),
            index=1
            )

        fig = plt.figure(figsize=(10,5))
        if (feature == 'Income'):
            plt.xticks(rotation=90)

        # This IF below is just to avoid the hue color swicht around
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
        
        st.subheader('Some Takeaways', divider='rainbow')
        st.write('- The costumers are well balance between Male and Female')
        st.write('- The great portion of costumers are younger people, ranging between 20 and 29 years old, and generally are Employers and Students with incomes lower than RM 25.000')

################################ STREAMLIT: 2.2. MCA ################################
    with tab2_2:
        st.header('Multi Correspondence Analysis (MCA)')
        st.subheader("""
                     :orange[Notes:]  \n
                     - **Interpretation:** Points that are closer to each other in the MCA plot are more similar  \n
                     This is, by adding variables to the plot we can see which are the nearest blue points to each red point, 
                     this allow us to find recurrent and non-recurrent consutmers charecteristics\n
                     - Maximaze the plot is recomended :arrow_up_down:'
                     """, divider='rainbow')
    
        selected_columns = st.multiselect(
            'Select variables to plot (Recurrent Costumer is always selected))',
            ['Gender', 'Age', 'Profession', 'Income', 'Visit Frequency',
             'Prefered Form of Consumption', 'Time Spent on Visit','Spend per Visit', 'Distance to Store'],
            ['Age'])

        if (selected_columns == []):
            selected_columns = ['Recurrent Costumer']

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

        altair_chart = (c_points + annot1 + annot_visit + customizations).properties(
            width=700,
            height=700
        ).interactive().configure(background='#FFFFFF').configure_axis(labelColor='black', 
                                                                       grid=True, gridColor='#F8F9F9', titleColor='black', titleFontSize=18)

        st.altair_chart(altair_chart, use_container_width=False, theme="streamlit")

        st.subheader('Some Takeaways', divider='rainbow')
        st.write('- Monthly Visitors tends to consume by Drive-Thru, expending regular values on each visit')
        st.write('- Monthly Visitors tends to make short visits, up to one hour')

################################ STREAMLIT: 2.3. RATES ################################
    with tab2_3:
        st.header('Quality rates')
        st.subheader('Frequency distribution (n=122)', divider='rainbow')

        feature = st.selectbox(
            'Select a variable',
            ('Quality Rate', 'Price Range Rate', 'Ambiance Rate', 'WiFi Quality Rate', 'Service Rate', 'Likely for Meetings or Hangouts', 'Sales and Promotion Importance'),
            index=1
            )

        fig = plt.figure(figsize=(10,5))

        data=data.sort_values(by=feature)
        g = sns.histplot(data=data , 
                     x=data[feature].astype(str), hue="Recurrent Costumer", multiple="stack", shrink=.8, 
                     palette={'Yes':'#6F8DE0','No':'#C0C0C0'})
        g.set_xlabel(feature, fontsize=14)
        g.set_ylabel("Count", fontsize=14)
        st.pyplot(fig)

        st.subheader('Some takeaways', divider='rainbow')
        st.write('- The Rates related to Price Range are not so skewed to higher notes, indicating some insatisfaction of the costumers')
        st.write('- Consequently, the Importance of Sales and Promotions to Costumers presents higher rates')
        
################################ STREAMLIT: 4. WORDCLOUD ################################
    with tab2_4:    
        st.header('Wordcloud')
        st.subheader('Form of communication in Promotions', divider='rainbow')

        text = ' '.join(str(x) for x in data['Form of communication to Promotions'].tolist())

        plt.figure().clear() 
        wc=WordCloud(background_color="white").generate(text)
        plt.imshow(wc)
        plt.axis('off')
        st.pyplot(plt)