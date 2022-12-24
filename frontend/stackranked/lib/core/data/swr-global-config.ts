import { SWRConfiguration, SWRConfig } from "swr";
import onUnauthorized from "../../auth/on-unauthorized";

const globalSWRConfig: SWRConfiguration = {
  onErrorRetry(error, key, config, revalidate, revalidateOpts) {
    if (error.status === 401) {
      return onUnauthorized("swr", key);
    }

    // Use default behavior if not 401
    return SWRConfig.default.onErrorRetry(
      error,
      key,
      config,
      revalidate,
      revalidateOpts
    );
  },
};

export default globalSWRConfig;
