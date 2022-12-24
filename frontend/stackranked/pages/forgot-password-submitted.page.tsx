import { NextPage } from "next";
import { useRouter } from "next/router";
import { ParsedUrlQuery } from "querystring";
import BasicAuthPageLayout from "../lib/auth/BasicAuthPageLayout";
import ForgotPasswordSubmitted from "../lib/auth/forgot-password/ForgotPasswordSubmitted";

type ExpectedQuery = {
  email: string;
};

function isValidQuery(query: ParsedUrlQuery): query is ExpectedQuery {
  return typeof query.email === "string";
}

const ForgotPasswordSubmittedPage: NextPage = () => {
  const { query } = useRouter();
  if (!isValidQuery(query)) {
    return <div>Sorry, an error has occurred</div>;
  }

  const { email } = query;

  return (
    <BasicAuthPageLayout>
      <ForgotPasswordSubmitted email={email} />
    </BasicAuthPageLayout>
  );
};

export default ForgotPasswordSubmittedPage;
