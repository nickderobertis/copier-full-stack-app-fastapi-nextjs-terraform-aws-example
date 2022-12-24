import { AppProps } from "next/app";
import { useEffect } from "react";
import Modal from "react-modal";
import { SWRConfig } from "swr";
import { restoreToken } from "./auth/state";
import { createIgnoreNetworkErrorsHandler } from "./core/errors/global-error-handlers";
import globalSWRConfig from "./core/data/swr-global-config";
import GlobalErrorBoundary from "./core/errors/GlobalErrorBoundary";
import MainLayout from "./core/layout/MainLayout";
import { meKey, updateMe } from "./user/user.api";

Modal.setAppElement("#__next");

export default function App({ Component, pageProps }: AppProps) {
  useEffect(() => {
    async function appAsyncStartup() {
      // Restore the user's auth token from local storage, if it exists
      await restoreToken();

      // Refresh the user's information based on whether the token is set
      await updateMe().catch(createIgnoreNetworkErrorsHandler(meKey));
    }
    appAsyncStartup();
  }, []);
  return (
    <SWRConfig value={globalSWRConfig}>
      <MainLayout>
        <GlobalErrorBoundary>
          <Component {...pageProps} />
        </GlobalErrorBoundary>
      </MainLayout>
    </SWRConfig>
  );
}
