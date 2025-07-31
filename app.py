import streamlit as st
import pandas as pd

# Step 1: Load and clean the data
@st.cache_data
def load_data():
    df = pd.read_csv("C:/Users/sarth/Downloads/restaurant recomendation system/Dataset  (2).csv", encoding="latin-1")
    df = df[["Restaurant Name", "Cuisines", "Average Cost for two", "Aggregate rating", "City"]]
    df.dropna(inplace=True)
    df["City"] = df["City"].astype(str).str.strip().str.lower()
    df["Cuisines"] = df["Cuisines"].astype(str).str.strip().str.lower()
    return df

df = load_data()

# Step 2: Define the recommendation function
def recommend_restaurants(cuisine, min_price, max_price, city, top_n=5):
    city = city.strip().lower()
    cuisine = cuisine.strip().lower()

    st.write(f"➡ Total records before filtering: {len(df)}")

    # City filter
    filtered_df = df[df["City"] == city]
    st.write("➡ After city filter:", len(filtered_df))

    # Cuisine filter
    filtered_df = filtered_df[filtered_df["Cuisines"].str.contains(cuisine, na=False)]
    st.write("➡ After cuisine filter:", len(filtered_df))

    # Price range filter
    filtered_df = filtered_df[
        (filtered_df["Average Cost for two"] >= min_price) &
        (filtered_df["Average Cost for two"] <= max_price)
    ]
    st.write("➡ After price filter:", len(filtered_df))

    if filtered_df.empty:
        st.error("❌ No restaurants found matching the criteria.")
        return None

    sorted_df = filtered_df.sort_values(by="Aggregate rating", ascending=False)
    return sorted_df.head(top_n)

# Streamlit UI
st.title("🍽️ Restaurant Recommendation System")

city = st.text_input("Enter City (e.g., Delhi)")
cuisine = st.text_input("Enter Cuisine (e.g., North Indian)")
min_price = st.number_input("Minimum Cost for Two", min_value=0, value=100)
max_price = st.number_input("Maximum Cost for Two", min_value=0, value=1000)
top_n = st.slider("Number of Recommendations", min_value=1, max_value=10, value=5)


if st.button("Recommend"):
    if city and cuisine:
        results = recommend_restaurants(cuisine, min_price, max_price, city, top_n)
        if results is not None:
            st.success("✅ Top Matches:")
            for i, row in results.iterrows():
                st.markdown(f"**{row['Restaurant Name']}**  \n"
                            f"*Cuisine:* {row['Cuisines']}  \n"
                            f"*Cost for two:* ₹{row['Average Cost for two']}  \n"
                            f"*Rating:* ⭐ {row['Aggregate rating']}")
    else:
        st.warning("Please enter both city and cuisine to proceed.")