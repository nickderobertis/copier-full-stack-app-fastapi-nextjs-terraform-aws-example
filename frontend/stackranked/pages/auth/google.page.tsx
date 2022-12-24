import { logInFromToken } from "Auth/login/login.api";
import googleAuthApi from "Auth/social-login/google/google-auth.api";
import { GoogleOAuthQuery } from "Auth/social-login/google/google-auth.data";
import Home from "lib/home/Home";
import log from "Logging/log";
import type { NextPage } from "next";
import { useRouter } from "next/router";
import { ParsedUrlQuery } from "querystring";
import { useEffect } from "react";

function isGoogleOAuthQuery(query: ParsedUrlQuery): query is GoogleOAuthQuery {
  return typeof query.code === "string" && typeof query.state === "string";
}

const GoogleAuthPage: NextPage = () => {
  const { query, push, pathname } = useRouter();
  useEffect(() => {
    if (!isGoogleOAuthQuery(query)) {
      // Invalid Google OAuth query. Don't log the user in.
      log.error("Invalid Google OAuth query", query);
      return;
    }
    async function loginWithGoogle(loginParams: GoogleOAuthQuery) {
      const response = await googleAuthApi().sendGoogleOAuthCallback(
        loginParams
      );
      if (response.access_token) {
        logInFromToken(response.access_token);
        push("/");
      }
    }
    loginWithGoogle(query);
  }, [query, push, pathname]);

  return <Home />;
};

export default GoogleAuthPage;
