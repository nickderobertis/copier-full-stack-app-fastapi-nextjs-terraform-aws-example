import datetime
from typing import Optional

from ext_sentry.models.generated.list_event import SentryListEventResponseItem
from pydantic import BaseModel

DATE_FORMAT = "%Y-%m-%dT%H:%M:%S%z"


class SentryEvent(BaseModel):
    created: datetime.datetime
    message: Optional[str] = None
    title: Optional[str] = None

    @classmethod
    def from_response_list_item(cls, item: SentryListEventResponseItem):
        return cls(
            created=datetime.datetime.strptime(item.dateCreated, DATE_FORMAT),
            message=item.message,
            title=item.title,
        )
