import type { NextPage } from "next";
import { useRouter } from "next/router";
import { ParsedUrlQuery } from "querystring";
import { useEffect } from "react";
import Home from "../lib/home/Home";

type ShowingLoginQuery = {
  login: string;
};

function isShowingLogin(query: ParsedUrlQuery): query is ShowingLoginQuery {
  return typeof query.login === "string";
}

const LoginPage: NextPage = () => {
  const { query, push, pathname } = useRouter();
  useEffect(() => {
    if (!isShowingLogin(query)) {
      // Login not yet showing. Need to redirect to add the query param.
      const currentRoute = pathname;
      const loginHref = `${currentRoute}?login=true`;
      push(loginHref);
    }
  }, [query, push, pathname]);

  return <Home />;
};

export default LoginPage;
