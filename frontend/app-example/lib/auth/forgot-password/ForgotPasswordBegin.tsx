import { useRouter } from "next/router";
import TextInput from "../../core/forms/TextInput";
import AuthForm, { TextInputCreator } from "../AuthForm";
import forgotPasswordApi from "./forgot-password.api";
import {
  forgotPasswordBeginSchema,
  ForgotPasswordBeginValidatedData,
} from "./forgot-password.data";

const textInputCreator: TextInputCreator<ForgotPasswordBeginValidatedData> = ({
  register,
  errors,
}) => {
  return [
    <TextInput
      {...register("email", { required: true })}
      type="email"
      placeholder="Email address"
      error={errors.email}
      key="email"
    />,
  ];
};

export default function ForgotPasswordBegin(): JSX.Element {
  const router = useRouter();
  const onSubmit = async (data: ForgotPasswordBeginValidatedData) => {
    await forgotPasswordApi().forgotPasswordBegin(data);
    router.push("/forgot-password-submitted?email=" + data.email);
  };

  return (
    <AuthForm
      onSubmit={onSubmit}
      textInputCreator={textInputCreator}
      schema={forgotPasswordBeginSchema}
      description="Enter your email address and we'll send you a link to reset your password."
      submitText="Send me a Link"
      id="forgot-password-begin"
    />
  );
}
