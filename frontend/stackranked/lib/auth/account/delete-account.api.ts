import onLogout from "Auth/logout/on-logout";
import googeAuthApi from "Auth/social-login/google/google-auth.api";
import { userApi } from "lib/user/user.api";
import { DeleteApi } from "../../api/api-client";
import { createApi } from "../../api/builder";
import loginApi from "../login/login.api";
import { accountErrors } from "./account.api";
import {
  DeleteAccountWithoutPasswordValidatedData,
  DeleteAccountWithPasswordValidatedData,
} from "./account.data";

export const deleteAccountErrors = {
  ...accountErrors,
  forbidden: "Forbidden",
} as const;

const apiFunctions = {
  deleteUserAccount: async (
    api: DeleteApi,
    data: DeleteAccountWithPasswordValidatedData
  ): Promise<void> => {
    const { email, password } = data;
    if (!password) {
      throw new Error(accountErrors.invalidPassword);
    }
    const verified = await loginApi().verifyLogin({
      email,
      password,
    });
    if (!verified) {
      throw new Error(accountErrors.invalidPassword);
    }
    return api.deleteMeDeleteMeMeDelete().then(onLogout);
  },
  deleteUserAccountOnlyConnectedNoPassword: async (
    api: DeleteApi,
    data: DeleteAccountWithoutPasswordValidatedData
  ): Promise<void> => {
    const { email } = data;
    // Check if email is in connected emails
    const connectedEmails = await googeAuthApi().getConnectedEmails();
    console.log("checking against connected emails", connectedEmails);
    if (!connectedEmails.includes(email)) {
      console.log("email not in connected emails");
      throw new Error(deleteAccountErrors.forbidden);
    }
    // Check if the same email is attached to the user
    const user = await userApi().getMe();
    console.log("checking against user", user);
    if (user.email !== email) {
      console.log("email not in user");
      throw new Error(deleteAccountErrors.forbidden);
    }
    console.log("actually making request");
    return api.deleteMeDeleteMeMeDelete().then(onLogout);
  },
} as const;

export default function deleteMeApi() {
  return createApi(DeleteApi, apiFunctions);
}
