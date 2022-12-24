import { ReactNode, useCallback, useMemo } from "react";
import { useForm } from "react-hook-form";
import TextInput from "../../core/forms/TextInput";
import { yupResolver } from "@hookform/resolvers/yup";
import SubmitButton from "../../core/buttons/SubmitButton";
import AuthLink from "../AuthLink";
import { SignUpValidatedData, signUpSchema } from "./signup.data";
import api, { signUpErrors } from "./signup.api";
import { createErrorSchemaHandler } from "../../core/errors/known-error-handler";
import NestedForm from "../../core/forms/NestedForm";
import SocialLoginButtons from "Auth/social-login/SocialLoginButtons";

function TextInputWrapper(props: { input: ReactNode }): JSX.Element {
  const { input } = props;
  return (
    <div className="md:gap-6">
      <div className="mb-6">{input}</div>
    </div>
  );
}

type Props = {
  afterSignUp: (data: SignUpValidatedData) => unknown;
};

export default function SignUp({ afterSignUp }: Props): JSX.Element {
  const methods = useForm<SignUpValidatedData>({
    resolver: yupResolver(signUpSchema),
  });
  const {
    register,
    setError,
    formState: { errors, isValid },
  } = methods;
  const onSubmit = useCallback(
    async function (data: SignUpValidatedData) {
      const errorHandler = createErrorSchemaHandler(signUpErrors, {
        emailInUse(error) {
          setError("email", {
            message: "Email already in use",
            type: "value",
          });
        },
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
      await api()
        .signUp(data)
        .then(() => afterSignUp(data))
        .catch(errorHandler);
    },
    [afterSignUp, setError]
  );

  const textInputs: ReactNode[] = useMemo(() => {
    const baseInputs = [
      <TextInput
        {...register("name", { required: true })}
        type="text"
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
    return baseInputs.map((input, index) => (
      <TextInputWrapper key={index} input={input} />
    ));
  }, [errors.email, errors.name, errors.password, register]);

  return (
    <div className="block rounded-lg shadow-lg bg-white px-6 py-12 md:px-12">
      <NestedForm methods={methods} onSubmit={onSubmit}>
        {textInputs}
        <div className="mt-9"></div>
        <SubmitButton text="Sign up" />
        <div className="mt-5"></div>
        <SocialLoginButtons />
        <AuthLink
          href="/?login=true"
          as="/login"
          text="Already have an account?"
        />
      </NestedForm>
    </div>
  );
}
