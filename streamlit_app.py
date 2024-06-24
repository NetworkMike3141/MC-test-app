import streamlit as st
import requests
import random
import pandas as pd
import matplotlib.pyplot as plt

st.title('Pokemon Explorer!')

pokemon_number = st.number_input('Please select your Pokemon!', min_value=1, max_value=1010, step=1)

def get_pokemon_data(pokemon_number):
    url = f"https://pokeapi.co/api/v2/pokemon/{pokemon_number}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

data = get_pokemon_data(pokemon_number) 

pokemon_name = data['name']
pokemon_height = data['height']
pokemon_weight = data['weight']
base_experience = data['base_experience']
pokemon_sprite_url = data['sprites']['front_default']


st.title(pokemon_name.title())
st.write(f"This Pokemon is {pokemon_height / 10} meters tall, weighs {pokemon_weight / 10} kg, and has a base experience of {base_experience}!")
st.image(pokemon_sprite_url, width=300)

random_pokemon_nums = random.sample(range(1, 1011), 10)

random_pokemon_data = []
for num in random_pokemon_nums:
    pokemon_data = get_pokemon_data(num)
    random_pokemon_data.append(pokemon_data) 

names = [pokemon_name.title()] + [pokemon['name'].title() for pokemon in random_pokemon_data]
heights = [pokemon_height / 10] + [pokemon['height'] / 10 for pokemon in random_pokemon_data]
weights = [pokemon_weight / 10] + [pokemon['weight'] / 10 for pokemon in random_pokemon_data]
base_experiences = [base_experience] + [pokemon['base_experience'] for pokemon in random_pokemon_data]

comparison_data = {
    'Height': heights,
    'Weight': weights,
    'Base Experience': base_experiences
    }

df = pd.DataFrame(comparison_data, index=names)

st.subheader('Comparison with 10 random Pokemon')

fig, axes = plt.subplots(3, 1, figsize=(10, 25))

df['Height'].plot(kind='bar', ax=axes[0], legend=False)
axes[0].set_title('Height Comparison')
axes[0].set_ylabel('Height (m)')

df['Weight'].plot(kind='bar', ax=axes[1], legend=False)
axes[1].set_title('Weight Comparison')
axes[1].set_ylabel('Weight (kg)')

df['Base Experience'].plot(kind='bar', ax=axes[2], legend=False)
axes[2].set_title('Base Experience Comparison')
axes[2].set_ylabel('Base Experience')

plt.tight_layout()
st.pyplot(fig)
