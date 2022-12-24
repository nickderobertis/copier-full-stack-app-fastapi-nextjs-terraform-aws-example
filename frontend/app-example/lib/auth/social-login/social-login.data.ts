import { getToken } from "Auth/state";
import { useEffect, useState } from "react";

export type SocialAuthRequestType = "login" | "associate";

export function useLoginRequestType(): SocialAuthRequestType {
  const [requestType, setRequestType] =
    useState<SocialAuthRequestType>("login");
  useEffect(() => {
    if (getToken()) {
      setRequestType("associate");
    }
  }, []);
  return requestType;
}
