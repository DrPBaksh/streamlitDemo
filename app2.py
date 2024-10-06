import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.title('Retirement Savings Calculator')

# Inputs - Collecting user inputs for retirement goal, current savings, interest rate, yearly deposits, and current age
final_goal = st.number_input('Final Savings Goal', min_value=0, value=1000000, step=1000)
st.write(f"Final Savings Goal: {final_goal}")
current_deposit = st.number_input('Current Deposit', min_value=0, value=10000, step=1000)
st.write(f"Current Deposit: {current_deposit}")
savings_interest = st.number_input('Savings Interest Rate (in %)', min_value=0.0, value=5.0, step=0.1)
st.write(f"Savings Interest Rate: {savings_interest}")
yearly_deposit = st.number_input('Yearly Deposit', min_value=0, value=10000, step=1000)
st.write(f"Yearly Deposit: {yearly_deposit}")
current_age = st.number_input('Current Age', min_value=0, value=30, step=1)
st.write(f"Current Age: {current_age}")

# Constants - Calculating interest rate as a decimal value
interest_rate = savings_interest / 100
st.write(f"Interest Rate: {interest_rate}")

# Calculations - Initializing lists to keep track of savings growth over the years
years = []
savings = []
age = current_age
current_savings = current_deposit
i = 0

st.write("Starting calculations...")
# Loop to calculate yearly savings until the savings goal is reached
while current_savings < final_goal:
    st.write(f"Year {i}: Savings = {current_savings}")
    years.append(i)  # Adding current year to the list
    savings.append(current_savings)  # Adding current savings to the list
    # Calculating savings for the next year by adding yearly deposit and interest
    current_savings += yearly_deposit + current_savings * interest_rate
    i += 1  # Incrementing year count
    age += 1  # Incrementing age

# Append the final year when goal is met
st.write(f"Year {i}: Savings = {current_savings}")
years.append(i)
savings.append(current_savings)
retirement_age = age  # Storing the age at which the goal is met

# Display graph - Plotting savings growth over time
fig, ax = plt.subplots()
ax.plot(years, savings, label='Savings Over Time')
ax.axhline(y=final_goal, color='r', linestyle='-', label='Savings Goal')  # Horizontal line indicating savings goal
ax.set_xlabel('Years')
ax.set_ylabel('Savings ($)')
ax.set_title('Savings Growth Over Time')
ax.legend()
st.pyplot(fig)

# Display retirement age
st.write(f"You will reach your savings goal at age: {retirement_age}")

# Display table - Creating and displaying a DataFrame to show savings growth over the years
data = {'Year': years, 'Savings ($)': savings}
df = pd.DataFrame(data)
st.write('Savings Growth Table:')
st.dataframe(df)