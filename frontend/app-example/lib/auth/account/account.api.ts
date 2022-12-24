import {
  UsersApi,
  UsersPatchCurrentUserUsersMePatchRequest,
} from "../../api/api-client";
import { createApi } from "../../api/builder";
import { filterObjForTruthyValues } from "../../core/data/filter-obj";
import { newPasswordErrors } from "../../core/errors/new-password-errors";
import { updateMe } from "../../user/user.api";
import { UserData } from "../../user/user.data";
import loginApi from "../login/login.api";
import {
  UpdateAccountValidatedData,
  UpdatePasswordValidatedData,
} from "./account.data";

export const accountErrors = {
  invalidPassword: "INVALID_PASSWORD",
} as const;

export const updateAccountErrors = {
  ...accountErrors,
} as const;

export const updatePasswordErrors = {
  ...accountErrors,
  ...newPasswordErrors,
} as const;

const apiFunctions = {
  updateUserAccount: async (
    api: UsersApi,
    data: UpdateAccountValidatedData,
    currentEmail?: string
  ): Promise<UserData> => {
    const { name, email, password } = filterObjForTruthyValues(data);
    if (!password) {
      throw new Error(accountErrors.invalidPassword);
    }
    const verified = await loginApi().verifyLogin({
      email: currentEmail ?? "",
      password,
    });
    if (!verified) {
      throw new Error(accountErrors.invalidPassword);
    }
    const params: UsersPatchCurrentUserUsersMePatchRequest = {
      userUpdate: {
        name,
        email,
        password,
      },
    };
    return api.usersPatchCurrentUserUsersMePatch(params).then(res => {
      updateMe({ name: res.name, email: res.email });
      return res;
    });
  },
  updatePassword: async (
    api: UsersApi,
    formData: UpdatePasswordValidatedData,
    email?: string
  ): Promise<void> => {
    const { oldPassword, newPassword } = formData;
    const verified = await loginApi().verifyLogin({
      email: email ?? "",
      password: oldPassword,
    });
    if (!verified) {
      throw new Error(accountErrors.invalidPassword);
    }
    const params: UsersPatchCurrentUserUsersMePatchRequest = {
      userUpdate: {
        password: newPassword,
      },
    };
    return api.usersPatchCurrentUserUsersMePatch(params).then(() => {});
  },
} as const;

export default function accountApi() {
  return createApi(UsersApi, apiFunctions);
}
