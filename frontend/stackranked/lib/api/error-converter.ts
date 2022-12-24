import { ErrorModel } from "./api-client";

type BackendErrorCode =
  | "REGISTER_USER_ALREADY_EXISTS"
  | "REGISTER_INVALID_PASSWORD"
  | "RESET_PASSWORD_INVALID_PASSWORD"
  | "LOGIN_BAD_CREDENTIALS"
  | "Unauthorized"
  | "Forbidden";

export type FrontendErrorCode =
  | BackendErrorCode
  | "PASSWORD_TOO_SHORT"
  | "PASSWORD_CONTAINS_EMAIL"
  | "INVALID_PASSWORD"
  | "Failed to fetch";

type BackendErrorSchema = {
  code: BackendErrorCode;
  reason: string;
};

type BackendCodeOverride = {
  backendCode: string;
  frontendCode: FrontendErrorCode;
  reason: string;
};

const overrides: BackendCodeOverride[] = [
  {
    backendCode: "[\\w]+_INVALID_PASSWORD",
    reason: "Password should be at least 8 characters",
    frontendCode: "PASSWORD_TOO_SHORT",
  },
  {
    backendCode: "[\\w]+_INVALID_PASSWORD",
    reason: "Password should not contain e-mail",
    frontendCode: "PASSWORD_CONTAINS_EMAIL",
  },
];

function isBackendErrorSchema(obj: any): obj is BackendErrorSchema {
  return obj && obj.code && obj.reason;
}

async function throwErrorFromResponse(resp: Response): Promise<never> {
  const error: ErrorModel = await resp.json();
  const detail = error.detail as BackendErrorSchema | string | undefined;

  if (typeof detail === "string") {
    throw new Error(detail);
  }
  if (!isBackendErrorSchema(detail)) {
    throw new Error(`Unknown error format ${error}`);
  }

  // Find the override for this backend error
  // It should have a code and reason that match the regexes in the
  // backendCode and reason properties of the override
  const override = overrides.find(
    o => detail.code.match(o.backendCode) && detail.reason.match(o.reason)
  );
  if (override) {
    throw new Error(override.frontendCode);
  }

  throw new Error(detail.code);
}

export async function throwErrorFromApi(err: any): Promise<never> {
  if (err instanceof Response) {
    return throwErrorFromResponse(err);
  }
  if (err instanceof Error) {
    throw err;
  }
  throw new Error(`${err}`);
}
