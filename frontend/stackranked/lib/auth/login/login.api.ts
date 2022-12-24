import {
  AuthApi,
  AuthJwtLoginAuthJwtLoginPostRequest,
} from "../../api/api-client";
import { ErrorModel } from "../../api/api-client/models/ErrorModel";
import { setToken } from "../state";
import { createApi } from "../../api/builder";
import { updateMe } from "../../user/user.api";
import { LoginValidatedData } from "./login.data";

export const loginErrorSchema = {
  invalidCredentials: "LOGIN_BAD_CREDENTIALS",
} as const;

type LoginResponse = {
  token: string;
};

export function logInFromToken(token: string) {
  setToken(token);
  updateMe();
}

const apiFunctions = {
  logIn: async (
    api: AuthApi,
    data: LoginValidatedData
  ): Promise<LoginResponse> => {
    const params: AuthJwtLoginAuthJwtLoginPostRequest = {
      username: data.email,
      password: data.password,
    };

    return api.authJwtLoginAuthJwtLoginPost(params).then(resp => {
      logInFromToken(resp.accessToken);
      return { token: resp.accessToken };
    });
  },
  verifyLogin: async (
    api: AuthApi,
    data: LoginValidatedData
  ): Promise<boolean> => {
    const params: AuthJwtLoginAuthJwtLoginPostRequest = {
      username: data.email,
      password: data.password,
    };

    return api
      .authJwtLoginAuthJwtLoginPost(params)
      .then(resp => {
        if (resp.accessToken) {
          return true;
        }
        return false;
      })
      .catch(async (resp: Response) => {
        return false;
      });
  },
} as const;

export default function loginApi() {
  return createApi(AuthApi, apiFunctions);
}
