import { NextPage } from "next";
import ForgotPasswordBegin from "../lib/auth/forgot-password/ForgotPasswordBegin";
import BasicAuthPageLayout from "../lib/auth/BasicAuthPageLayout";

const ForgotPassword: NextPage = () => {
  return (
    <BasicAuthPageLayout>
      <ForgotPasswordBegin />
    </BasicAuthPageLayout>
  );
};

export default ForgotPassword;
