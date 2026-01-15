from pegasus_framework.wiring.bootstrap import get_user_service
from pegasus_framework.business.users.user_service import UserService


def get_user_service_override() -> UserService:
    print(">>> USING OVERRIDE <<<")
    service = get_user_service()

    # punto único de extensión futura, aca meter :
    # - logging
    # - métricas
    # - feature flags
    # - decorators
    # - validaciones adicionales

    return service