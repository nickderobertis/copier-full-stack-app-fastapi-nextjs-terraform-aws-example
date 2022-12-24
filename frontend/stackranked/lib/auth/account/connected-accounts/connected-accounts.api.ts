import googeAuthApi from "Auth/social-login/google/google-auth.api";
import { SWRResponseToUseDataResponse, UseDataResponse } from "Data/ext-swr";
import useSWR from "swr";
import { ConnectedAccounts } from "./connected-accounts.data";

const connectedAccountsKey = "connectedAccounts";

const useConnectedAccountsFetcher: () => Promise<ConnectedAccounts> =
  async () => {
    const googleApi = googeAuthApi();
    const googleConnectedEmails = await googleApi.getConnectedEmails();
    const googleConnectedAccounts = googleConnectedEmails.map(email => ({
      email,
    }));
    return {
      Google: googleConnectedAccounts,
    };
  };

export function useConnectedAccounts(): UseDataResponse<ConnectedAccounts> {
  const response = useSWR(connectedAccountsKey, useConnectedAccountsFetcher);
  return SWRResponseToUseDataResponse(response);
}
