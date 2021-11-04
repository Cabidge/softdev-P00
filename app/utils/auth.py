from flask import Flask             #facilitate flask webserving
from flask import session           #facilitate user sessions
from os import urandom
from utils.db import initializeUsersTable, addUser, getUserByUsername
from werkzeug.security import generate_password_hash, check_password_hash
from utils.response import Response

class AuthService:

    activeUsers = {}

    def __init__(self):
        initializeUsersTable()

    def currentUser(self):
        if "sessionID" in session:
            sessionID = session.get("sessionID")
            username = self.activeUsers[sessionID]

            userData = getUserByUsername(username)

            if (userData.success):
                return Response(True, userData.payload, "")

        return Response(False, None, "")

    def login(self, username, password):
        userData = getUserByUsername(username)

        if (userData.success):
            if userData.payload and username == userData.payload["username"]:
                if check_password_hash(userData.payload["password"], password):
                    sessionID = urandom(32)
                    session["sessionID"] = sessionID
                    self.activeUsers[sessionID] = username

                    return Response(True, True, "")

        return Response(False, False, "")

    def register(self, username, displayName, password):
        hashedPw = generate_password_hash(password)
        addUser(username, displayName, hashedPw)
        return Response(True, True, "")

    def logout(self):
        if session.get("username"):
            session.pop("username")
        return Response(True, True, "")
