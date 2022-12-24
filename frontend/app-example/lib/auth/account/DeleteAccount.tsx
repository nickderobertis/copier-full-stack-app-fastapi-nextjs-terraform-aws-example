import { ErrorFormattedMessage } from "Core/forms/ErrorFormattedMessage";
import { useMe } from "lib/user/user.api";
import { useRouter } from "next/router";
import { useCallback, useMemo } from "react";
import { UseFormSetError } from "react-hook-form";
import { createErrorSchemaHandler } from "../../core/errors/known-error-handler";
import TextInput from "../../core/forms/TextInput";
import AuthForm, { TextInputCreator } from "../AuthForm";
import {
  deleteAccountWithoutPasswordSchema,
  deleteAccountWithPasswordSchema,
  DeleteAccountWithPasswordValidatedData,
} from "./account.data";
import deleteMeApi, { deleteAccountErrors } from "./delete-account.api";

export default function DeleteAccount(): JSX.Element {
  const router = useRouter();
  const { data: userData } = useMe();
  console.log("user data", userData);
  const hasRealPassword = userData?.hasRealPassword ?? true;
  const schema = hasRealPassword
    ? deleteAccountWithPasswordSchema
    : deleteAccountWithoutPasswordSchema;

  const textInputCreator: TextInputCreator<DeleteAccountWithPasswordValidatedData> =
    useCallback(
      ({ register, errors }) => {
        const emailInput = (
          <TextInput
            {...register("email", { required: true })}
            type="email"
            placeholder="Email address"
            error={errors.email}
            key="email"
          />
        );

        if (hasRealPassword) {
          return [
            emailInput,
            <TextInput
              {...register("password", { required: true })}
              type="password"
              placeholder="Password"
              error={errors.password}
              key="password"
            />,
          ];
        } else {
          return [emailInput];
        }
      },
      [hasRealPassword]
    );

  const onSubmit = useCallback(
    (
      data: DeleteAccountWithPasswordValidatedData,
      setError: UseFormSetError<DeleteAccountWithPasswordValidatedData>
    ) => {
      console.log("on submit", data);
      const errorField = hasRealPassword ? "password" : "email";
      const errorHandler = createErrorSchemaHandler(deleteAccountErrors, {
        invalidPassword(error) {
          setError(errorField, {
            message: "Invalid email or password",
            type: "custom",
          });
        },
        forbidden(error) {
          setError(errorField, {
            message: "You do not have permission to delete this account",
            type: "custom",
          });
        },
        default(error) {
          setError(errorField, {
            message: "An unexpected error occurred",
            type: "custom",
          });
        },
      });

      const deleteApi = deleteMeApi();

      console.log("sending request to delete");

      return (
        hasRealPassword
          ? deleteApi.deleteUserAccount(data)
          : deleteApi.deleteUserAccountOnlyConnectedNoPassword(data)
      )
        .then(() => {
          router.push("/delete-account-success");
        })
        .catch(errorHandler);
    },
    [hasRealPassword, router]
  );

  return (
    <AuthForm
      onSubmit={onSubmit}
      textInputCreator={textInputCreator}
      schema={schema}
      description="Delete your account by entering your email and your password."
      submitText="Delete my Account"
      id="delete-account"
    >
      <ErrorFormattedMessage message="THIS CANNOT BE UNDONE" />
    </AuthForm>
  );
}
