import { ResponseError, UserRead, UsersApi } from "../api/api-client";
import { createApi } from "../api/builder";
import useSWR, { mutate } from "swr";
import {
  SWRResponseToUseDataResponse,
  UseDataResponse,
} from "../core/data/ext-swr";
import { getToken } from "../auth/state";
import { createErrorSchemaHandler } from "Errors/known-error-handler";
import onLogout from "Auth/logout/on-logout";
import { is401Response } from "Api/error-response";
import log from "Logging/log";

export const meKey = "me";

const userErrorSchema = {
  unauthorized: "Unauthorized",
} as const;

const apiFunctions = {
  getMe: async (api: UsersApi): Promise<UserRead> => {
    try {
      return await api.usersCurrentUserUsersMeGet();
    } catch (e: unknown) {
      if (is401Response(e)) {
        throw new Error(userErrorSchema.unauthorized);
      }
      throw e;
    }
  },
} as const;

export function userApi() {
  return createApi(UsersApi, apiFunctions);
}

const userErrorHandler = createErrorSchemaHandler(userErrorSchema, {
  unauthorized(error) {
    onLogout();
  },
  default(error) {
    log.exception(error);
  },
});

const useMeFetcher: () => Promise<Partial<UserRead>> = () => {
  // useMe is used on pages where the user may not be logged in, so avoid
  // requesting it if there is no token
  if (!getToken()) {
    return Promise.resolve({});
  }
  const api = userApi();
  return api.getMe().catch((error: unknown) => {
    userErrorHandler(error);
    return {};
  });
};

export function updateMe(data?: Partial<UserRead>) {
  const updater = data ? data : useMeFetcher;
  return mutate(meKey, updater);
}

export function clearMe() {
  return mutate(meKey, { name: undefined, email: undefined });
}

export function useMe(): UseDataResponse<Partial<UserRead>> {
  const response = useSWR(meKey, useMeFetcher);
  return SWRResponseToUseDataResponse(response);
}
