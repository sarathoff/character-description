import streamlit as st
import random
import google.generativeai as gen_ai

# Configure Streamlit page settings
st.set_page_config(
    page_title="Character Description Generator",
    page_icon=":memo:",  # Favicon emoji
    layout="centered",  # Page layout option
)

# Directly set the API key here (not recommended for production)
GOOGLE_API_KEY = "AIzaSyDL_nopsrrujLZJuMjVbSLxjkC8B11LOMw"

# Set up Google Gemini-Pro AI model
gen_ai.configure(api_key=GOOGLE_API_KEY)
model = gen_ai.GenerativeModel('gemini-pro')

# Streamlit app layout
st.title("Character Description Generator")

# Predefined lists for random selection
names = ["John", "Emily", "Alex", "Sophia", "Michael", "Lily"]
traits = ["brave", "curious", "ambitious", "cunning", "loyal", "mysterious"]
backgrounds = ["a mysterious past", "a royal lineage", "a traumatic childhood", "a life of crime", "a humble beginning"]
occupations = ["warrior", "scholar", "thief", "merchant", "adventurer", "detective"]
genders = ["Male", "Female", "Non-binary"]
ages = range(18, 80)
appearances = ["tall and muscular", "slim and graceful", "short and stocky", "average height with a strong build"]
hair_colors = ["dark", "blonde", "red", "brown", "gray"]
eye_colors = ["blue", "green", "brown", "hazel", "gray"]
clothing_styles = ["modern", "vintage", "casual", "elegant", "worn-out"]
unique_features = ["a scar on the left cheek", "a tattoo of a dragon", "a pair of round glasses", "a missing finger", "piercing blue eyes"]

# Function to generate a random character description
def generate_random_character_description():
    character_name = random.choice(names)
    character_traits = random.choice(traits)
    character_background = random.choice(backgrounds)
    character_occupation = random.choice(occupations)
    character_gender = random.choice(genders)
    character_age = random.choice(ages)
    physical_appearance = f"{random.choice(appearances)}, with {random.choice(hair_colors)} hair and {random.choice(eye_colors)} eyes"
    clothing_style = random.choice(clothing_styles)
    unique_feature = random.choice(unique_features)

    return f"""
    Name: {character_name}
    Traits: {character_traits}
    Background: {character_background}
    Occupation: {character_occupation}
    Gender: {character_gender}
    Age: {character_age}
    Physical Appearance: {physical_appearance}
    Clothing Style: {clothing_style}
    Unique Features: {unique_feature}
    """

# Function to validate and generate character description based on user input
def validate_and_generate_description(name, gender, age, description):
    # Check for explicit or adult content
    if any(word in description.lower() for word in ["nudity", "adult", "explicit", "sexual"]):
        return generate_random_character_description(), True
    
    # Create prompt based on user input
    prompt = f"""
    Create a character description based on the following details:

    Name: {name if name else random.choice(names)}
    Gender: {gender if gender else random.choice(genders)}
    Age: {age if age else random.choice(ages)}
    Description: {description}

    Please include specific details on physical features, clothing, and any distinguishing marks to create a vivid visual image.
    """

    # Attempt to generate character description using the Gemini-Pro model
    try:
        response = model.generate_content([prompt])
        character_description = response.text

        # Check the generated response for inappropriate content
        if any(word in character_description.lower() for word in ["nudity", "adult", "explicit", "sexual"]):
            return generate_random_character_description(), True
    except:
        # If the LLM fails to respond
        return generate_random_character_description(), False
    
    return character_description, False

# Layout for user options
st.subheader("Choose an Option")
option = st.radio("Do you want to provide inputs or generate a random character?", 
                  ('Provide Inputs', 'Generate Random Character'))

if option == 'Provide Inputs':
    st.subheader("Optional Inputs")
    name = st.text_input("Character Name (Optional)")
    gender = st.selectbox("Character Gender (Optional)", ["", "Male", "Female", "Non-binary"])
    age = st.slider("Character Age (Optional)", 10, 100, 30)
    description = st.text_area("Character Description (Optional)")

    if st.button("Generate Character Description"):
        if description:
            character_description, is_violation = validate_and_generate_description(name, gender, age, description)
            if is_violation:
                st.warning("Your input contains inappropriate content or violates the policy. Please avoid using explicit words or adult content. A random character description has been generated instead.")
        else:
            character_description = generate_random_character_description()

        st.subheader("Optimized Character Description")
        st.write(character_description)

elif option == 'Generate Random Character':
    if st.button("Generate Random Character Description"):
        with st.spinner("Generating character description..."):
            random_description = generate_random_character_description()
            
            prompt = f"""
            Generate a detailed character description optimized for image generation based on the following details:
            
            {random_description}
            
            Please include specific details on physical features, clothing, and any distinguishing marks to create a vivid visual image.
            """
            
            try:
                # Generate character description using the Gemini-Pro model
                response = model.generate_content([prompt])
                character_description = response.text
            except:
                st.warning("Something went wrong while generating the character description. A random character description has been generated as a fallback.")
                character_description = generate_random_character_description()

        st.subheader("Optimized Character Description for Image Generation")
        st.write(character_description)
