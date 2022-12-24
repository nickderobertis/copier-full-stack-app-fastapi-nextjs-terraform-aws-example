import { isResponse } from "../data/response";
import {
  withAuthenticatedGlobalSchema,
  withGlobalSchema,
} from "./global-schema";
import {
  createErrorSchemaHandler,
  ErrorHandlerSchema,
} from "./known-error-handler";
import log from "Logging/log";
import onUnauthorized from "../../auth/on-unauthorized";

const apiGlobalErrorSchema = withGlobalSchema({});
const authenticatedGlobalErrorSchema = withAuthenticatedGlobalSchema({});

export function createIgnoreNetworkErrorsHandler(
  path: string,
  authenticated: boolean = true
) {
  const commonErrorHandlers: ErrorHandlerSchema<
    typeof apiGlobalErrorSchema,
    void
  > = {
    networkError(error) {
      log.warn("Network error", error);
    },
    default(error) {
      if (isResponse(error)) {
        return handleErrorResponse(error, path);
      }
      log.error("Uncaught error from API", error);
      throw error;
    },
  };
  if (authenticated) {
    return createErrorSchemaHandler<
      typeof authenticatedGlobalErrorSchema,
      void
    >(authenticatedGlobalErrorSchema, {
      ...commonErrorHandlers,
      unauthorized(error) {
        onUnauthorized("openapi-client", path);
      },
    });
  }
  return createErrorSchemaHandler<typeof apiGlobalErrorSchema, void>(
    apiGlobalErrorSchema,
    commonErrorHandlers
  );
}

async function handleErrorResponse(resp: Response, path: string) {
  if (resp.status === 401) {
    return onUnauthorized("openapi-client", path);
  }
  throw new Error(`${resp.status} ${await resp.body}`);
}
