import {
  AuthApi,
  RegisterRegisterAuthRegisterPostRequest,
} from "../../api/api-client";
import { createApi } from "../../api/builder";
import { newPasswordErrors } from "../../core/errors/new-password-errors";
import loginApi from "../login/login.api";
import { SignUpValidatedData } from "./signup.data";

export const signUpErrors = {
  emailInUse: "REGISTER_USER_ALREADY_EXISTS",
  ...newPasswordErrors,
} as const;
type SignupError = typeof signUpErrors[keyof typeof signUpErrors];

type SignUpResponse = {
  name?: string;
  email?: string;
  error?: SignupError;
};

const apiFunctions = {
  signUp: async (
    api: AuthApi,
    data: SignUpValidatedData
  ): Promise<SignUpResponse> => {
    const params: RegisterRegisterAuthRegisterPostRequest = {
      userCreate: {
        email: data.email,
        name: data.name,
        password: data.password,
      },
    };

    return api.registerRegisterAuthRegisterPost(params).then(async resp => {
      await loginApi().logIn({
        email: resp.email,
        password: data.password,
      });
      return { email: resp.email, name: resp.name };
    });
  },
};

export default function signUpApi() {
  return createApi(AuthApi, apiFunctions);
}
