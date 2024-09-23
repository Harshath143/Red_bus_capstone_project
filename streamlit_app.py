import streamlit as st
import pandas as pd

# Load dataset with the new cache_data method
@st.cache_data
def load_data():
    data = pd.read_csv('Final_df.csv')
    return data

df = load_data()

# Set custom styles using markdown and CSS
st.markdown("""
    <style>
    /* App background and text styles */
    .stApp {
        background: url('https://www.hdwallpapers.in/download/red_black_white_geometric_shapes_4k_hd_geometric-HD.jpg');
        background-size: cover;
    }
    
    /* Style the title */
    .title h1 {
        color: #fff;
        font-size: 3.5em;
        font-family: 'Arial', sans-serif;
        text-align: center;
        margin-bottom: 20px;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.4);
    }
    
    /* Style the filter widgets */
    .stSlider label, .stMultiSelect label {
        font-size: 1.2em;
        color: #fff;
        text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.5);
    }
    
    /* Style the cards */
    .card {
        background-color: #ecf0f1;
        border: 1px solid #bdc3c7;
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }
    
    /* Style headers */
    .header-img {
        display: block;
        margin-left: auto;
        margin-right: auto;
        width: 50%;
    }
    </style>
""", unsafe_allow_html=True)

# App header with an image
st.markdown("""
    <div style="text-align: center;">
        <img src="https://th.bing.com/th/id/OIP.CdbTjbHPhZtQcUwZwmbshgHaE5?w=296&h=196&c=7&r=0&o=5&dpr=1.3&pid=1.7" width="300" />
        <h3 style="color: white;">Red Bus Filtering Dashboard</h3>
    </div>
""", unsafe_allow_html=True)

# Two-column layout: filters on the left and results on the right
left_column, right_column = st.columns(2)

with left_column:
    # App title with styling
    st.markdown("<div class='title'><h1>🚍 Bus Filters</h1></div>", unsafe_allow_html=True)

    # Route Name filter
    st.markdown("### 🛣️ Route Name")
    route_name = st.multiselect("Select Route Name:", options=df['Route_name'].unique())

    # Bus Name filter
    st.markdown("### 🚌 Bus Operator")
    bus_name = st.multiselect("Select Bus Operator:", options=df['Bus_name'].unique())

    # Bus Type filter
    st.markdown("### 🚍 Bus Type")
    bus_type = st.multiselect("Select Bus Type:", options=df['Bus_type'].unique())

    # Start Time filter
    st.markdown("### ⏰ Start Time")
    start_time = st.slider("Select Start Time (in hours):", 0, 23, (0, 23), format="%d:00")

    # End Time filter
    st.markdown("### ⏰ End Time")
    end_time = st.slider("Select End Time (in hours):", 0, 23, (0, 23), format="%d:00")

    # Price filter with emoji
    st.markdown("### 💰 Price Range")
    price_range = st.slider("Select Price Range:", float(df['price'].min()), float(df['price'].max()), 
                            (float(df['price'].min()), float(df['price'].max())), step=1.0)

    # Seats Available filter
    st.markdown("### 🪑 Seats Available")
    seats_available = st.slider("Select Seat Availability:", 0, df['Seats_Available'].apply(lambda x: int(str(x).split()[0])).max(), 
                                (0, df['Seats_Available'].apply(lambda x: int(str(x).split()[0])).max()), step=1)

    # Ratings filter
    st.markdown("### ⭐ Ratings")
    ratings = st.slider("Select Rating Range:", float(df['Ratings'].min()), float(df['Ratings'].max()), 
                        (float(df['Ratings'].min()), float(df['Ratings'].max())), step=0.1)

with right_column:
    # Apply filters
    filtered_df = df[
        (df['Route_name'].isin(route_name) if route_name else True) &
        (df['Bus_name'].isin(bus_name) if bus_name else True) &
        (df['Bus_type'].isin(bus_type) if bus_type else True) &
        (df['Start_time'].apply(lambda x: int(x.split(":")[0])).between(start_time[0], start_time[1])) &
        (df['End_time'].apply(lambda x: int(x.split(":")[0])).between(end_time[0], end_time[1])) &
        (df['price'].between(price_range[0], price_range[1])) &
        (df['Seats_Available'].apply(lambda x: int(str(x).split()[0])).between(seats_available[0], seats_available[1])) &
        (df['Ratings'].between(ratings[0], ratings[1]))
    ]

    # Display filtered data as cards
    st.markdown("<div class='title'><h1>📝 Filtered Results</h1></div>", unsafe_allow_html=True)

    if not filtered_df.empty:
        for index, row in filtered_df.iterrows():
            st.markdown(f"""
                <div class="card">
                    <h4>🚍 {row['Bus_name']}</h4>
                    <p><strong>Route:</strong> {row['Route_name']}</p>
                    <p><strong>Type:</strong> {row['Bus_type']}</p>
                    <p><strong>Start Time:</strong> {row['Start_time']}</p>
                    <p><strong>End Time:</strong> {row['End_time']}</p>
                    <p><strong>Price:</strong> ₹{row['price']}</p>
                    <p><strong>Seats Available:</strong> {row['Seats_Available']}</p>
                    <p><strong>Ratings:</strong> ⭐{row['Ratings']}</p>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown("<p style='color: red;'>No results found. Please adjust your filters.</p>")
