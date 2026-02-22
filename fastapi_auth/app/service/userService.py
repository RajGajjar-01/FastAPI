from app.db.repository.user import UserRepository
from app.db.schemas.user import UserInCreate, UserInLogin, UserOutput, UserWithToken
from app.core.security.authHandler import AuthHandler
from app.core.security.hashHelper import HashHelper
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session

class UserService:
    def __init__(self, session: Session):
        self.__userRepository = UserRepository(session=session)

    def signup(self, user_details: UserInCreate) -> UserOutput:
        if self.__userRepository.user_exist_by_email(email=user_details.email):
            raise HTTPException(status_code=400, detail="please login")
        
        hashed_password = HashHelper.get_password_hash(plain_password=user_details.password)
        user_details.password = hashed_password
        return self.__userRepository.create_user(user_data=user_details)
    
    def login(self, user_details: UserInLogin) -> UserWithToken:
        if not self.__userRepository.user_exist_by_email(email=user_details.email):
            raise HTTPException(status_code=400, detail="please signup")
        
        user = self.__userRepository.get_user_by_email(email=user_details.email)
        if HashHelper.verify_password(plain_password=user_details.password, hashed_password=user.password):
            token = AuthHandler.sign_jwt(user_id=user.id)
            if token:
                return UserWithToken(token=token)
            raise HTTPException(status_code=500, detail="Unable to process request")
        
        raise HTTPException(status_code=400, detail="please check your credentials")
    
    def get_user_by_id(self, user_id: int):
        user = self.__userRepository.get_user_by_id(user_id=user_id)
        if user:
            return user
        raise HTTPException(status_code=400, detail="User is not available")