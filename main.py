from fastapi import FastAPI
import httpx
import os
from sqlalchemy.orm import Session
import models, schemas, crud
from database import engine, SessionLocal
import setting
models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/meroshare/apply")
def apply_share():

    client_id = setting.CLIENT_ID
    client_secret = setting.CLIENT_SECRET
    client_username = setting.CLIENT_USERNAME
    crn_number = setting.CRN
    transaction_pin = setting.PIN
    url = setting.BASE_URL_MEROSHARE
    
    jwt_token = ""
    response = httpx.post(
        f'{url}/api/meroShare/auth/',
        json={"clientId":client_id,"username":client_username,"password":client_secret}
    )

    if response.status_code == 200:
        jwt_token = response.headers.get("authorization")

        ipolist_response = httpx.post(
            f'{url}/api/meroShare/companyShare/applicableIssue/',
            headers={"Authorization": jwt_token},
            json={"filterFieldParams":[{"key":"companyIssue.companyISIN.script","alias":"Scrip"},{"key":"companyIssue.companyISIN.company.name","alias":"Company Name"},{"key":"companyIssue.assignedToClient.name","value":"","alias":"Issue Manager"}],"page":1,"size":10,"searchRoleViewConstants":"VIEW_APPLICABLE_SHARE","filterDateParams":[{"key":"minIssueOpenDate","condition":"","alias":"","value":""},{"key":"maxIssueCloseDate","condition":"","alias":"","value":""}]}
        )

        owndetails_response = httpx.get(
            f'{url}/api/meroShare/ownDetail/',
            headers={"Authorization": jwt_token}
        )
        owndetails = owndetails_response.json()

        bank_response = httpx.get(
            f'{url}/api/meroShare/bank/',
            headers={"Authorization": jwt_token}
        )

        bank = bank_response.json()
        bank_id = bank[0].get("id") if bank and isinstance(bank[0], dict) else None

        bank_details_response = httpx.get(f'{url}/api/meroShare/bank/{bank_id}', headers={"Authorization": jwt_token})
        bank_details = bank_details_response.json()

        if ipolist_response.status_code == 200:
            ipolist = ipolist_response.json()
            for issue in ipolist.get("object", []):
                if issue.get("shareTypeName") == "IPO" and issue.get('action', '') == "" and issue.get('shareGroupName') == "Ordinary Shares" and issue.get('statusName') == 'CREATE_APPROVE':
                    ipo_details_response = httpx.get(f'{url}/api/meroShare/active/{issue.get("companyShareId")}', headers={"Authorization": jwt_token})
                    ipo_details = ipo_details_response.json()
                    check_response = httpx.get(f'{url}/api/meroShare/applicantForm/customerType/{issue.get("companyShareId")}/{owndetails.get("demat")}', headers={"Authorization": jwt_token})
                    if check_response.status_code == 200 or check_response.status_code == 202:
                        if check_response.json().get("status", {}) == 'ACCEPTED':
                            print("Customer is eligible to apply for this IPO")

                            if float(ipo_details.get('sharePerUnit')) < 200 or float(ipo_details.get('sharePerUnit')) > 90:
                                ipo_request = {
                                    "demat": owndetails.get('demat'),
                                    "boid": owndetails.get('boid'),
                                    "accountNumber": bank_details[0].get('accountNumber') if bank_details and isinstance(bank_details[0], dict) else None,
                                    "customerId": bank_details[0].get('id') if bank_details and isinstance(bank_details[0], dict) else None ,
                                    "accountBranchId": bank_details[0].get("accountBranchId") if bank_details and isinstance(bank_details[0], dict) else None,
                                    "accountTypeId": bank_details[0].get("accountTypeId") if bank_details and isinstance(bank_details[0], dict) else None,
                                    "appliedKitta":"10",
                                    "crnNumber": crn_number,
                                    "transactionPIN": transaction_pin,
                                    "companyShareId": issue.get('companyShareId'),
                                    "bankId": bank_id
                                }

                                response = httpx.post(
                                    f'{url}/api/meroShare/applicantForm/share/apply',
                                    headers={"Authorization": jwt_token},
                                    json=ipo_request
                                )

                                if response.status_code == 200 or response.status_code == 202:
                                    return {"message": "Successfully applied for 10 kitta IPO shares"}
                                