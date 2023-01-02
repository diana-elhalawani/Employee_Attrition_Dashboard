''' Toulouse Business School MSc AIBA

Course: Advanced Python for Data Science -- PROJECT
Author: Diana El Halawani

App Description: Exploratory dashboard of employee attrition using streamlit

'''

# Import Libraries

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Define some variables
TITLE = 'Employee Attrition Analysis Dashboard'
CAPTION = 'Select a Department'

# Configure page settings
st.set_page_config(page_title='Employee Attrition Dashboard', layout='wide')

# Define functions


@st.cache
def load_data():
    """ Function to import data into a dataframe"""
    data = pd.read_csv(
        "C:/Users/diana/Documents/4.TBS/MScAI-BusinessAnalytics/Python1/EmployeeAttrition.csv")
    return data


def get_dept(data):
    """ Function that returns the unique values of departments """
    return data['Department'].unique().tolist()


@st.cache
def dept_filter(data, department):
    """ Function to filter the data by department """
    filter_data = data[data['Department'] == department]
    return filter_data


@st.cache
def group_data(data):
    """ Function to group data by Attrition """
    agg_data = data.groupby('Attrition').count()['EmployeeCount'].reset_index()
    return agg_data


# Use pd.Categorical in the function below to have an output with zero values
# For better charts (no gaps) later

def group_data_field(data, field):
    """ Function to group data by Attrition and another field for plotting - Data Preparation """
    agg_data = data.groupby([pd.Categorical(
        data[field]), 'Attrition']).count()['EmployeeCount'].reset_index()
    return agg_data


def split(data, condition):
    """ Function to split the data based on attrition """
    split_data = data[data['Attrition'] == condition]
    return split_data


def bar_chart_v(stayed, left, label):
    """ Function to plot a vertical bar chart """
    rc_1 = {'figure.figsize': (12, 10),
            'axes.facecolor': 'white',
            'axes.edgecolor': 'white',
            'axes.labelcolor': 'black',
            'figure.facecolor': 'white',
            'patch.edgecolor': 'white',
            'text.color': 'black',
            'xtick.color': 'black',
            'ytick.color': 'black',
            'grid.color': 'grey',
            'font.size': 10,
            'axes.labelsize': 16,
            'xtick.labelsize': 14,
            'ytick.labelsize': 14}
    plt.rcParams.update(rc_1)
    fig, ax_1 = plt.subplots()
    sns.set_theme(style='whitegrid')

    sns.set_color_codes('muted')
    sns.barplot(
        x=stayed.index,
        y='EmployeeCount',
        data=stayed,
        label='Employees that stayed',
        color='b',
        ci=None)
    sns.set_color_codes('muted')
    sns.barplot(
        x='level_0',
        y='EmployeeCount',
        data=left,
        label='Employees that left',
        color='r',
        ci=None)
    ax_1.set_xticklabels(stayed['level_0'])
    sns.set(font_scale=1.5)
    ax_1.legend(ncol=1, loc="upper right", frameon=True)
    ax_1.set(xlabel=label, ylabel='Number of Employees')
    plt.title(f"Attrition by {label}", fontsize=20)
    st.pyplot(fig)


def bar_chart_h(stayed, left, label):
    """ Function to plot a horizontal bar chart """
    rc_1 = {'figure.figsize': (20, 10),
            'axes.facecolor': 'white',
            'axes.edgecolor': 'white',
            'axes.labelcolor': 'black',
            'figure.facecolor': 'white',
            'patch.edgecolor': 'white',
            'text.color': 'black',
            'xtick.color': 'black',
            'ytick.color': 'black',
            'grid.color': 'grey',
            'font.size': 10,
            'axes.labelsize': 16,
            'xtick.labelsize': 14,
            'ytick.labelsize': 14}
    plt.rcParams.update(rc_1)
    fig, ax_1 = plt.subplots()
    sns.set_theme(style='whitegrid')

    sns.set_color_codes('muted')
    sns.barplot(
        x='EmployeeCount',
        y=stayed.index,
        data=stayed,
        label='Employees that stayed',
        color='b',
        ci=None,
        orient='h')
    sns.set_color_codes('muted')
    sns.barplot(
        x='EmployeeCount',
        y='level_0',
        data=left,
        label='Employees that left',
        color='r',
        ci=None,
        orient='h')
    ax_1.set_yticklabels(['Entry-level',
                          'Intermediate',
                          'First-level Mngmnt',
                          'Middle Mngmnt',
                          'Senior Mngmnt'])
    sns.set(font_scale=1.5)
    ax_1.legend(ncol=1, loc="upper right", frameon=True)
    ax_1.set(ylabel=label, xlabel='Number of Employees')
    plt.title(f"Attrition by {label}")
    st.pyplot(fig)


def pie_chart(data):
    """ Function to plot pie chart """
    rc_1 = {'figure.figsize': (12, 10)}
    plt.rcParams.update(rc_1)
    fig, ax_1 = plt.subplots()
    sns.set_color_codes('muted')
    colors = ['b', 'r']
    patches = ax_1.pie(
        data=data,
        x='EmployeeCount',
        labels=data['EmployeeCount'],
        colors=colors,
        textprops={
            'fontsize': 14})
    legend_labels = ['Employees that left', 'Employees that stayed']
    sns.set(font_scale=1.2)
    plt.legend(patches, legend_labels, loc='upper right')
    plt.title('Employee Attrition', fontsize=18)
    st.pyplot(fig)


def main():
    ''' Streamlit Wep App '''

    st.header(TITLE)

    employee_data = load_data()
    departments = ['ALL'] + get_dept(employee_data)
    selected_dept = st.selectbox(CAPTION, departments)

    if selected_dept == 'ALL':
        filter_data = employee_data
    else:
        filter_data = dept_filter(employee_data, selected_dept)

    row1_1, row1_2, row1_3 = st.columns((1, 1, 1))

    with row1_1:

        # Group the data
        agg_data = group_data_field(filter_data, 'BusinessTravel')

        # Split the data
        employees_stayed = split(agg_data, 'No')
        employees_left = split(agg_data, 'Yes')

        # Plot it
        bar_chart_v(employees_stayed, employees_left, 'Business Travel')

    with row1_2:

        # Group the data
        agg_data = group_data_field(filter_data, 'YearsAtCompany')

        # Split the data
        employees_stayed = split(agg_data, 'No')
        employees_left = split(agg_data, 'Yes')

        # Plot it
        bar_chart_v(employees_stayed, employees_left, 'Years At Company')

    with row1_3:

        # Group the data
        agg_data = group_data(filter_data)

        # Plot it
        pie_chart(agg_data)

    _, row3_1, _ = st.columns((0.2, 1, 0.2))

    with row3_1:

        # Group the data
        agg_data = group_data_field(filter_data, 'JobLevel')

        # Split the data
        employees_stayed = split(agg_data, 'No')
        employees_left = split(agg_data, 'Yes')

        # Plot it
        bar_chart_h(employees_stayed, employees_left, 'Job Level')


if __name__ == '__main__':
    main()
