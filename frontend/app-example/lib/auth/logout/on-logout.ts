import { clearMe } from "../../user/user.api";
import noop from "../../core/no-op";
import { clearToken } from "../state";

export default function onLogout(): Promise<void> {
  return Promise.all([clearToken(), clearMe()]).then(noop);
}
