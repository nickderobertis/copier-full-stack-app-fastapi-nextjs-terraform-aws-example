import { ReactNode, useCallback, useMemo } from "react";
import { useForm } from "react-hook-form";
import TextInput from "../../core/forms/TextInput";
import { yupResolver } from "@hookform/resolvers/yup";
import SubmitButton from "../../core/buttons/SubmitButton";
import AuthLink from "../AuthLink";
import { loginSchema, LoginValidatedData } from "./login.data";
import api, { loginErrorSchema } from "./login.api";
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
  afterLogin: (data: LoginValidatedData) => void;
};

export default function LogIn({ afterLogin }: Props): JSX.Element {
  const methods = useForm<LoginValidatedData>({
    resolver: yupResolver(loginSchema),
  });
  const {
    register,
    setError,
    formState: { errors },
  } = methods;
  const onSubmit = useCallback(
    function onSubmit(data: LoginValidatedData) {
      const errorHandler = createErrorSchemaHandler(loginErrorSchema, {
        invalidCredentials(error) {
          setError("password", {
            message: "Invalid email or password",
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
      return api()
        .logIn(data)
        .then(() => {
          afterLogin(data);
        })
        .catch(errorHandler);
    },
    [afterLogin, setError]
  );

  const textInputs: ReactNode[] = useMemo(() => {
    const baseInputs = [
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
  }, [errors.email, errors.password, register]);

  return (
    <div
      className="block rounded-lg shadow-lg bg-white px-6 py-12 md:px-12"
      id="login-form"
    >
      <NestedForm methods={methods} onSubmit={onSubmit}>
        {textInputs}
        <div className="mt-9"></div>
        <SubmitButton text="Log in" />
        <div className="mt-5"></div>
        <SocialLoginButtons />
        <div className="flex justify-around">
          <AuthLink href="/forgot-password" text="Forgot password?" />
          <AuthLink href="/?signup=true" as="/signup" text="Need an account?" />
        </div>
      </NestedForm>
    </div>
  );
}
