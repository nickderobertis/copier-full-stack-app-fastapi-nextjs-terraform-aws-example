import { FrontendErrorCode } from "../../api/error-converter";

// Keys are the error codes, values are the error messages.
type ErrorSchema = Record<string, FrontendErrorCode>;
export type ErrorHandler<K, R = unknown> = (error: Error, key?: K) => R;
type ErrorHandlerSchemaWithoutDefault<
  T extends ErrorSchema,
  Returns = unknown
> = {
  [K in keyof T]: ErrorHandler<K, Returns>;
};
export type ErrorHandlerSchema<
  T extends ErrorSchema,
  Returns = unknown
> = ErrorHandlerSchemaWithoutDefault<T, Returns> & {
  default: (error: any) => Returns;
};

export function createErrorSchemaHandler<
  T extends ErrorSchema,
  Returns = unknown
>(
  errorSchema: T,
  errorHandlerSchema: ErrorHandlerSchema<T, Returns>
): (error: any) => Returns {
  return (error: any) => handleError(error, errorHandlerSchema, errorSchema);
}

function handleError<T extends ErrorSchema, Returns = unknown>(
  error: any,
  handlerSchema: ErrorHandlerSchema<T, Returns>,
  errorSchema: T
): Returns {
  if (error instanceof Error) {
    return _handleError(error, handlerSchema, errorSchema);
  }
  return handlerSchema.default(error);
}

function _handleError<T extends ErrorSchema, Returns = unknown>(
  error: Error,
  handlerSchema: ErrorHandlerSchema<T, Returns>,
  errorSchema: T
): Returns {
  const message = error.message as T[keyof T];
  const key = getKeyByValue(errorSchema, message);
  const handler = handlerSchema[key];
  if (handler) {
    // TODO: Not sure why it is inferring undefined as the type for key here. Ignore for now.
    // @ts-ignore
    return handler(error, message);
  }
  return handlerSchema.default(error);
}

function getKeyByValue<T extends Record<string, unknown>>(
  object: T,
  value: string
): keyof T {
  return Object.keys(object).find(key => object[key] === value) as keyof T;
}
