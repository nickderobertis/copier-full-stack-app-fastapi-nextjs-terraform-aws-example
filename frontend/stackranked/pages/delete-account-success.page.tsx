import DeleteAccountSuccess from "Auth/account/DeleteAccountSuccess";
import { NextPage } from "next";
import BasicAuthPageLayout from "../lib/auth/BasicAuthPageLayout";

const DeleteAccountSuccessPage: NextPage = () => {
  return (
    <BasicAuthPageLayout>
      <DeleteAccountSuccess />
    </BasicAuthPageLayout>
  );
};

export default DeleteAccountSuccessPage;
