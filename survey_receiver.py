import streamlit as st
import uuid
from datetime import datetime, timezone
import os
from azure.storage.blob import BlobServiceClient
import json

# Instead, use an environment variable
connect_str = os.environ.get('AZURE_STORAGE_CONNECTION_STRING')

def save_review(review_data, container_name):
    blob_service_client = BlobServiceClient.from_connection_string(connect_str)
    container_client = blob_service_client.get_container_client(container_name)
    
    blob_name = f"{review_data['review_id']}.json"
    blob_client = container_client.get_blob_client(blob_name)
    
    blob_client.upload_blob(json.dumps(review_data), overwrite=True)

def main():
    st.title("Customer Review Submission")

    # Get business_id and container_name from URL parameters
    params = st.experimental_get_query_params()
    business_id = params.get("business_id", [""])[0]
    container_name = params.get("container", [""])[0]

    if not business_id or not container_name:
        st.error("Missing business ID or container name. Please scan a valid QR code.")
        return

    st.write(f"Thank you for visiting {business_id}! We'd love to hear your feedback.")

    review_content = st.text_area("Please enter your review:")
    location = st.text_input("Location:")

    if st.button("Submit Review"):
        if review_content and location:
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
            except Exception as e:
                st.error(f"An error occurred while saving your review. Please try again later. Error: {str(e)}")
        else:
            st.warning("Please fill in both the review and location fields.")

if __name__ == "__main__":
    main()
