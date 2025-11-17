from fastapi import FastAPI
from auth.auth_router import router as auth_router
from routers.user_router import router as user_router
from routers.admin_router import router as admin_router
from fastapi.security import OAuth2PasswordBearer

app = FastAPI(title="Auth System WIth RBAC")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
app.include_router(auth_router)
app.include_router(user_router)
app.include_router(admin_router)
