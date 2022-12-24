import { FieldError } from "react-hook-form";
import { ErrorFormattedMessage } from "./ErrorFormattedMessage";

type Props = {
  error?: FieldError;
};

export default function FieldErrorDisplay({ error }: Props) {
  if (!error) {
    return null;
  }
  if (error.type === "required") {
    return <ErrorFormattedMessage message="This field is required" />;
  }
  if (!error.message) {
    return null;
  }
  return <ErrorFormattedMessage message={error.message} />;
}
