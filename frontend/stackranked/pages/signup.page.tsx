import type { NextPage } from "next";
import { useRouter } from "next/router";
import { ParsedUrlQuery } from "querystring";
import { useEffect } from "react";
import Home from "../lib/home/Home";

type ShowingSignupQuery = {
  signup: string;
};

function isShowingSignup(query: ParsedUrlQuery): query is ShowingSignupQuery {
  return typeof query.signup === "string";
}

const SignupPage: NextPage = () => {
  const { query, push, pathname } = useRouter();
  useEffect(() => {
    if (!isShowingSignup(query)) {
      // Login not yet showing. Need to redirect to add the query param.
      const currentRoute = pathname;
      const loginHref = `${currentRoute}?signup=true`;
      push(loginHref);
    }
  }, [query, push, pathname]);

  return <Home />;
};

export default SignupPage;
