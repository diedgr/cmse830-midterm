# Import packages
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Import data
csv_file_path = 'V-Dem-CPD-Party-V2.csv'
data = pd.read_csv(csv_file_path)

# Add a title, caption, and introductory paragraph
st.title("Exploring the Positions and Ideologies of Political Parties")
st.caption("Source: [V-Party Dataset](https://www.v-dem.net/data/v-party-dataset/country-party-date-v2/)")
st.write("This visualization presents time-series data of the ideological positions of major political parties from 178 countries. The data is sourced from the V-Party dataset, which includes assessments of party organization and identity as reflected by experts in political science.")
st.write("Below, there are **two interactive visuals**. The first allows the user to view the political positions for parties for a given country, based on a key issue. The scoring system can be used to determine the meaning behind these position scores. The second visual outlines the position score in relation to the parties ideological position on the social and economic spectrum.")

# Dictionary mapping variable names to user-friendly labels
label_map = {
    "v2paanteli": "Anti-Elitism",
    "v2papeople": "People-Centrism",
    "v2paopresp": "Political Opponents",
    "v2paplur": "Political Pluralism",
    "v2paminor": "Minority Rights",
    "v2paviol": "Rejection of Political Violence",
    "v2paimmig": "Immigration",
    "v2palgbt": "LGBT Social Equality",
    "v2paculsup": "Cultural Superiority",
    "v2parelig": "Religious Principles",
    "v2pagender": "Gender Equality",
    "v2pawomlab": "Working Women"
}

# Function to format the select box display
def format_func(key):
    return label_map[key]

# Sidebar for user input
st.sidebar.header("Select Options")
country_name = st.sidebar.selectbox("Select Country", data['country_name'].unique())
identity_score = st.sidebar.selectbox(
    "Select Party Position",
    options=list(label_map.keys()),
    format_func=format_func
)

filtered_data = data[data['country_name'] == country_name]

# Create a line graph with Plotly
party_options = filtered_data['v2paenname'].unique()

# Filter the party options based on the filtered data
filtered_party_options = filtered_data['v2paenname'].unique()

party_colors = {party: px.colors.qualitative.Plotly[i % len(px.colors.qualitative.Plotly)] for i, party in enumerate(party_options)}
fig = px.line(filtered_data, x='year', y=identity_score, color='v2paenname', color_discrete_map=party_colors, labels={'year': 'Year', identity_score: label_map[identity_score]})
if identity_score == 'v2pariglef_osp':
    fig.update_yaxes(title=label_map[identity_score])
else:
    fig.update_yaxes(title=label_map[identity_score])

# Set a custom range for the x-axis
min_year = filtered_data['year'].min()
max_year = filtered_data['year'].max()
fig.update_layout(xaxis=dict(range=[min_year, max_year]))

# Add subheader and introductory paragraph for graph
st.header(f"Scores for Parties in {country_name}")
st.write(f"This line graph examines party positions related to {label_map[identity_score].lower()} across time. To better interpret these scores, please use the question and coding boxes for more information.")

# Remove the legend from the graph
fig.update_traces(showlegend=False)

# Display the line graph
st.plotly_chart(fig)

# Set up the layout for the legend and additional information
col1, col2 = st.columns([3, 3])

# Display the legend in col1
with col1:
    st.subheader("Legend")
    for party in filtered_party_options:
        color = party_colors[party]
        if filtered_data[filtered_data['v2paenname'] == party][identity_score].notna().any():
            st.write(f"<div style='display: flex; align-items: center;'><div style='background-color: {color}; width: 20px; height: 10px; margin-right: 5px;'></div> {party}</div>", unsafe_allow_html=True)

# Dictionary mapping variable names to corresponding questions
question_map = {
    "v2paanteli": "How important is anti-elite rhetoric for this party?",
    "v2papeople": "Do leaders of this party glorify the ordinary people and identify themselves as part of them?",
    "v2paopresp": "Prior to this election, have leaders of this party used severe personal attacks or tactics of demonization against their opponents?",
    "v2paplur": "Prior to this election, to what extent was the leadership of this political party clearly committed to free and fair elections with multiple parties, freedom of speech, media, assembly and association?",
    "v2paminor": "According to the leadership of this party, how often should the will of the majority be implemented even if doing so would violate the rights of minorities?",
    "v2paviol": "To what extent does the leadership of this party explicitly discourage the use of violence against domestic political opponents?",
    "v2paimmig": "What is the party’s position regarding immigration into the country?",
    "v2palgbt": "What is this party’s position toward social equality for the lesbian, gay, bisexual, and transgender (LGBT) community?",
    "v2paculsup": "To what extent does the party leadership promote the cultural superiority of a specific social group or the nation as a whole?",
    "v2parelig": "To what extent does this party invoke God, religion, or sacred/religious texts to justify its positions?",
    "v2pagender": "What is the share of women in national-level leadership positions of this political party?",
    "v2pawomlab": "To what extent does this party support the equal participation of women in the labor market?"
}

