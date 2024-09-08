import streamlit as st
import pandas as pd

# Load the restaurant data from the CSV file
df = pd.read_csv("food1.csv")

# Title and UI Layout
st.title("Restaurants Spotter")
st.markdown("### Welcome to the City of Nawabs! 🤴")

# Restaurant search form
st.markdown("#### Find the perfect restaurant for your dining experience!")

# Create the form
with st.form("restaurant_form"):
    people = st.number_input("Number of People", min_value=1, step=1, value=1)
    min_price = st.number_input("Min Budget", min_value=0, step=1, value=0)
    max_price = st.number_input("Max Budget", min_value=0, step=1, value=0)

    cuisine = st.selectbox(
        "Cuisine",
        ["North Indian", "Mughlai", "Chinese", "South Indian", "Awadhi", "Continental", "Desserts", "Bakery", "Fast Food"]
    )
    
    locality = st.selectbox(
        "Locality",
        ["Aliganj", "Aminabad", "Gomti Nagar", "Chowk", "Hazratganj", "Lalbagh", "Kaiserbagh", "RajajiPuram", "Charbagh", "Mahanagar", "Khurram Nagar"]
    )

    # Submit button
    submit_button = st.form_submit_button(label="Get Restaurants")

# Handle form submission
if submit_button:
    st.markdown(f"### Results for {people} people, {cuisine} cuisine in {locality}")
    
    # Filter the data based on user inputs
    filtered_restaurants = df[
        (df["Cuisine"].str.contains(cuisine, case=False)) & 
        (df["Locality"].str.contains(locality, case=False)) &
        (df["Price"] >= min_price) & 
        (df["Price"] <= max_price)
    ]

    if not filtered_restaurants.empty:
        for idx, row in filtered_restaurants.iterrows():
            st.markdown(f"**{row['Name']}**")
            st.markdown(f"Rating: {row['Rating']} ⭐")
            st.markdown(f"Address: {row['Address']}")
            st.markdown(f"Timings: {row['Timings']}")
            st.markdown("---")
    else:
        st.markdown("### Sorry, no restaurants found! Try a different search.")

# Footer
st.markdown(
    """
    <div style="text-align: center; background-color: rgb(12, 12, 12, 0.6); padding: 1rem;">
        <span style="color: white; font-weight: bold;">Developed by <b style="color: chartreuse;">Sarvesh Sharma</b></span>
        <br><br>
        <a href="https://github.com/shsarv" target="_blank" style="font-size:xx-large; color: #d5d7da;">
            <i class="fa fa-github" aria-hidden="true"></i>
        </a>&emsp;
        <a href="https://www.linkedin.com/in/sarvesh-kumar-sharma-869a1b185/" target="_blank" style="font-size:xx-large; color: #0077B5;">
            <i class="fa fa-linkedin-square" aria-hidden="true"></i>
        </a>
    </div>
    """,
    unsafe_allow_html=True
)
