import AuthCard from "../AuthCard";

type Props = {
  email: string;
};

export default function ForgotPasswordSubmitted({ email }: Props): JSX.Element {
  return (
    <AuthCard>
      <p>Please check {email} for a link to reset your password.</p>
      <div className="mt-3"></div>
      <p className="text-sm">
        If you do not have an account with us, no email will be sent.
      </p>
    </AuthCard>
  );
}
