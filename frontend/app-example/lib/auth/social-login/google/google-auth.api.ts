import { AuthApi } from "Api/api-client";
import { createApi } from "Api/builder";
import { getToken } from "Auth/state";
import { GoogleOAuthQuery } from "./google-auth.data";

export const googleAuthErrors = {} as const;
type GoogleAuthError = typeof googleAuthErrors[keyof typeof googleAuthErrors];

const scopesString = process.env.NEXT_PUBLIC_GOOGLE_SCOPES;
const scopes = scopesString ? scopesString.split(",") : [];

type SignUpResponse = {
  access_token?: string;
  error?: GoogleAuthError;
};

const apiFunctions = {
  getGoogleAuthUrl: async (api: AuthApi): Promise<string> => {
    // If the user is logged in, get url for associate, otherwise get url for sign up
    if (getToken()) {
      return apiFunctions._getGoogleAuthUrlForAssociate(api);
    } else {
      return apiFunctions._getGoogleAuthUrlForLogin(api);
    }
  },

  _getGoogleAuthUrlForLogin: async (api: AuthApi): Promise<string> => {
    const response = await api.oauthGoogleJwtAuthorizeAuthGoogleAuthorizeGet({
      scopes,
    });
    return response.authorizationUrl;
  },

  _getGoogleAuthUrlForAssociate: async (api: AuthApi): Promise<string> => {
    const response =
      await api.oauthAssociateGoogleAuthorizeAuthAssociateGoogleAuthorizeGet({
        scopes,
      });
    return response.authorizationUrl;
  },

  sendGoogleOAuthCallback: async (
    api: AuthApi,
    googleOAuthQuery: GoogleOAuthQuery
  ): Promise<SignUpResponse> => {
    if (getToken()) {
      return apiFunctions._sendGoogleOAuthCallbackForAssociate(
        api,
        googleOAuthQuery
      );
    } else {
      return apiFunctions._sendGoogleOAuthCallbackForLogin(
        api,
        googleOAuthQuery
      );
    }
  },

  _sendGoogleOAuthCallbackForAssociate: async (
    api: AuthApi,
    googleOAuthQuery: GoogleOAuthQuery
  ): Promise<SignUpResponse> => {
    await api.oauthAssociateGoogleCallbackAuthAssociateGoogleCallbackGet(
      googleOAuthQuery
    );

    return {
      access_token: getToken(),
    };
  },

  _sendGoogleOAuthCallbackForLogin: async (
    api: AuthApi,
    googleOAuthQuery: GoogleOAuthQuery
  ): Promise<SignUpResponse> => {
    const response = await api.oauthGoogleJwtCallbackAuthGoogleCallbackGet(
      googleOAuthQuery
    );

    return JSON.parse(response) as SignUpResponse;
  },

  getConnectedEmails: async (api: AuthApi): Promise<string[]> => {
    const response = await api.connectedAuthConnectedGoogleConnectedGet();
    return response.connectedEmails;
  },
};

export default function googeAuthApi() {
  return createApi(AuthApi, apiFunctions);
}
