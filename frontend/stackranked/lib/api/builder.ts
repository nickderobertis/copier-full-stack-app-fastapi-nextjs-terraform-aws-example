import { BaseAPI } from "./api-client";
import { getApiConfig } from "./client-config";
import { throwErrorFromApi } from "./error-converter";

type Api = BaseAPI;
type ApiClass = typeof BaseAPI;
type OmitFirstArg<F> = F extends (x: any, ...args: infer P) => infer R
  ? (...args: P) => R
  : never;

type ApiFunction<T extends Api> = (api: T, ...args: any[]) => Promise<unknown>;
type ApiFunctions<T extends Api> = {
  [key: string]: ApiFunction<T>;
};
type ExternalApiFunctions<T> = {
  [key in keyof T]: OmitFirstArg<T[key]>;
};

export function createApi<
  Api extends ApiClass,
  Fns extends ApiFunctions<InstanceType<Api>>
>(api: Api, fns: Fns): ExternalApiFunctions<Fns> {
  const config = getApiConfig();
  const apiInstance = new api(config);
  const result: ExternalApiFunctions<Fns> = {} as any;
  for (const key in fns) {
    const fn = fns[key];
    // First provide the api as the first argument automatically, creating
    // a new function that takes the rest of the arguments.
    // @ts-ignore
    const partialFn = (...args: any) => fn(apiInstance, ...args);
    // Now wrap the function in a try/catch, and catch with the standard error handler
    const caughtFn = (...args: any) =>
      partialFn(...args).catch(throwErrorFromApi);
    // @ts-ignore
    result[key] = caughtFn;
  }
  return result;
}
