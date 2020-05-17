from __future__ import annotations

import sample.repository
import sample.domain.authentication


class Domain:
    def __init__(
            self,
            repository: sample.repository.Repository,
    ) -> None:
        self.authentication = sample.domain.authentication.Authentication(
            repository=repository)
