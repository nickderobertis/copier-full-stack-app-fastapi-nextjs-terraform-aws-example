import Link from "next/link";
import Button from "../core/buttons/Button";

type Props = {
  loginHref: string;
  signUpHref: string;
};

export default function NavBarLoginSignupButtons({
  loginHref,
  signUpHref,
}: Props): JSX.Element {
  return (
    <div className="flex items-center lg:ml-auto">
      <Link href={loginHref} as="/login">
        <button
          type="button"
          className="inline-block px-6 py-2.5 mr-2 bg-transparent text-blue-600 font-medium text-xs leading-tight uppercase rounded hover:text-blue-700 hover:bg-gray-100 focus:bg-gray-100 focus:outline-none focus:ring-0 active:bg-gray-200 transition duration-150 ease-in-out"
          data-mdb-ripple="true"
          data-mdb-ripple-color="light"
        >
          Login
        </button>
      </Link>
      <Link href={signUpHref} as="/signup">
        <a>
          <Button text="Sign up for free" />
        </a>
      </Link>
    </div>
  );
}
