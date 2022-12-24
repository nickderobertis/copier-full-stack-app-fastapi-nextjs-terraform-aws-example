import { useRouter } from "next/router";
import { UseFormSetError } from "react-hook-form";
import { createErrorSchemaHandler } from "../../core/errors/known-error-handler";
import TextInput from "../../core/forms/TextInput";
import AuthCard from "../AuthCard";
import AuthForm, { TextInputCreator } from "../AuthForm";
import forgotPasswordApi, {
  resetPasswordErrorSchema,
} from "./forgot-password.api";
import {
  forgotPasswordResetSchema,
  ForgotPasswordResetValidatedData,
} from "./forgot-password.data";

type Props = {
  token?: string;
};

const textInputCreator: TextInputCreator<ForgotPasswordResetValidatedData> = ({
  register,
  errors,
}) => {
  return [
    <TextInput
      {...register("password", { required: true })}
      type="password"
      placeholder="New Password"
      error={errors.password}
      key="password"
    />,
  ];
};

export default function ForgotPasswordReset({ token }: Props): JSX.Element {
  const router = useRouter();

  if (!token) {
    return <AuthCard>No token provided</AuthCard>;
  }

  const onSubmit = (
    data: ForgotPasswordResetValidatedData,
    setError: UseFormSetError<ForgotPasswordResetValidatedData>
  ) => {
    const errorHandler = createErrorSchemaHandler(resetPasswordErrorSchema, {
      passwordTooShort(error) {
        setError("password", {
          message: "Please use a password of at least 8 characters",
          type: "value",
        });
      },
      passwordContainsEmail(error) {
        setError("password", {
          message: "Please use a password that does not contain email",
          type: "value",
        });
      },
      default(error) {
        setError("password", {
          message: "An unexpected error occurred",
          type: "manual",
        });
      },
    });
    return forgotPasswordApi()
      .resetPassword(data, token)
      .then(() => router.push("/reset-password-finish"))
      .catch(errorHandler);
  };

  return (
    <AuthForm
      onSubmit={onSubmit}
      textInputCreator={textInputCreator}
      schema={forgotPasswordResetSchema}
      description="Please enter a new password."
      submitText="Update my Password"
      id="forgot-password-reset"
    />
  );
}
