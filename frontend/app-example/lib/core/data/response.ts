export function isResponse(response: any): response is Response {
  return response instanceof Response;
}
