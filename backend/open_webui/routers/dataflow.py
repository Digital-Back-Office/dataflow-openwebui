from fastapi import APIRouter, Depends, HTTPException, Request
import requests

router = APIRouter()

@router.get("/user")
def get_dataflow_user(request: Request):
    """
    Fetches the user information from the Dataflow using the session ID from cookies.
    """
    try:
        session_id = request.cookies.get("dataflow_session")
        if not session_id:
            raise HTTPException(status_code=401, detail="Session ID missing in cookies")
        
        cookies = {
            "dataflow_session": session_id,
            "jupyterhub-hub-login": ""
        }
        
        response = requests.get("http://ui-svc.dataflow-studio.svc.cluster.local:8000/hub/ui/api/auth", cookies=cookies, timeout=5)
        
        user_data = response.json()
        if not user_data:
            raise HTTPException(status_code=404, detail="User not found")
        
        user_email = user_data.get('email')
        user_name = user_data.get('user_name')
        
        return {
            "email": user_email,
            "user_name": user_name
        }
        
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")