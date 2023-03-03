import streamlit as st
import requests
import pandas as pd
import xml.etree.ElementTree as ET

# Create a title for the app
st.title("Sitemap Generator")

# Create a file uploader widget for the csv input
input_file = st.file_uploader("Upload a csv file containing URLs in a column called url", type="csv")

# Check if the input file is valid
if input_file:
    # Read the csv file into a dataframe
    df = pd.read_csv(input_file)

    # Create an empty list to store the XML elements
    xml_elements = []

    # Loop through each URL and create an Element object with a loc tag
    for url in df["url"]:
        element = ET.Element("loc")
        element.text = url
        xml_elements.append(element)

    # Split the list into chunks of 50,000 elements
    chunk_size = 50000
    xml_chunks = [xml_elements[i:i+chunk_size] for i in range(0, len(xml_elements), chunk_size)]

    # Create an empty list to store the XML files names and contents 
    xml_files = []

# Loop through each chunk and create an XML tree with a urlset tag 
for i, chunk in enumerate(xml_chunks):
    root = ET.Element("urlset", attrib={"xmlns": "http://www.sitemaps.org/schemas/sitemap/0.9"})
    root.extend(chunk)
    tree = ET.ElementTree(root)

    # Write the XML tree to a string and append it to the list of files names and contents 
    output_file = f"sitemap_{i}.xml"
    output_content = ET.tostring(root, encoding="UTF-8", method="xml")
    xml_files.append((output_file, output_content))

# Display a message when the sitemap files are ready 
st.success("Your sitemap files are ready!")

# Loop through each file name and content and create a download link widget 
for file_name, file_content in xml_files:
    st.download_button(label=f"Download {file_name}", data=file_content, mime="text/xml", file_name=file_name)
