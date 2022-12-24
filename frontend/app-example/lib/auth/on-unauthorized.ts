import log from "../core/logging/log";
import onLogout from "./logout/on-logout";

type ApiSource = "openapi-client" | "swr";

export default function onUnauthorized(
  source: ApiSource,
  path: string
): Promise<void> {
  log.warn(`Unauthorized from ${source} ${path}`);
  return onLogout();
}
