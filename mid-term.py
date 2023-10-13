import pandas as pd
import prince
import altair as alt
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

st.title('Understanding Starbucks Customers')


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


st.header('Survey dataframe', divider='rainbow')
st.dataframe(data) 


st.header('Socio-demographics variables', divider='rainbow')
st.subheader('Frequency distribution')

def plot_bar(feature,figsize):
    plot_data = organize_plot_data(feature)
    generate_plot(plot_data,feature,figsize)

def organize_plot_data(feature):
    plot_data = data[['Timestamp',feature]] #Timestamp is used only for counting the occurrences
    plot_data = plot_data.groupby(feature).count()
    plot_data = plot_data.reset_index()
    plot_data.columns = [feature,'Counts'] 
    return plot_data

def generate_plot(plot_data,feature,figsize):
    #fig = plt.figure() # create the canvas for plotting
    fig = plt.figure(figsize=figsize)
    ax = plt.subplot(1,1,1) 
    ax.bar(x = plot_data[feature], height = plot_data['Counts'])
    ax.set_title('Costumers by {}'.format(feature))
    st.pyplot(fig)

feature = st.selectbox(
    'Select a variable',
    ('Gender', 'Age', 'Profession', 'Income', 'Visit Frequency', 'Spend per Visit', 'Membership'),
    index=1
    )

plot_bar(feature, figsize=(10,6))


st.header('Multi Correspondence Analysis', divider='rainbow')
###########
survey = pd.read_csv('./Starbucks satisfactory survey encode cleaned.csv')

selected_columns = st.multiselect(
    'Select variables to plot (VisitNo is always selected))',
    ['gender', 'age', 'status', 'income', 'method',
       'timeSpend', 'location', 'membershipCard', 'spendPurchase'],
    ['age'])

selected_columns = ['visitNo'] + selected_columns
# st.write('You selected:', options)

# selected_columns = ['gender', 'age', 'status', 'income']

mca_data = survey[selected_columns]
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
print(cc)
print(crc_df)

# plot and annotate
points = mca.plot(mca_data)

# filter rows whose name start with 'visit'
cc_visit = cc[cc['name'].str.startswith('visit')]
cc_other = cc[~cc['name'].str.startswith('visit')]

c_points = alt.Chart(cc_other).mark_point().encode(
    x='x',
    y='y',
    color=alt.value('blue')
)

print(points)
print(cc)




annot1 = alt.Chart(cc).mark_text(
    align='left',
    baseline='middle',
    fontSize = 15,
    dx = 7
).encode(
    x='x',
    y='y',
    text='name'
)

# annot_visit = alt.Chart(cc_visit).mark_text(
#     align='left',
#     baseline='middle',
#     fontSize = 10,
#     dx = 7
# ).encode(
#     x='x',
#     y='y',
#     text='name',
#     color='name'
# )

annot_visit = alt.Chart(cc_visit).mark_point().encode(
    x='x',
    y='y',
    color=alt.value('red')
    )

altair_chart = (c_points + annot1 + annot_visit).properties(
    width=700,
    height=700
).interactive()

st.altair_chart(altair_chart, use_container_width=False, theme="streamlit")

