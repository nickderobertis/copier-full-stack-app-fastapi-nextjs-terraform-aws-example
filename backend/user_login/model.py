import datetime
import os
from enum import Enum
from typing import TYPE_CHECKING, Final, Iterator

import dateutil.parser
import pandas as pd
from okta.models import LogActor, LogEvent, LogTarget
from tests.unit.user_login.exc import InvalidUserLoginStructureException

if TYPE_CHECKING:
    from googleapiclient._apis.admin.reports_v1.schemas import Activity

from pydantic import BaseModel

GOOGLE_LOGIN_ID: Final[str] = "Google Login"
GOOGLE_LOGIN_NAME: Final[str] = "Google Login"


class EventSource(str, Enum):
    GOOGLE = "Google"
    OKTA = "Okta"


class UserLoginEvent(BaseModel):
    time: datetime.datetime
    user_id: str
    user_email: str
    target_name: str
    target_id: str
    source: EventSource

    @classmethod
    def from_google_activity(
        cls, activity: "Activity", target_name: str, target_id: str
    ) -> "UserLoginEvent":
        # TODO: when will there be multiple events for single activity? What will those contain?
        if len(activity["events"]) > 1:
            raise NotImplementedError("Multiple events not yet supported")

        time_str = activity["id"]["time"]
        actor = activity["actor"]
        return cls(
            time=dateutil.parser.isoparse(time_str),
            user_id=actor["profileId"],
            user_email=actor["email"],
            target_name=target_name,
            target_id=target_id,
            source=EventSource.GOOGLE,
        )

    @classmethod
    def from_google_login_activity(cls, activity: "Activity") -> "UserLoginEvent":
        return cls.from_google_activity(activity, GOOGLE_LOGIN_ID, GOOGLE_LOGIN_NAME)

    @classmethod
    def from_google_token_activity(cls, activity: "Activity") -> "UserLoginEvent":
        if len(activity["events"]) != 1:
            raise NotImplementedError("Must have a single event")
        event = activity["events"][0]
        target_name: str | None = None
        target_id: str | None = None
        for parameter in event["parameters"]:
            if parameter["name"] == "app_name":
                target_name = parameter["value"]
            elif parameter["name"] == "client_id":
                target_id = parameter["value"]
        if target_name is None or target_id is None:
            raise InvalidUserLoginStructureException(
                f"Did not find both client_id and app_name in event parameters: {event['parameters']}"
            )
        return cls.from_google_activity(activity, target_name, target_id)

    @classmethod
    def from_okta_log_event(cls, log_event: LogEvent) -> "UserLoginEvent":
        actor: LogActor = log_event.actor
        selected_targets: list[LogTarget] = []
        for target in log_event.target:
            if target.type == "AppInstance":
                selected_targets.append(target)
        # TODO: Will there ever be multiple app instances in a single event?
        if len(selected_targets) > 1:
            raise NotImplementedError("Multiple targets not yet supported")
        target = selected_targets[0]
        return cls(
            time=log_event.published,
            user_id=actor.id,
            user_email=actor.alternate_id,
            target_id=target.id,
            # TODO: we have both display_name and alternate_id that seem to have similar values. Should we use alternate_id somehow?
            target_name=target.display_name,
            source=EventSource.OKTA,
        )


class UserLoginEvents(BaseModel):
    events: list[UserLoginEvent]

    @classmethod
    def from_google_login_activities(cls, activities: list["Activity"]):
        # TODO: filter activity based on whether they are login events
        return cls(
            events=[UserLoginEvent.from_google_login_activity(a) for a in activities]
        )

    @classmethod
    def from_google_token_activities(cls, activities: list["Activity"]):
        # TODO: filter activity based on whether they are login events
        return cls(
            events=[UserLoginEvent.from_google_token_activity(a) for a in activities]
        )

    @classmethod
    def from_okta_log_events(cls, log_events: list[LogEvent]):
        # TODO: filter log_events based on whether they are login events
        return cls(events=[UserLoginEvent.from_okta_log_event(e) for e in log_events])

    def __getitem__(self, item) -> "UserLoginEvent":
        return self.events[item]

    def __iter__(self) -> Iterator["UserLoginEvent"]:
        return iter(self.events)

    def __len__(self) -> int:
        return len(self.events)

    def __contains__(self, item) -> bool:
        return item in self.events

    def to_df(self) -> pd.DataFrame:
        return pd.DataFrame([event.__dict__ for event in self])

    def to_csv(self, path: os.PathLike) -> None:
        self.to_df().to_csv(path)

    def to_parquet(self, path: os.PathLike) -> None:
        self.to_df().to_parquet(path)

    def merge(self, other: "UserLoginEvents") -> "UserLoginEvents":
        return UserLoginEvents(events=self.events + other.events)
