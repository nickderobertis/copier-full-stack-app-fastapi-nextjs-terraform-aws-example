import { UseFormReset, UseFormSetError } from "react-hook-form";
import { createErrorSchemaHandler } from "../../core/errors/known-error-handler";
import TextInput from "../../core/forms/TextInput";
import { useMe } from "../../user/user.api";
import AuthForm, { TextInputCreator } from "../AuthForm";
import accountApi, { updatePasswordErrors } from "./account.api";
import {
  updatePasswordSchema,
  UpdatePasswordValidatedData,
} from "./account.data";

const textInputCreator: TextInputCreator<UpdatePasswordValidatedData> = ({
  register,
  errors,
}) => {
  return [
    <TextInput
      {...register("oldPassword", { required: true })}
      type="password"
      placeholder="Current Password"
      error={errors.oldPassword}
      key="oldPassword"
    />,
    <TextInput
      {...register("newPassword", { required: true })}
      type="password"
      placeholder="New Password"
      error={errors.newPassword}
      key="newPassword"
    />,
  ];
};

export default function UpdatePassword(): JSX.Element {
  const { data } = useMe();
  const { email } = data || {};

  const onSubmit = (
    data: UpdatePasswordValidatedData,
    setError: UseFormSetError<UpdatePasswordValidatedData>,
    reset: UseFormReset<UpdatePasswordValidatedData>
  ) => {
    const errorHandler = createErrorSchemaHandler(updatePasswordErrors, {
      invalidPassword(error) {
        setError("oldPassword", {
          message: "Invalid password",
          type: "custom",
        });
      },
      passwordTooShort(error) {
        setError("newPassword", {
          message: "Please use a password of at least 8 characters",
          type: "value",
        });
      },
      passwordContainsEmail(error) {
        setError("newPassword", {
          message: "Please use a password that does not contain email",
          type: "value",
        });
      },
      default(error) {
        setError("newPassword", {
          message: "An unexpected error occurred",
          type: "custom",
        });
      },
    });
    return accountApi()
      .updatePassword(data, email)
      .then(() => reset())
      .catch(errorHandler);
  };

  return (
    <AuthForm
      onSubmit={onSubmit}
      textInputCreator={textInputCreator}
      schema={updatePasswordSchema}
      description="Update your password by entering your current password and then the new one."
      submitText="Update my Password"
      id="update-password"
    />
  );
}
