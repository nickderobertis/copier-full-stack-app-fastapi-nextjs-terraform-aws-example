import {
  deleteLocalData,
  getLocalData,
  storeLocalData,
} from "../core/local-storage";
import { USER_TOKEN_KEY } from "./config";

type AuthState = {
  userToken?: string;
};

// Global mutable auth state
const authState: AuthState = {};

export function setToken(token: string) {
  authState.userToken = token;
  storeLocalData(token, USER_TOKEN_KEY);
}

export function getToken(): string | undefined {
  return authState.userToken;
}

export function clearToken() {
  authState.userToken = undefined;
  return deleteLocalData(USER_TOKEN_KEY);
}

export async function restoreToken() {
  const token = await getLocalData<string>(USER_TOKEN_KEY);
  if (token) {
    setToken(token);
  }
}