# Dictionary mapping variable names to corresponding coding system
coding_map = {
    "v2paanteli": [
        "0: Not at all important. The leadership of this party never makes statements against the elite.",
        "1: Not important. The leadership of this party rarely makes statements against the elite.",
        "2: Somewhat important. The leadership of this party sometimes makes statements against the elite.",
        "3: Important. The leadership of this party often makes statements against the elite.",
        "4: Very important. The leadership of this party makes statements against the elite whenever possible."
    ],
    "v2papeople": [
        "0: Never. The party leadership never glorifies and identifies with the ordinary people.",
        "1: Usually not. The party leadership generally does not glorify and identify with the ordinary people.",
        "2: About half of the time. The party leadership sometimes glorifies and identifies with the ordinary people.",
        "3: Usually. The party leadership generally glorifies and identifies with the ordinary people, which they claim to represent.",
        "4: Always. The party leadership always glorifies and identifies with the ordinary people, which they claim to represent."
    ],
    "v2paopresp": [
        "0: Always. Party leaders always used severe personal attacks or tactics of demonization against their opponents.",
        "1: Usually. Party leaders usually used severe personal attacks or tactics of demonization against their opponents.",
        "2: About half of the time. Party leaders sometimes used severe personal attacks or tactics of demonization against their opponents.",
        "3: Usually not. Party leaders usually did not use severe personal attacks or tactics of demo- nization against their opponents.",
        "4: Never. Party leaders never used severe personal attacks or tactics of demonization against their opponents."
    ],
    "v2paplur": [
        "0: Not at all committed. The party leadership was not at all committed to free and fair, multi-party elections, freedom of speech, media, assembly and association.",
        "1: Not committed. The party leadership was not committed to free and fair, multi-party elections, freedom of speech, media, assembly and association.",
        "2: Weakly committed. The party leadership was weakly committed to free and fair, multi- party elections, freedom of speech, media, assembly and association.",
        "3: Committed. The party leadership was committed to free and fair, multi-party elections, freedom of speech, media, assembly and association.",
        "4: Fully committed. The party leadership was fully committed to free and fair, multi-party elections, freedom of speech, media, assembly and association."
    ],
    "v2paminor": [
        "0: Always. The leadership of this party argues that the will of the majority should always determine policy even if such policy violates minority rights.",
        "1: Usually. The leadership of this party argues that the will of the majority should usually determine policy even if such policy violates minority rights.",
        "2: Half of the time. The leadership of this party argues that the will of the majority should about half of the time determine policy even if such policy violate minority rights.",
        "3: Usually not. The leadership of this party argues that the will of the majority should usually not determine policy if such policy violates minority rights.",
        "4: Never. The leadership of this party argues that the will of the majority should never determine policy if such policy violates minority rights."
    ],
    "v2paviol": [
        "0: Encourages. Leaders of this party often encourage the use of violence against domestic political opponents.",
        "1: Sometimes encourages. Leaders of this party sometimes encourage the use of violence against domestic political opponents and generally refrain from discouraging it.",
        "2: Discourages about half of the time. Leaders of this party occasionally discourage the use of violence against domestic political opponents, and do not encourage it.",
        "3: Generally discourages. Leaders of this party often discourage the use of violence against its domestic political opponents.",
        "4: Consistently discourages. Leaders of this party consistently reject the use of violence against its domestic political opponents."
    ],
    "v2paimmig": [
        "0: Strongly opposes. This party strongly opposes all or almost all forms of immigration into the country.",
        "1: Opposes. This party opposes most forms of immigration into the country.",
        "2: Ambiguous/No position. This party has no clear policy with regard to immigration into the country.",
        "3: Supports. This party supports most forms of immigration into the country.",
        "4: Strongly supports. This party strongly supports all or almost all forms of immigration into the country."
    ],
    "v2palgbt": [
        "0: Strongly opposes. This party is strongly opposed to LGBT social equality.",
        "1: Opposes. This party is opposed to LGBT social equality.",
        "2: Ambiguous/No position. This party has no clear policy with regard to LGBT social equality.",
        "3: Supports. This party supports LGBT social equality.",
        "4: Strongly supports. This party strongly supports LGBT social equality."
    ],
    "v2paculsup": [
        "0: Strongly promotes. The party strongly promotes the cultural superiority of a specific social group or the nation as a whole.",
        "1: Promotes. The party promotes the cultural superiority of a specific social group or the nation as a whole.",
        "2: Ambiguous. The party does not take a specific position on the cultural superiority of a specific social group or the nation as a whole.",
        "3: Opposes. The party opposes the promotion of the cultural superiority of a specific social group or the nation as a whole.",
        "4: Strongly opposes. The party strongly opposes the promotion of the cultural superiority of a specific social group or the nation as a whole."
    ],
    "v2parelig": [
        "0: Always, or almost always. The party almost always invokes God, religion, or sacred/religious texts to justify its positions.",
        "1: Often, but not always. The party often, but not always, invokes God, religion, or religious texts to justify its positions.",
        "2: About half of the time. The party about half of the time invokes God, religion, or religious texts to justify its positions.",
        "3: Rarely. The party rarely invokes God, religion, or religious texts to justify its positions.",
        "4: Never. The party never invokes God, religion, or religious texts to justify its positions."
    ],
    "v2pagender": [
        "0: None.",
        "1: Small minority (about 1-15%).",
        "2: Medium minority (about 16-25%).",
        "3: Large minority (about 26-39%).",
        "4: Balanced (about 40% or more)."
    ],
    "v2pawomlab": [
        "0: Strongly opposes. This party strongly opposes all or almost all types of measures that support the equal participation of women in the labor market.",
        "1: Opposes. This party opposes most types of measures that support the equal participation of women in the labor market.",
        "2: Ambiguous/No position. This party has no clear policy with regard to measures that support the equal participation of women in the labor market.",
        "3: Supports. This party supports most types of measures that support the equal participation of women in the labor market.",
        "4: Strongly supports. This party strongly supports all or almost all types of measures that support the equal participation of women in the labor market."
    ],
}

