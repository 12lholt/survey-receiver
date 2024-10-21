import streamlit as st
import uuid
from datetime import datetime, timezone
import os
from azure.storage.blob import BlobServiceClient
import json

# Use an environment variable for the connection string
connect_str = os.environ.get('AZURE_STORAGE_CONNECTION_STRING')

def save_review(review_data, container_name):
    blob_service_client = BlobServiceClient.from_connection_string(connect_str)
    container_client = blob_service_client.get_container_client(container_name)
    
    blob_name = f"{review_data['review_id']}.json"
    blob_client = container_client.get_blob_client(blob_name)
    
    blob_client.upload_blob(json.dumps(review_data), overwrite=True)

def main():
    st.title("Customer Review Submission")

    # Get business_id, container_name, and location from URL parameters, with default values
    business_id = st.query_params.get("business_id", "MX001")
    container_name = st.query_params.get("container", "bergstrom_test")
    location = st.query_params.get("location", "Unknown")

    st.write(f"Thank you for visiting {business_id}! We'd love to hear your feedback.")

    review_content = st.text_area("Please enter your review:")

    if st.button("Submit Review"):
        if review_content:
            review_data = {
                "review_id": str(uuid.uuid4()),
                "business_id": business_id,
                "review_content": review_content,
                "location": location,
                "date": datetime.now(timezone.utc).isoformat()
            }

            try:
                save_review(review_data, container_name)
                st.success("Thank you for your review! It has been submitted successfully.")
                st.write("Debug info (will be removed in production):")
                st.write(f"Business ID: {business_id}")
                st.write(f"Container Name: {container_name}")
                st.write(f"Location: {location}")
            except Exception as e:
                st.error(f"An error occurred while saving your review. Please try again later. Error: {str(e)}")
        else:
            st.warning("Please enter your review before submitting.")

if __name__ == "__main__":
    main()