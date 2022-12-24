import { NextPage } from "next";
import BasicAuthPageLayout from "../lib/auth/BasicAuthPageLayout";
import ForgotPasswordSuccess from "../lib/auth/forgot-password/ForgotPasswordSuccess";

const ResetPasswordFinish: NextPage = () => {
  return (
    <BasicAuthPageLayout>
      <ForgotPasswordSuccess />
    </BasicAuthPageLayout>
  );
};

export default ResetPasswordFinish;