# Question and coding display
with col2:
    st.subheader("Scoring System")
    if identity_score in label_map:
        with st.expander("Question"):
            st.write(question_map[identity_score])
        with st.expander("Coding"):
            for rating in coding_map[identity_score]:
                st.write(rating)

# Title and introductory paragraph for 3D scatter plot
st.markdown(f"<h2 style='padding-top: 20px;'><b>{label_map[identity_score]} on Political Spectrum</b></h2>", unsafe_allow_html=True)
st.write(f"This interactive 3D scatter plot compares three contemporary variables: a party's economic ideology, social ideology, and {label_map[identity_score].lower()} position.")

# Define function to map integer scores to categories for economic position
def map_economic_category(score):
    if score < 1:
        return "Far-Left"
    elif score < 2:
        return "Left"
    elif score < 3:
        return "Center-Left"
    elif score < 4:
        return "Center"
    elif score < 5:
        return "Center-Right"
    elif score < 6:
        return "Right"
    else:
        return "Far-Right"

# Define function to map integer scores to categories for social position
def map_social_category(score):
    if score < 2:
        return "Very Liberal"
    elif score < 4:
        return "Liberal"
    elif score < 7:
        return "Moderate"
    elif score < 9:
        return "Conservative"
    else:
        return "Very Conservative"

# 3D Scatter plot creation
fig_3d = go.Figure(data=[go.Scatter3d(
    x=filtered_data['v2pariglef_osp'],
    y=filtered_data['ep_v6_lib_cons'],
    z=filtered_data[identity_score],
    text=[f"<b>Party:</b> {party}<br><b>Economic Position:</b> {map_economic_category(x)}<br><b>Social Position:</b> {map_social_category(y)}<br><b>{label_map[identity_score]}:</b> {z}" 
          for party, x, y, z in zip(filtered_data['v2paenname'], filtered_data['v2pariglef_osp'], filtered_data['ep_v6_lib_cons'], filtered_data[identity_score])],  # update the text
    hovertemplate=' %{text} <extra></extra>',  # remove X, Y, and Z labels
    mode='markers',
    marker=dict(
        size=8,
        color=[party_colors[party] for party in filtered_data['v2paenname']],  # set color to the party color from party_colors
        colorscale='Viridis',  # choose a colorscale
        opacity=0.8
    )
)])

# Layout configuration for the 3D scatter plot
fig_3d.update_layout(scene=dict(
    xaxis_title='Economic Left-Right Scale',
    yaxis_title='Social Liberalism-Conservatism Scale',
    zaxis_title=label_map[identity_score],
    xaxis=dict(title=dict(font=dict(size=12)), range=[6, 0]),  # reverse the range
    yaxis=dict(title=dict(font=dict(size=12))),
    zaxis=dict(title=dict(font=dict(size=12))),
), 
margin=dict(l=0, r=0, b=0, t=0))

# Configuring the frame
fig_3d.update_layout(scene_aspectmode='cube',
                    scene_aspectratio=dict(x=1, y=1, z=0.8))

# Display the 3D scatter plot
st.plotly_chart(fig_3d)