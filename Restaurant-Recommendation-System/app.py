import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load the dataset
lko_rest = pd.read_csv("food1.csv")

# Define the fav function
def fav(lko_rest1):
    lko_rest1 = lko_rest1.reset_index()
    count1 = CountVectorizer(stop_words='english')
    count_matrix = count1.fit_transform(lko_rest1['highlights'])
    cosine_sim2 = cosine_similarity(count_matrix, count_matrix)

    sim = list(enumerate(cosine_sim2[0]))
    sim = sorted(sim, key=lambda x: x[1], reverse=True)
    sim = sim[1:11]
    indi = [i[0] for i in sim]

    final = lko_rest1.copy().iloc[indi[0]]
    final = pd.DataFrame(final)
    final = final.T

    for i in range(1, len(indi)):
        final1 = lko_rest1.copy().iloc[indi[i]]
        final1 = pd.DataFrame(final1)
        final1 = final1.T
        final = pd.concat([final, final1])

    return final

# Define the restaurant recommendation function
def rest_rec(cost, people=2, min_cost=0, cuisine=[], Locality=[], fav_rest="", lko_rest=lko_rest):
    cost = cost + 200
    x = cost / people
    y = min_cost / people

    lko_rest1 = lko_rest.copy().loc[lko_rest['locality'] == Locality[0]]

    for i in range(1, len(Locality)):
        lko_rest2 = lko_rest.copy().loc[lko_rest['locality'] == Locality[i]]
        lko_rest1 = pd.concat([lko_rest1, lko_rest2])
        lko_rest1.drop_duplicates(subset='name', keep='last', inplace=True)

    lko_rest_locale = lko_rest1.copy()

    lko_rest_locale = lko_rest_locale.loc[lko_rest_locale['average_cost_for_one'] <= x]
    lko_rest_locale = lko_rest_locale.loc[lko_rest_locale['average_cost_for_one'] >= y]

    lko_rest_locale['Start'] = lko_rest_locale['cuisines'].str.find(cuisine[0])
    lko_rest_cui = lko_rest_locale.copy().loc[lko_rest_locale['Start'] >= 0]

    for i in range(1, len(cuisine)):
        lko_rest_locale['Start'] = lko_rest_locale['cuisines'].str.find(cuisine[i])
        lko_rest_cu = lko_rest_locale.copy().loc[lko_rest_locale['Start'] >= 0]
        lko_rest_cui = pd.concat([lko_rest_cui, lko_rest_cu])
        lko_rest_cui.drop_duplicates(subset='name', keep='last', inplace=True)

    if fav_rest != "":
        favr = lko_rest.loc[lko_rest['name'] == fav_rest].drop_duplicates()
        favr = pd.DataFrame(favr)
        lko_rest3 = pd.concat([favr, lko_rest_cui])
        lko_rest3.drop('Start', axis=1, inplace=True)
        rest_selected = fav(lko_rest3)
    else:
        lko_rest_cui = lko_rest_cui.sort_values('scope', ascending=False)
        rest_selected = lko_rest_cui.head(10)
    
    return rest_selected

# Define the calculation function
def calc(max_Price, people, min_Price, cuisine, locality):
    rest_sugg = rest_rec(max_Price, people, min_Price, [cuisine], [locality])
    rest_list1 = rest_sugg.copy().loc[:, ['name', 'address', 'locality', 'timings', 'aggregate_rating', 'url', 'cuisines']]
    rest_list = pd.DataFrame(rest_list1)
    rest_list = rest_list.reset_index()
    rest_list = rest_list.rename(columns={'index': 'res_id'})
    rest_list.drop('res_id', axis=1, inplace=True)
    rest_list = rest_list.T
    rest_list = rest_list
    ans = rest_list.to_dict()
    res = [value for value in ans.values()]
    return res

# Streamlit application
st.title("Restaurant Recommender")

# Input form
with st.form(key="restaurant_form"):
    people = st.number_input("Number of People", min_value=1, step=1, value=2)
    min_Price = st.number_input("Minimum Price", min_value=0, step=100)
    max_Price = st.number_input("Maximum Price", min_value=0, step=100)
    cuisine1 = st.text_input("Cuisine", "Indian")
    locality1 = st.text_input("Locality", "Hazratganj")

    submit_button = st.form_submit_button(label="Search")

# Display results after form submission
if submit_button:
    res = calc(max_Price, people, min_Price, cuisine1, locality1)
    
    if len(res) > 0:
        st.subheader("Recommended Restaurants")
        for r in res:
            st.write(f"**Name:** {r['name']}")
            st.write(f"**Address:** {r['address']}")
            st.write(f"**Locality:** {r['locality']}")
            st.write(f"**Timings:** {r['timings']}")
            st.write(f"**Rating:** {r['aggregate_rating']}")
            st.write(f"**Cuisines:** {r['cuisines']}")
            st.write(f"**URL:** {r['url']}")
            st.markdown("---")
    else:
        st.write("No restaurants found matching your criteria.")
