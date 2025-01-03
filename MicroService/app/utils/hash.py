from passlib.context import CryptContext

pwdContext = CryptContext(schemes=["bcrypt"], deprecated="auto")

def getPasswordHash(password):
    return pwdContext.hash(password)

def verifyPassword(plainPassword, hashedPassword):
    return pwdContext.verify(plainPassword, hashedPassword)
