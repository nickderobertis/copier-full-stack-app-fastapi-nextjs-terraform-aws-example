const globalErrorSchema = {
  networkError: "Failed to fetch",
} as const;

export function withGlobalSchema<T>(schema: T): T & typeof globalErrorSchema {
  return { ...schema, ...globalErrorSchema };
}

const authenticatedGlobalErrorSchema = {
  unauthorized: "Unauthorized",
  ...globalErrorSchema,
} as const;

export function withAuthenticatedGlobalSchema<T>(
  schema: T
): T & typeof authenticatedGlobalErrorSchema {
  return { ...schema, ...authenticatedGlobalErrorSchema };
}
