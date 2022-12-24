import { ConnectedAccount } from "./connected-accounts.data";

type Props = {
  providerName: string;
  accounts: ConnectedAccount[];
};

export default function ConnectedProviderAccounts({
  providerName,
  accounts,
}: Props): JSX.Element {
  return (
    <div className="mt-3">
      <h3>{providerName}</h3>
      <ul>
        {accounts.map((account, idx) => (
          <li key={idx}>{account.email}</li>
        ))}
      </ul>
    </div>
  );
}
