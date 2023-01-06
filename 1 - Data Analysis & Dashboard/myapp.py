import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import openpyxl
import plotly.figure_factory as ff

st.title('Dashboard - Getaround')
st.header('The new feature analysis')
st.markdown("👋 Welcome, you'll find here the dashboard created to share my analysis on the Getaround Project")
st.markdown('')



STATE_COLUMN = 'state'
CAR_ID = 'car_id'
DELAY_CHECKOUT_COLUMN = 'delay_at_checkout_in_minutes'
TIME_DELTA_PREVIOUS_RENT = 'time_delta_with_previous_rental_in_minutes'
TIME_DELTA_GROUPS = 'time_delta_previous_rental_groups'
LATE_GROUPS = 'late_groups'
EARLY_GROUPS = 'early_groups'



DATA_URL_original = 'c:\\Users\\Christophe\\Desktop\\certification35288_bloc5-Deployment-Getaround\\1 - Data Analysis & Dashboard\\src\\get_around_delay_analysis.xlsx'
DATA_URL_analysis = 'c:\\Users\\Christophe\\Desktop\\certification35288_bloc5-Deployment-Getaround\\1 - Data Analysis & Dashboard\\src\\dashboard_data.csv'
DATA_URL_late = 'c:\\Users\\Christophe\\Desktop\\certification35288_bloc5-Deployment-Getaround\\1 - Data Analysis & Dashboard\\src\\dashboard_data_late.csv'
DATA_URL_early = 'c:\\Users\\Christophe\\Desktop\\certification35288_bloc5-Deployment-Getaround\\1 - Data Analysis & Dashboard\\src\\dashboard_data_early.csv'

@st.cache
def load_data(DATA_URL):
    data = pd.read_excel(DATA_URL)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    return data

def load_data_2(DATA_URL):
    data = pd.read_csv(DATA_URL)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    return data


# Create a text element and let the reader know the data is loading.
data_load_state = st.text('Loading data...')
# Load 10,000 rows of data into the dataframe.
data_original = load_data(DATA_URL_original)
data_analysis = load_data_2(DATA_URL_analysis)
data_late = load_data_2(DATA_URL_late)
data_early = load_data_2(DATA_URL_early)

data_connected_checkin = data_analysis[data_analysis['checkin_type']=='connect']

# Notify the reader that the data was successfully loaded.
data_load_state.text('Loading data...Done! (using st.cache, to win time computing)')
st.markdown('')

st.subheader('PART-1 - Original Data')

if st.checkbox('Show sample of raw data'):
    st.subheader('Raw data (25 first rows)')
    st.write(data_original)
    #st.write(data.iloc[:25,0:])

if st.checkbox('States value_counts'):
    st.subheader('States value_counts')
    fig1 = px.bar(data_frame=data_original,
        x= STATE_COLUMN,
        color=STATE_COLUMN
    )
    st.plotly_chart(fig1)


if st.checkbox('Heatmap'):
    st.subheader('Heatmap')
    # Correlation matrix
    corr_matrix = data_original.corr().round(2)
    fig2 = ff.create_annotated_heatmap(
        corr_matrix.values,
        x = corr_matrix.columns.tolist(),
        y = corr_matrix.index.tolist())

    st.plotly_chart(fig2)


if st.checkbox('Delay Column Histogram'):
    st.subheader('Delay Column Histogram')
    hist_values_time_delta = px.histogram(
        data_frame=data_original,
        x=TIME_DELTA_PREVIOUS_RENT, 
        color=STATE_COLUMN
        )
    st.plotly_chart(hist_values_time_delta)

if st.checkbox('Car_ID Histogram'):
    st.subheader('Is State linked to car ID?')
    hist_values_car = px.histogram(
        data_frame=data_original,
        x=CAR_ID, 
        color=STATE_COLUMN
        )
    st.plotly_chart(hist_values_car)

st.subheader('PART-2 - Data Analysis')

