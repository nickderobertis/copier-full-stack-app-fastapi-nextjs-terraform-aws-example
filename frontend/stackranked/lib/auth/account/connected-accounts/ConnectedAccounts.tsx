import AuthCard from "Auth/AuthCard";
import SocialLoginButtons from "Auth/social-login/SocialLoginButtons";
import { useMemo } from "react";
import { useConnectedAccounts } from "./connected-accounts.api";
import { OAuthAccountType } from "./connected-accounts.data";
import ConnectedProviderAccounts from "./ConnectedProviderAccounts";

export default function ConnectedAccounts(): JSX.Element {
  const { data, error, isLoading } = useConnectedAccounts();

  const connectedAccountsElems = useMemo(() => {
    if (isLoading) {
      return [];
    }
    if (error) {
      return [];
    }
    if (!data) {
      return [];
    }
    // Iterate over keys of data
    return Object.keys(data).map((providerName, idx) => {
      const accounts = data[providerName as OAuthAccountType];
      return (
        <ConnectedProviderAccounts
          key={idx}
          providerName={providerName}
          accounts={accounts}
        />
      );
    });
  }, [data, error, isLoading]);

  return (
    <AuthCard id="connected-accounts">
      <p>View your connected accounts and connect additional accounts</p>
      {isLoading ? (
        <p>Loading...</p>
      ) : error || !data ? (
        <p>Failed to load connected accounts</p>
      ) : (
        connectedAccountsElems
      )}
      <div className="mt-6"></div>
      <SocialLoginButtons />
    </AuthCard>
  );
}
