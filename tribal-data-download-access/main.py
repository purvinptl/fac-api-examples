import os
import requests
import json

FAC_API_KEY = os.getenv("API_GOV_KEY")
ACCESS_TOKEN = os.getenv("BEARER_TOKEN")
API_KEY = os.getenv("API_KEY_ID")
FAC_API_BASE = os.getenv("FAC_API_URL")
FAC_PDF_BASE = os.getenv("FAC_PDF_DOWNLOAD")

# Step 1: Fetch Data About a Submission
def fetch_submission_data(report_id):
    url = f'{FAC_API_BASE}/general?report_id=eq.{report_id}'
    headers = {
        'Authorization': f'Bearer {ACCESS_TOKEN}'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        submission_data = response.json()
        return submission_data

    
# Step 2: Request File Access
def request_file_access(report_id):
    url = f'{FAC_API_BASE}/rpc/request_file_access'
    headers = {
        'content-Profile': 'admin_api_v1_1_0',
        'x-api-user-id': f'{API_KEY}',
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {ACCESS_TOKEN}'
    }
    payload = json.dumps({
        "report_id": f'{report_id}'
        })
    
    response = requests.request("POST", url, headers=headers, data=payload)
    
    if response.status_code == 200:
        access_info = response.json()
        return access_info
    
# Step 3: Download the File
def download_file(access_info):
    access_uuid_value = access_info.get('access_uuid')
    url = f'{FAC_PDF_BASE}/dissemination/report/pdf/ota/{access_uuid_value}'
    payload = {}
    headers = {
        'X-Api-Key': f'{FAC_API_KEY}'
    }
    try:
        response = requests.get(url, headers=headers, data=payload)
        if response.status_code == 200:
            with open("downloaded_file.pdf", "wb") as pdf_file:
                pdf_file.write(response.content)
            print("File downloaded successfully.")
        else:
            print("Failed to download file. Status code:", response.status_code)
            print("Response content:", response.text)
    except Exception as e:
        print("Error occurred while downloading file:", e)

# Example usage:

if __name__ == "__main__":

    print("-" * 100)
    report_id = "2022-06-TSTDAT-0000182926"
    file_uuid = request_file_access(report_id)
    submission_data = fetch_submission_data(report_id)
    if submission_data:
        print("Submission Data:")
        print(submission_data)
    else:
        print("Failed to fetch submission data.")

    print("-" * 100)

    access_info = request_file_access(report_id)
    
    # Check if file access is successful.
    if access_info:
        print("Access Info:")
        print(access_info)
    else:
        print("Failed to request file access.")
    print("-" * 100)

    download_file(access_info)