import { NextPage } from "next";
import BasicAuthPageLayout from "../lib/auth/BasicAuthPageLayout";
import LogoutSuccess from "../lib/auth/logout/LogoutSuccess";

const LogoutSuccessPage: NextPage = () => {
  return (
    <BasicAuthPageLayout>
      <LogoutSuccess />
    </BasicAuthPageLayout>
  );
};

export default LogoutSuccessPage;
