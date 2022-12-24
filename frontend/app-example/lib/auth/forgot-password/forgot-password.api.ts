import { AuthApi } from "../../api/api-client";
import { createApi } from "../../api/builder";
import { newPasswordErrors } from "../../core/errors/new-password-errors";
import noop from "../../core/no-op";
import {
  ForgotPasswordBeginValidatedData,
  ForgotPasswordResetValidatedData,
} from "./forgot-password.data";

export const resetPasswordErrorSchema = {
  ...newPasswordErrors,
} as const;

const apiFunctions = {
  forgotPasswordBegin: async (
    api: AuthApi,
    data: ForgotPasswordBeginValidatedData
  ): Promise<void> => {
    const { email } = data;
    return api
      .resetForgotPasswordAuthForgotPasswordPost({
        bodyResetForgotPasswordAuthForgotPasswordPost: { email },
      })
      .then(noop);
  },
  resetPassword: async (
    api: AuthApi,
    data: ForgotPasswordResetValidatedData,
    token: string
  ): Promise<void> => {
    const { password } = data;
    return api
      .resetResetPasswordAuthResetPasswordPost({
        bodyResetResetPasswordAuthResetPasswordPost: { password, token },
      })
      .then(noop);
  },
} as const;

export default function forgotPasswordApi() {
  return createApi(AuthApi, apiFunctions);
}
