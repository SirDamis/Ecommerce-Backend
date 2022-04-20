from django.core.signing import BadSignature, SignatureExpired
from graphql_auth.bases import Output
from graphql_auth.exceptions import (
    UserAlreadyVerified,
    TokenScopeError
)
from graphql_auth.models import UserStatus
from graphql_auth.constants import Messages


from .tasks import send_welcome_email_task



class VerifyAccountMixin(Output):
    """
    Verify user account.
    Receive the token that was sent by email.
    If the token is valid, make the user verified
    by making the `user.status.verified` field true.
    """

    @classmethod
    def resolve_mutation(cls, root, info, **kwargs):
        try:
            token = kwargs.get("token")
            UserStatus.verify(token)
            send_welcome_email_task.delay(token)
            return cls(success=True)
        except UserAlreadyVerified:
            return cls(success=False, errors=Messages.ALREADY_VERIFIED)
        except SignatureExpired:
            return cls(success=False, errors=Messages.EXPIRED_TOKEN)
        except (BadSignature, TokenScopeError):
            return cls(success=False, errors=Messages.INVALID_TOKEN)