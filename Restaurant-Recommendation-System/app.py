pip install streamlit pandas scikit-learn
import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load your dataset
lko_rest = pd.read_csv("food1.csv")

# Function to calculate recommendations based on cosine similarity
def fav(lko_rest1):
    lko_rest1 = lko_rest1.reset_index()
    count1 = CountVectorizer(stop_words='english')
    count_matrix = count1.fit_transform(lko_rest1['highlights'])
    cosine_sim2 = cosine_similarity(count_matrix, count_matrix)
    sim = list(enumerate(cosine_sim2[0]))
    sim = sorted(sim, key=lambda x: x[1], reverse=True)
    sim = sim[1:11]
    indi = [i[0] for i in sim]
    final = lko_rest1.copy().iloc[indi[0]].to_frame().T
    for i in range(1, len(indi)):
        final = pd.concat([final, lko_rest1.copy().iloc[indi[i]].to_frame().T])
    return final

# Function for restaurant recommendations based on filters
def rest_rec(cost, people=2, min_cost=0, cuisine=[], locality=[], fav_rest=""):
    x = cost / people
    y = min_cost / people
    filtered_rest = lko_rest[lko_rest['locality'].isin(locality)]
    filtered_rest = filtered_rest[
        (filtered_rest['average_cost_for_one'] <= x) & (filtered_rest['average_cost_for_one'] >= y)
    ]
    filtered_rest['Start'] = filtered_rest['cuisines'].apply(lambda x: any(c in x for c in cuisine))
    filtered_rest = filtered_rest[filtered_rest['Start']]

    if fav_rest:
        favr = lko_rest[lko_rest['name'] == fav_rest].drop_duplicates()
        rest_selected = fav(pd.concat([favr, filtered_rest]))
    else:
        filtered_rest = filtered_rest.sort_values('scope', ascending=False)
        rest_selected = filtered_rest.head(10)
    return rest_selected

# Streamlit app code
st.title("Restaurant Spotter")
st.write("Welcome to the City of Nawabs! Let us help you find the best restaurants based on your preferences.")

# Form to take user input
with st.form(key="restaurant_search_form"):
    people = st.number_input("No. of People", min_value=1, value=2)
    min_Price = st.number_input("Minimum Budget", min_value=0, value=0)
    max_Price = st.number_input("Maximum Budget", min_value=0, value=500)
    cuisine = st.multiselect("Select Cuisine", ['North Indian', 'Mughlai', 'Chinese', 'South Indian', 'Awadhi', 'Continental', 'Desserts', 'Bakery', 'Fast Food'])
    locality = st.multiselect("Select Locality", ['Aliganj', 'Aminabad', 'Gomti Nagar', 'Chowk', 'Hazratganj', 'Lalbagh', 'Kaiserbagh', 'RajajiPuram', 'Charbagh', 'Mahanagar', 'Khurram Nagar'])
    fav_rest = st.text_input("Favorite Restaurant (Optional)")
    
    submit_button = st.form_submit_button(label="Get Restaurant Recommendations")

# Handle form submission
if submit_button:
    if not cuisine or not locality:
        st.error("Please select at least one cuisine and one locality.")
    else:
        recommendations = rest_rec(max_Price, people, min_Price, cuisine, locality, fav_rest)
        if recommendations.empty:
            st.write("Sorry, no restaurants found based on your criteria.")
        else:
            st.write("Here are some restaurant recommendations:")
            st.dataframe(recommendations[['name', 'address', 'locality', 'timings', 'aggregate_rating', 'url', 'cuisines']])

# Footer
st.markdown("""
<div style='text-align: center; color: white; background-color: black; padding: 10px;'>
    Developed by <b>Sarvesh Sharma</b> 
    <a href='https://github.com/shsarv' target='_blank'><i class='fa fa-github'></i></a> 
    <a href='https://www.linkedin.com/in/sarvesh-kumar-sharma-869a1b185/' target='_blank'><i class='fa fa-linkedin'></i></a>
</div>
""", unsafe_allow_html=True)
