import logging

from fastapi import APIRouter, Request, Depends, Form
from fastapi.responses import RedirectResponse

from app.core.router_factory import create_crud_router
from app.core.services_factory import get_quest_applications_service
from app.core.auth import build_user_dependency

from app.core.helpers import safe_next_url

logger = logging.getLogger(__name__)

router = create_crud_router(
    get_quest_applications_service(),
    "/quest-applications",
    True,
    True
)

get_user_for_write = build_user_dependency(True)

quest_applications_router = APIRouter()

@quest_applications_router.post("/quest-applications/{application_id}/approve")
async def approve_application(
    request: Request,
    application_id: int,
    back: str | None = Form(None),
    user_id = Depends(get_user_for_write)
):
    logger.debug("Approving application %s", application_id)

    quest_id, error = get_quest_applications_service().approve(
        application_id=application_id
    )

    redirect_url = safe_next_url(back)

    if error:
        logger.warning("Approve failed for application_id=%s: %s", application_id, error)
        request.session["flash"] = "Application cannot be approved"
        return RedirectResponse(
            url = redirect_url,
            status_code = 303
        )

    request.session["flash"] = "Application succesfully approved"
    return RedirectResponse(
        url = redirect_url,
        status_code = 303
    )


@quest_applications_router.post("/quest-applications/{application_id}/reject")
async def reject_application(
    request: Request,
    application_id: int,
    back: str | None = Form(None),
    user_id = Depends(get_user_for_write)
):
    logger.debug("Rejecting application %s", application_id)

    quest_id, error = get_quest_applications_service().reject(
        application_id=application_id
    )

    redirect_url = safe_next_url(back)

    if error:
        logger.warning("Reject failed for application_id=%s: %s", application_id, error)
        request.session["flash"] = "Application cannot be rejected"
        return RedirectResponse(
            url = redirect_url,
            status_code = 303
        )

    request.session["flash"] = "Application succesfully rejected"
    return RedirectResponse(
        url = redirect_url,
        status_code = 303
    )