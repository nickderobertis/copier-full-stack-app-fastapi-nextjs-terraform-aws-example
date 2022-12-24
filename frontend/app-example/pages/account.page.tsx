import { NextPage } from "next";
import BasicAuthPageLayout from "Auth/BasicAuthPageLayout";
import UpdateAccountDetails from "Auth/account/UpdateAccountDetails";
import UpdatePassword from "Auth/account/UpdatePassword";
import DeleteAccount from "Auth/account/DeleteAccount";
import ConnectedAccounts from "Auth/account/connected-accounts/ConnectedAccounts";

const AccountPage: NextPage = () => {
  return (
    <BasicAuthPageLayout>
      <UpdateAccountDetails />
      <div className="mt-32"></div>
      <UpdatePassword />
      <DeleteAccount />
      <ConnectedAccounts />
    </BasicAuthPageLayout>
  );
};

export default AccountPage;
