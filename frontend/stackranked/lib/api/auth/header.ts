export function authHeader(userToken: string): { Authorization: string } {
  return { Authorization: `Bearer ${userToken}` };
}
