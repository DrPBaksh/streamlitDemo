import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Set page configuration
st.set_page_config(page_title="Retirement Calculator", layout="wide")

# Custom CSS to improve the look and feel
st.markdown("""
<style>
    .reportview-container {
        background-color: #f0f2f6;
    }
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    h1, h2, h3 {
        color: #1f3d7a;
    }
    .stButton>button {
        color: #ffffff;
        background-color: #1f3d7a;
        border: none;
        border-radius: 4px;
        padding: 0.5rem 1rem;
    }
    .stButton>button:hover {
        background-color: #2c5299;
    }
    .css-1aumxhk {
        background-color: #ffffff;
        border-radius: 4px;
        padding: 1rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.12), 0 1px 2px rgba(0,0,0,0.24);
    }
</style>
""", unsafe_allow_html=True)

# Function to calculate retirement (unchanged)
def calculate_retirement(current_age, final_savings_goal, current_deposit, savings_interest, yearly_deposit):
    age = current_age
    savings = current_deposit
    years = []
    savings_over_time = []

    while savings < final_savings_goal:
        savings += yearly_deposit
        savings *= (1 + savings_interest / 100)
        age += 1
        years.append(age)
        savings_over_time.append(savings)

        if age > 100:  # Set a maximum age to prevent infinite loops
            break

    return age, years, savings_over_time

# Custom color palette
colors = ['#1f3d7a', '#3498db', '#2ecc71', '#e74c3c', '#f39c12']

# App title and description
st.title('Professional Retirement Calculator')
st.markdown("""
This advanced tool helps you plan your financial future by projecting your savings growth
and estimating your retirement age based on your current financial situation and goals.
""")

# Create two columns for input fields
col1, col2 = st.columns(2)

with col1:
    st.subheader("Financial Goals")
    final_savings_goal = st.number_input('Final Savings Goal ($)', min_value=0, value=1000000, step=10000, format="%d")
    current_deposit = st.number_input('Current Savings ($)', min_value=0, value=10000, step=1000, format="%d")

with col2:
    st.subheader("Savings Parameters")
    savings_interest = st.number_input('Annual Interest Rate (%)', min_value=0.0, max_value=20.0, value=5.0, step=0.1, format="%.1f")
    yearly_deposit = st.number_input('Yearly Deposit ($)', min_value=0, value=10000, step=1000, format="%d")

st.subheader("Personal Information")
current_age = st.slider('Current Age', min_value=18, max_value=80, value=30, step=1)

if st.button('Calculate Retirement Projection'):
    retirement_age, years, savings_over_time = calculate_retirement(
        current_age, final_savings_goal, current_deposit, savings_interest, yearly_deposit
    )

    # Display retirement age
    st.header('Retirement Projection Results')
    if retirement_age <= 100:
        st.success(f'You are projected to reach your savings goal at age {retirement_age}')
    else:
        st.error('You may not reach your savings goal before age 100 with the current parameters')

    # Create and display the graph
    fig, ax = plt.subplots(figsize=(12, 6))
    sns.set_style("whitegrid")
    sns.set_palette(sns.color_palette(colors))
    
    ax.plot(years, savings_over_time, label='Savings Growth', linewidth=2)
    ax.axhline(y=final_savings_goal, color=colors[3], linestyle='--', label='Savings Goal', linewidth=2)
    
    ax.set_xlabel('Age', fontsize=12)
    ax.set_ylabel('Savings ($)', fontsize=12)
    ax.set_title('Savings Growth Projection', fontsize=16, fontweight='bold')
    ax.legend(fontsize=10)
    ax.grid(True, linestyle='--', alpha=0.7)
    
    # Format y-axis labels to show as millions/thousands
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x/1e6:.1f}M' if x >= 1e6 else f'${x/1e3:.0f}K'))
    
    plt.tight_layout()
    st.pyplot(fig)