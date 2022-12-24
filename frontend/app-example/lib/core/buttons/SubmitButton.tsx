import { CSSProperties, useMemo } from "react";
import { useForm, useFormContext } from "react-hook-form";
import ReactiveButton from "reactive-button";
import { useDeepCompareMemo } from "use-deep-compare";
import styles from "./SubmitButton.module.css";

export type ButtonState = "idle" | "loading" | "success" | "error";

type Props = {
  text: string;
  state?: ButtonState;
};

const classes = `${styles.SubmitButton} inline-block px-6 py-2.5 w-full bg-blue-600 text-white font-medium text-xs leading-tight uppercase shadow-md hover:bg-blue-700 hover:disabled:bg-blue-600 hover:shadow-lg hover:disabled:shadow-md focus:bg-blue-700 focus:shadow-lg focus:outline-none focus:ring-0 active:bg-blue-800 active:shadow-lg transition duration-150 ease-in-out`;

export default function SubmitButton({ text, state }: Props) {
  const {
    formState: { errors },
  } = useFormContext();
  const hasErrors = Object.keys(errors).length > 0;

  const stateWithDefault = state ?? "idle";
  return (
    <ReactiveButton
      disabled={hasErrors}
      buttonState={stateWithDefault}
      idleText={text}
      type="submit"
      className={classes}
    />
  );
}