if st.checkbox('Time Delta GROUPS'):

    st.subheader('Count according to time delta with previous rental')
    option = st.selectbox(
    'How would you see this feature?',
    ('Barplot', 'Pie Chart'))

    if option == 'Barplot':

        fig3 = px.bar(data_frame=data_analysis,
            x= TIME_DELTA_GROUPS,
            color=TIME_DELTA_GROUPS,
            color_discrete_sequence=px.colors.qualitative.Pastel1,
        )
        st.plotly_chart(fig3)

    else:
        #st.subheader('Count according to time delta with previous rental')

        sizes = data_analysis[TIME_DELTA_GROUPS]
        explode = (0.1, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')

        fig4, (ax1,ax2) = plt.subplots(ncols=2)
        data_analysis.groupby(TIME_DELTA_GROUPS).size().plot(kind='pie', 
                                                            autopct='%1.1f%%', 
                                                            textprops={'fontsize': 5},
                                                            colors=['#125fb8', '#158ed8'], 
                                                            startangle=90,
                                                            ax=ax1)
    

        data_connected_checkin.groupby(TIME_DELTA_GROUPS).size().plot(kind='pie', 
                                                            autopct='%1.1f%%', 
                                                            textprops={'fontsize': 5},
                                                            colors=['#125fb8', '#158ed8'], 
                                                            startangle=90,
                                                            ax=ax2)
        #ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        ax1.set_xlabel('All checkin types')
        ax1.set_ylabel('')

        ax2.set_xlabel('Connected Checkin')
        ax2.set_ylabel('')

        st.pyplot(fig4)


if st.checkbox('Late GROUPS'):
    st.subheader("Count according 'late groups' column I've created")
    option = st.selectbox(
    'Please choose the filter on Checkin_type column',
    ('All rents', 'Connect checkin', 'Mobile checkin'))

    if option == 'All rents':
        fig5 = px.bar(data_frame=data_late,
                x= LATE_GROUPS,
                color=LATE_GROUPS,
                # hover_data=[
                #         'late <= 1 hour', 
                #         'late btw 1 and 2 hours', 
                #         'late btw 2 and 3 hours', 
                #         'late btw 3 and 4 hours', 
                #         'late btw 4 and 6 hours', 
                #         'late btw 6h and 1 day',
                #         'late btw 1 and 2 days',
                #         ],
                #color_discrete_map={'late <= 1 hour':'#125fb8'},
                color_discrete_sequence=px.colors.qualitative.Pastel1,
        )
        model = st.radio('Order', ('ascending', 'descending'))
        if model == 'ascending':
            fig5.update_layout(xaxis={'categoryorder':'total ascending'})
        else:
            fig5.update_layout(xaxis={'categoryorder':'total descending'})
            
        st.plotly_chart(fig5)


    elif option == 'Connect checkin':
        fig6 = px.bar(data_frame=data_late[data_late['checkin_type']=='connect'],
                x= LATE_GROUPS,
                color=LATE_GROUPS,
                # hover_data=[
                #         'late <= 1 hour', 
                #         'late btw 1 and 2 hours', 
                #         'late btw 2 and 3 hours', 
                #         'late btw 3 and 4 hours', 
                #         'late btw 4 and 6 hours', 
                #         'late btw 6h and 1 day',
                #         'late btw 1 and 2 days',
                #         ],
                #color_discrete_map={'late <= 1 hour':'#125fb8'},
                color_discrete_sequence=px.colors.qualitative.Pastel1,
        )
        model = st.radio('Order', ('ascending', 'descending'))
        if model == 'ascending':
            fig6.update_layout(xaxis={'categoryorder':'total ascending'})
        else:
            fig6.update_layout(xaxis={'categoryorder':'total descending'})
        st.plotly_chart(fig6)

    elif option == 'Mobile checkin':
        fig7 = px.bar(data_frame=data_late[data_late['checkin_type']=='mobile'],
                x= LATE_GROUPS,
                color=LATE_GROUPS,
                # hover_data=[
                #         'late <= 1 hour', 
                #         'late btw 1 and 2 hours', 
                #         'late btw 2 and 3 hours', 
                #         'late btw 3 and 4 hours', 
                #         'late btw 4 and 6 hours', 
                #         'late btw 6h and 1 day',
                #         'late btw 1 and 2 days',
                #         ],
                #color_discrete_map={'late <= 1 hour':'#125fb8'},
                color_discrete_sequence=px.colors.qualitative.Pastel1,
        )
        model = st.radio('Order', ('ascending', 'descending'))
        if model == 'ascending':
            fig7.update_layout(xaxis={'categoryorder':'total ascending'})
        else:
            fig7.update_layout(xaxis={'categoryorder':'total descending'})
        st.plotly_chart(fig7)


# if st.checkbox('Early GROUPS'):
#     pass

# else:
#     pass










