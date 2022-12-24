import { SWRResponse } from "swr";

export type UseDataResponse<T> = {
  data?: T;
  error: unknown;
  isLoading: boolean;
};

export function SWRResponseToUseDataResponse<T>(
  response: SWRResponse<T>
): UseDataResponse<T> {
  return {
    data: response.data,
    error: response.error,
    isLoading: !response.data && !response.error,
  };
}
