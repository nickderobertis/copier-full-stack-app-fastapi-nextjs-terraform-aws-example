import { UseFormSetError } from "react-hook-form";
import { createErrorSchemaHandler } from "../../core/errors/known-error-handler";
import TextInput from "../../core/forms/TextInput";
import { useMe } from "../../user/user.api";
import AuthForm, { TextInputCreator } from "../AuthForm";
import accountApi, { updateAccountErrors } from "./account.api";
import {
  updateAccountSchema,
  UpdateAccountValidatedData,
} from "./account.data";

const textInputCreator: TextInputCreator<UpdateAccountValidatedData> = ({
  register,
  errors,
}) => {
  return [
    <TextInput
      {...register("name", { required: true })}
      type="string"
      placeholder="Name"
      error={errors.name}
      key="name"
    />,
    <TextInput
      {...register("email", { required: true })}
      type="email"
      placeholder="Email address"
      error={errors.email}
      key="email"
    />,
    <TextInput
      {...register("password", { required: true })}
      type="password"
      placeholder="Password"
      error={errors.password}
      key="password"
    />,
  ];
};

type CurrentAccountDetailsProps = {
  name?: string;
  email?: string;
};

function CurrentAccountDetails({
  name,
  email,
}: CurrentAccountDetailsProps): JSX.Element {
  return (
    <div>
      <p id="current-name">Name: {name}</p>
      <p id="current-email">Email: {email}</p>
    </div>
  );
}

export default function UpdateAccountDetails(): JSX.Element {
  const { data } = useMe();
  const { name, email } = data || {};
  const onSubmit = (
    data: UpdateAccountValidatedData,
    setError: UseFormSetError<UpdateAccountValidatedData>
  ) => {
    const errorHandler = createErrorSchemaHandler(updateAccountErrors, {
      invalidPassword(error) {
        setError("password", {
          message: "Invalid password",
          type: "custom",
        });
      },
      default(error) {
        setError("password", {
          message: "An unexpected error occurred",
          type: "custom",
        });
      },
    });
    return accountApi().updateUserAccount(data, email).catch(errorHandler);
  };

  return (
    <AuthForm
      onSubmit={onSubmit}
      textInputCreator={textInputCreator}
      schema={updateAccountSchema}
      description="Update your name or email by entering that and your password."
      submitText="Update my Account"
      id="update-account-details"
    >
      <CurrentAccountDetails name={name} email={email} />
    </AuthForm>
  );
}
