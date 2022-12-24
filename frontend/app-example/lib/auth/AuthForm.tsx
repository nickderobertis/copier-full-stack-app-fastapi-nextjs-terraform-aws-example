import {
  PropsWithChildren,
  ReactNode,
  useCallback,
  useEffect,
  useState,
} from "react";
import { useDeepCompareCallback, useDeepCompareMemo } from "use-deep-compare";
import {
  DeepRequired,
  FieldErrorsImpl,
  useForm,
  UseFormRegister,
  UseFormReset,
  UseFormSetError,
} from "react-hook-form";
import { yupResolver } from "@hookform/resolvers/yup";
import * as yup from "yup";
import SubmitButton, { ButtonState } from "Core/buttons/SubmitButton";
import AuthCard from "./AuthCard";
import { objIsEmpty } from "../core/data/falsy";
import NestedForm from "../core/forms/NestedForm";

type TextInputCreatorOptions<T> = {
  register: UseFormRegister<T>;
  errors: FieldErrorsImpl<DeepRequired<T>>;
};
export type TextInputCreator<T> = (
  options: TextInputCreatorOptions<T>
) => ReactNode[];

type Props<T> = PropsWithChildren<{
  textInputCreator: TextInputCreator<T>;
  schema: yup.AnyObjectSchema;
  onSubmit: (
    data: T,
    setError: UseFormSetError<T>,
    reset: UseFormReset<T>
  ) => Promise<unknown>;
  description: string;
  submitText: string;
  id: string;
}>;

function TextInputWrapper(props: { input: ReactNode }): JSX.Element {
  const { input } = props;
  return (
    <div className="md:gap-6">
      <div className="mb-6">{input}</div>
    </div>
  );
}

export default function AuthForm<T>({
  textInputCreator,
  onSubmit,
  schema,
  description,
  submitText,
  children,
  id,
}: Props<T>): JSX.Element {
  const methods = useForm<T>({ resolver: yupResolver(schema) });
  const {
    register,
    formState: { errors },
    setError,
    reset,
  } = methods;
  const [buttonState, setButtonState] = useState<ButtonState>("idle");
  const [buttonStateShouldChange, setButtonStateShouldChange] =
    useState<boolean>(false);
  const useTextInputs: ReactNode[] = useDeepCompareMemo(() => {
    const textInputs = textInputCreator({ register, errors });
    return textInputs.map((input, index) => (
      <TextInputWrapper key={index} input={input} />
    ));
  }, [{ ...errors }, register, textInputCreator]);

  const useOnSubmit = useDeepCompareCallback(
    async (data: T) => {
      setButtonState("loading");
      await onSubmit(data, setError, reset);
      setButtonStateShouldChange(true);
    },
    [{ ...errors }, onSubmit, setError]
  );

  useEffect(() => {
    if (buttonStateShouldChange) {
      if (objIsEmpty(errors)) {
        setButtonState("success");
      } else {
        setButtonState("error");
      }
      setButtonStateShouldChange(false);
    }
  }, [buttonStateShouldChange, errors]);

  return (
    <AuthCard id={id}>
      <NestedForm methods={methods} onSubmit={useOnSubmit}>
        <p>{description}</p>
        {children}
        <div className="mt-6"></div>
        {useTextInputs}
        <div className="mt-12"></div>
        <SubmitButton text={submitText} state={buttonState} />
      </NestedForm>
    </AuthCard>
  );
}
