import Link from "next/link";

type Props = {
  href: string;
  as?: string;
  text: string;
};

export default function AuthLink({ href, text, as }: Props): JSX.Element {
  return (
    <Link href={href} as={as}>
      <div className="pt-4">
        <a className="text-sm text-gray-600 hover:text-gray-900" href="#">
          {text}
        </a>
      </div>
    </Link>
  );
}
