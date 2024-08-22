import streamlit as st
import cv2
from PIL import Image
import numpy as np
import time

# Custom CSS for a more professional look with a black background
st.markdown("""
    <style>
    body {
        background-color: #000000;
        color: #ffffff;
    }
    .main {
        background-color: #000000;
    }
    .stButton>button {
        background-color: #444444;
        color: white;
        padding: 8px 20px;
        font-size: 16px;
        border-radius: 5px;
        border: none;
    }
    .stButton>button:hover {
        background-color: #555555;
        color: white;
    }
    .stImage {
        border-radius: 10px;
        box-shadow: 0px 4px 8px rgba(255, 255, 255, 0.1);
    }
    .stDownloadButton>button {
        background-color: #28a745;
        color: white;
        padding: 8px 20px;
        font-size: 16px;
        border-radius: 5px;
        border: none;
    }
    .stDownloadButton>button:hover {
        background-color: #218838;
        color: white;
    }
    .stSlider>div>div>div {
        color: #0066cc;
    }
    </style>
""", unsafe_allow_html=True)

# Function to load and resize the image
def load_image(image_path):
    image = Image.open(image_path)
    return image.resize((1080, 720))

# Function to convert image to grayscale
def convert_to_gray(image):
    return cv2.cvtColor(np.array(image), cv2.COLOR_RGB2GRAY)

# Function to blur the image
def blur_image(image, kernel_size):
    return cv2.GaussianBlur(np.array(image), (kernel_size, kernel_size), 0)

# Function to detect edges in the image
def edge_detection(image, low_threshold, high_threshold):
    return cv2.Canny(np.array(image), low_threshold, high_threshold)

# Main function
def main():
    st.title("Image Processing Application")
    st.write("Enhance your images with Grayscale, Blur, and Edge Detection effects. Upload your image and get started!")

    # Image selection
    image_file = st.file_uploader("Upload an Image", type=['jpg', 'jpeg', 'png'])

    if image_file is not None:
        # Load and display the original image
        image = load_image(image_file)

        st.subheader("Original Image")
        st.image(image, caption="Resized Image (1080x720 pixels)", use_column_width=True, output_format="PNG")

        # Create columns for buttons and sliders
        st.markdown("### Apply Effects")
        col1, col2, col3 = st.columns([1, 1, 1])

        with col1:
            st.subheader("Grayscale")
            if st.button("Apply Grayscale"):
                with st.spinner("Processing..."):
                    time.sleep(1)
                    gray_image = convert_to_gray(image)
                    st.image(gray_image, caption="Gray-scaled Image", use_column_width=True)

        with col2:
            st.subheader("Blur")
            kernel_size = st.slider("Select Kernel Size", min_value=3, max_value=15, step=2, value=5, key="blur_slider")
            if st.button("Apply Blur"):
                with st.spinner("Processing..."):
                    time.sleep(1)
                    blurred_image = blur_image(image, kernel_size)
                    st.image(blurred_image, caption="Blurred Image", use_column_width=True)

        with col3:
            st.subheader("Edge Detection")
            low_threshold = st.slider("Low Threshold", min_value=50, max_value=200, value=100, key="edge_low_slider")
            high_threshold = st.slider("High Threshold", min_value=150, max_value=300, value=200, key="edge_high_slider")
            if st.button("Apply Edge Detection"):
                with st.spinner("Processing..."):
                    time.sleep(1)
                    edge_image = edge_detection(image, low_threshold, high_threshold)
                    st.image(edge_image, caption="Edge-detected Image", use_column_width=True)

        # Allow the user to download processed images
        st.markdown("---")
        st.subheader("Download Your Processed Images")
        download_col1, download_col2, download_col3 = st.columns(3)

        with download_col1:
            if "gray_image" in locals():
                st.download_button("Download Gray-scaled Image", data=Image.fromarray(gray_image).tobytes(), file_name="gray_image.png")

        with download_col2:
            if "blurred_image" in locals():
                st.download_button("Download Blurred Image", data=Image.fromarray(blurred_image).tobytes(), file_name="blurred_image.png")

        with download_col3:
            if "edge_image" in locals():
                st.download_button("Download Edge-detected Image", data=Image.fromarray(edge_image).tobytes(), file_name="edge_image.png")

if __name__ == "__main__":
    main()
