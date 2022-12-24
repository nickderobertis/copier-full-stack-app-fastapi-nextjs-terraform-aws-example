import { Configuration, ConfigurationParameters } from "./api-client";
import { authHeader } from "./auth/header";
import { getToken } from "../auth/state";

const configParams: ConfigurationParameters = {
  basePath: process.env.NEXT_PUBLIC_API_URL,
  middleware: [
    {
      async pre(context) {
        const { url, init } = context;
        return { url, init };
      },
      async post(context) {
        return context.response;
      },
    },
  ],
};

export function getApiConfig(): Configuration {
  const token = getToken();
  const config: ConfigurationParameters = {
    ...configParams,
  };
  if (token) {
    config.headers = {
      ...authHeader(token),
    };
  }
  return new Configuration(config);
}
