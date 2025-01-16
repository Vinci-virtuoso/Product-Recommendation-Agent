import streamlit as st
import requests
import json
from PIL import Image
from io import BytesIO
import re

# API endpoint
API_ENDPOINT = "http://localhost:8000/query"

def load_and_display_image(image_url):
    try:
        st.write(f"Attempting to load image from: {image_url}")
        response = requests.get(image_url)
        response.raise_for_status()
        img = Image.open(BytesIO(response.content))
        return img
    except Exception as e:
        st.error(f"Error loading image: {e}")
        return None

def extract_url_from_markdown(text):
    st.write(f"Trying to extract URL from: {text}")
    # First, try markdown link format [text](url)
    url_pattern = r'\[View Product\]\((.*?)\)'
    match = re.search(url_pattern, text)
    if match:
        return match.group(1)
    
    # If no markdown link found, try looking for a URL directly
    url_pattern = r'https?://[^\s<>"]+|www\.[^\s<>"]+|View Product'
    match = re.search(url_pattern, text)
    if match:
        return match.group(0)
    return None

st.title("Product Recommendation Agent")

user_id = st.text_input("Enter User ID")
question = st.text_area("Enter your question about products")

if st.button("Submit"):
    if user_id and question:
        payload = json.dumps({
            "question": question,
            "user_id": user_id
        })
        headers = {
            'Content-Type': 'application/json'
        }
        
        try:
            # Show the API request being made
            st.write("Making API request...")
            response = requests.post(API_ENDPOINT, headers=headers, data=payload)
            response.raise_for_status()
            result = response.json()
            
            # Show the raw API response
            st.write("Raw API Response:")
            st.write(result)
            
            # Parse and display products
            products = result['result'].split('\n')
            st.write(f"Found {len(products)} lines in response")
            
            for line in products:
                st.write(f"Processing line: {line}")
                
                if line.startswith('**'):
                    st.write("Found product name:", line)
                    st.markdown(f"### {line.strip('*').strip()}")
                    
                elif "Price:" in line:
                    st.write("Found price:", line)
                    price = line.split(':')[1].strip()
                    st.write(f"Price: {price}")
                    
                elif "Image:" in line:
                    st.write("Found image line:", line)
                    image_url = extract_url_from_markdown(line)
                    if image_url:
                        st.write(f"Extracted image URL: {image_url}")
                        img = load_and_display_image(image_url)
                        if img:
                            st.image(img, use_container_width=True)
                    else:
                        st.warning(f"Could not extract image URL from: {line}")
                
            st.success("Processing completed!")
            
        except requests.exceptions.RequestException as e:
            st.error(f"Error connecting to the API: {e}")
        except json.JSONDecodeError as e:
            st.error(f"Error decoding API response: {e}")
        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")
            st.write("Full error:", str(e))
    else:
        st.warning("Please enter both User ID and your question.")