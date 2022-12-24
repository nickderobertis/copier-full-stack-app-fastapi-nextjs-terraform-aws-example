type Props = {
  message: string;
};

export function ErrorFormattedMessage({ message }: Props): JSX.Element {
  return <span className="text-red-600">{message}</span>;
}
