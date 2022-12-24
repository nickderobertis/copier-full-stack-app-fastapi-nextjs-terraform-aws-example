import AuthCard from "../AuthCard";
import AuthLink from "../AuthLink";

export default function LogoutSuccess(): JSX.Element {
  return (
    <AuthCard id="logout-success">
      <p>You have successfully been logged out.</p>
      <div className="mt-3"></div>
      <AuthLink href="/?login=true" as="/login" text="Login" />
    </AuthCard>
  );
}
