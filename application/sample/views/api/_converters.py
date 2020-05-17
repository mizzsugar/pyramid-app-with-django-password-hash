import sample.domain.dto
import sample.views.api._models as _models


def convert_draft_sign_in(
        source: _models.SignIn
) -> sample.domain.dto.DraftUser:
    return sample.domain.dto.SignIn(
        email=source.email, password=source.password)


def convert_draft_sign_up(
        source: _models.SignUp
) -> sample.domain.dto.DraftUser:
    return sample.domain.dto.DraftUser(
        email=source.email, password=source.password)
