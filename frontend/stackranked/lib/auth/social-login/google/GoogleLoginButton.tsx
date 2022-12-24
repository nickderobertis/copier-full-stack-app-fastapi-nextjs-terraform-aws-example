import { useEffect, useMemo, useState } from "react";
import { GoogleLoginButton } from "react-social-login-buttons";
import { SocialAuthRequestType } from "../social-login.data";
import googleAuthApi from "./google-auth.api";

type Props = {
  loginRequestType: SocialAuthRequestType;
};

export default function GoogleButton({ loginRequestType }: Props) {
  const [url, setUrl] = useState<string | null>(null);
  useEffect(() => {
    async function getGoogleUrlFromBackend() {
      const url = await googleAuthApi().getGoogleAuthUrl();
      setUrl(url);
    }

    getGoogleUrlFromBackend();
  }, []);

  const text = useMemo(() => {
    switch (loginRequestType) {
      case "login":
        return "Log in with Google";
      case "associate":
        return "Connect Google";
    }
  }, [loginRequestType]);

  if (!url) {
    return null;
  }

  return (
    <div>
      <GoogleLoginButton
        onClick={() => {
          window.location.href = url;
        }}
        style={{
          display: "flex",
          fontSize: "1rem",
          borderRadius: "8px",
          height: "35px",
          width: "100%",
          margin: undefined,
        }}
        text={text}
        className="justify-center"
      />
    </div>
  );
}
