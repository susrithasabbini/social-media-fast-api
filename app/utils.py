from passlib.context import CryptContext

pwdContext = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash(password: str):
    return pwdContext.hash(password)


def verify(plainPassword, hashedPassword):
    return pwdContext.verify(plainPassword, hashedPassword)


def formatPostDict(post):
    return {
        "post": {
            "id": post[0].id,
            "title": post[0].title,
            "description": post[0].description,
            "published": post[0].published,
            "ownerId": post[0].ownerId,
            "createdAt": post[0].createdAt.isoformat(),
            "owner": {
                "id": post[0].owner.id,
                "email": post[0].owner.email,
                "createdAt": post[0].owner.createdAt.isoformat(),
            },
        },
        "votes": post[1],
    }
