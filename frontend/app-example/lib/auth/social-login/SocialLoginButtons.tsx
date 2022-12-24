import GoogleLoginButton from "./google/GoogleLoginButton";
import { useLoginRequestType } from "./social-login.data";

type Props = {};

export default function SocialLoginButtons({}: Props) {
  const loginRequestType = useLoginRequestType();

  return (
    <div>
      <GoogleLoginButton loginRequestType={loginRequestType} />
    </div>
  );
}
