import { PropsWithChildren } from "react";

type Props = PropsWithChildren<{ id?: string }>;

export default function AuthCard(props: Props): JSX.Element {
  return (
    <div
      className="block rounded-lg shadow-lg bg-white px-6 py-12 md:px-12"
      id={props.id}
    >
      {props.children}
    </div>
  );
}
