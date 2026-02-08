from fastapi import APIRouter, Depends
import httpx
from cryptography.fernet  import Fernet
from sqlalchemy.orm import Session
from app.deps import get_db
from app.internal.response import success_response
from app.schemas.meroshare import MeroshareCreate,MeroshareRead
from app.internal.encrypt import encrypt_string, decrypt_string
from app.models.meroshare import Meroshare

router = APIRouter(prefix='/meroshare')

@router.get("/test")
def test():
    
    key = Fernet.generate_key()
    return {
        'key': key.decode()
    }

@router.post("/save/account")
def save_meroshare_account(db: Session = Depends(get_db), data: MeroshareCreate = None):
    meroshare = Meroshare(**data.model_dump())
    db.add(meroshare)
    db.commit()
    db.refresh(meroshare)
    
    return success_response(data=None)

@router.get("/", response_model=list[MeroshareRead])
def read_meroshares(db: Session = Depends(get_db)):
    return db.query(Meroshare).filter(
        Meroshare.is_deleted == False
    ).all()


@router.get("/apply")
def apply_share():
    url = ""
    clients = [
        {
            "client_id" : "",
            "client_secret" : "",
            "client_username" : "",
            "crn_number" : "",
            "transaction_pin" : ""
        }
    ]

    for client in clients:
        jwt_token = ""
        response = httpx.post(
            f'{url}/api/meroShare/auth/',
            json={"clientId": client.client_id,"username": client.client_username,"password": client.client_secret}
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
                                        "crnNumber": client.crn_number,
                                        "transactionPIN": client.transaction_pin,
                                        "companyShareId": issue.get('companyShareId'),
                                        "bankId": bank_id
                                    }

                                    response = httpx.post(
                                        f'{url}/api/meroShare/applicantForm/share/apply',
                                        headers={"Authorization": jwt_token},
                                        json=ipo_request
                                    )

                                    if response.status_code == 200 or response.status_code == 202:
                                        print("successfully applied")
                    else:
                        print("already appled or impossible to apply")
            else:
                print("Failed to load")
        else:
            print("Login failed")
                                