import { ResponseError } from "./api-client";

export function isResponseError(error: unknown): error is ResponseError {
  return (
    (error as ResponseError).response !== undefined &&
    (error as ResponseError).response.status !== undefined
  );
}

export function is401Response(error: unknown): boolean {
  return isResponseError(error) && error.response.status === 401;
}
