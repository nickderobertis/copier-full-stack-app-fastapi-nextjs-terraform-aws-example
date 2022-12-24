import { AuthApi } from "../../api/api-client";
import onLogout from "./on-logout";
import { createApi } from "../../api/builder";

const apiFunctions = {
  logOut: async (api: AuthApi): Promise<void> => {
    return api.authJwtLogoutAuthJwtLogoutPost().finally(onLogout);
  },
} as const;

export default function logoutApi() {
  return createApi(AuthApi, apiFunctions);
}
