import { NextPage } from "next";
import { useRouter } from "next/router";
import { ParsedUrlQuery } from "querystring";
import BasicAuthPageLayout from "../lib/auth/BasicAuthPageLayout";
import ForgotPasswordReset from "../lib/auth/forgot-password/ForgotPasswordReset";

type ExpectedQuery = {
  token: string;
};

function isValidQuery(query: ParsedUrlQuery): query is ExpectedQuery {
  return typeof query.token === "string";
}

const ForgotPasswordSubmittedPage: NextPage = () => {
  const { query } = useRouter();
  if (!isValidQuery(query)) {
    return <div>Sorry, an error has occurred</div>;
  }

  const { token } = query;

  return (
    <BasicAuthPageLayout>
      <ForgotPasswordReset token={token} />
    </BasicAuthPageLayout>
  );
};

export default ForgotPasswordSubmittedPage;
