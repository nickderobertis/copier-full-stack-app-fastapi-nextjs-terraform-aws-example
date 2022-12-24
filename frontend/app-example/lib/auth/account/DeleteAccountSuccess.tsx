import { useRouter } from "next/router";
import { useCallback } from "react";
import Button from "../../core/buttons/Button";
import AuthCard from "../AuthCard";

export default function DeleteAccountSuccess(): JSX.Element {
  const { push } = useRouter();
  const onClick = useCallback(() => push("/?signup=true", "/signup"), [push]);
  return (
    <AuthCard id="delete-account-success">
      <p>Your account has been successfully deleted.</p>
      <div className="mt-3"></div>
      <Button text="Sign Up" onClick={onClick} />
    </AuthCard>
  );
}
