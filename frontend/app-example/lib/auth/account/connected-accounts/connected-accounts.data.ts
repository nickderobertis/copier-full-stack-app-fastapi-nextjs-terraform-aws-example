export type OAuthAccountType = "Google";
export type ConnectedAccount = {
  email: string;
};
export type ConnectedAccounts = {
  [key in OAuthAccountType]: ConnectedAccount[];
};
