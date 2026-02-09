from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from app.deps import get_db
from app.internal.response import success_response
from app.schemas.meroshare import MeroshareCreate
from app.models.meroshare import Meroshare
from app.core.setting import settings
from app.internal.encrypt import decrypt_string
from app.internal.meroshare import safe_http_request

router = APIRouter(prefix='/meroshare')

@router.post("/save/account") #need to update with authication, (temp for now)
def save_meroshare_account(db: Session = Depends(get_db), data: MeroshareCreate = None):
    meroshare = Meroshare(**data.model_dump())
    db.add(meroshare)
    db.commit()
    db.refresh(meroshare)
    return success_response(data=None)

@router.get("/apply")
def apply_share(db: Session = Depends(get_db), request: Request = None):
    ip = request.client.host

    if(ip != '127.0.0.1'):
        raise Exception('unauthorized ip address')

    url = settings.MEROSHARE_URL
    clients = (
    db.query(Meroshare)
    .filter(Meroshare.is_deleted == False)
    .all())

    for client in clients:
        username = decrypt_string(client.username)
        password = decrypt_string(client.password)
        crn = decrypt_string(client.crn)
        pin = decrypt_string(client.pin)

        jwt_token = ""
        auth_response = safe_http_request(method='post', url=f'{url}/api/meroShare/auth/', json={"clientId": client.client_id,"username": username,"password": password}, auth=True)
       
        if auth_response["success"]:
            jwt_token = auth_response['auth']
        else:
            print(auth_response["message"])
            continue

        ipolist_response = safe_http_request(
                method='POST',
                url=f'{url}/api/meroShare/companyShare/applicableIssue/',
                headers={"Authorization": jwt_token},
                auth=False,
                json={"filterFieldParams":[{"key":"companyIssue.companyISIN.script","alias":"Scrip"},{"key":"companyIssue.companyISIN.company.name","alias":"Company Name"},{"key":"companyIssue.assignedToClient.name","value":"","alias":"Issue Manager"}],"page":1,"size":10,"searchRoleViewConstants":"VIEW_APPLICABLE_SHARE","filterDateParams":[{"key":"minIssueOpenDate","condition":"","alias":"","value":""},{"key":"maxIssueCloseDate","condition":"","alias":"","value":""}]}
            )

        ipolist = []
        if ipolist_response['success']:
            ipolist = ipolist_response.get("object", [])
        else:
            continue

        if ipolist:
            continue
        
        owndetails_response = safe_http_request(
            method='GET',
            url=f'{url}/api/meroShare/ownDetail/',
            headers={"Authorization": jwt_token}
        )

        owndetails = None
        if owndetails_response['success']:
            owndetails = owndetails_response['data']


        bank_response = safe_http_request(
            method='GET',
            url = f'{url}/api/meroShare/bank/',
            headers={"Authorization": jwt_token}
        )

        bank = None
        bank_id = None
        if bank_response['success']:
            bank = bank_response['data']
            bank_id = bank[0].get("id") if bank and isinstance(bank[0], dict) else None
            

        
        bank_details_response =safe_http_request(method = 'GET', url = f'{url}/api/meroShare/bank/{bank_id}', headers={"Authorization": jwt_token})
        bank_details = None
        if bank_details_response['success']:
            bank_details = bank_details_response['data']
           

        for issue in ipolist:
            if issue.get("shareTypeName") == "IPO" and issue.get('action', '') == "" and issue.get('shareGroupName') == "Ordinary Shares" and issue.get('statusName') == 'CREATE_APPROVE':
                
                ipo_details_response = safe_http_request(method='GET',url = f'{url}/api/meroShare/active/{issue.get("companyShareId")}', headers={"Authorization": jwt_token})
                ipo_details = ipo_details_response['data'] if ipo_details_response['success'] else None

                check_response = safe_http_request(method='GET',url = f'{url}/api/meroShare/applicantForm/customerType/{issue.get("companyShareId")}/{owndetails.get("demat")}', headers={"Authorization": jwt_token})
                
                if check_response['success']:
                    if check_response['data'].get("status", {}) == 'ACCEPTED':
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
                                "crnNumber": crn,
                                "transactionPIN": pin,
                                "companyShareId": issue.get('companyShareId'),
                                "bankId": bank_id
                            }

                            response_ipo = safe_http_request(
                                method='POST',
                                url =f'{url}/api/meroShare/applicantForm/share/apply',
                                headers={"Authorization": jwt_token},
                                json=ipo_request
                            )

                            if response_ipo['success']:
                                print('success')
                            else:
                                print('failed')

    return success_response(message='Completed')