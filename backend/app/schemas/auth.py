from __future__ import annotations

from pydantic import BaseModel, ConfigDict, EmailStr


class AuthStartRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    email: EmailStr


class AuthStartResponse(BaseModel):
    status: str


class AuthVerifyRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    token: str


class AuthUser(BaseModel):
    id: str
    email: str
    tier: str


class AuthVerifyResponse(BaseModel):
    session_token: str
    user: AuthUser
