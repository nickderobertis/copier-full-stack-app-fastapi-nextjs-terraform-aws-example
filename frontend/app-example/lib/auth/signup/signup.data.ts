import * as yup from "yup";
import passwordValidator from "../../core/data/password-validator";

export const signUpSchema = yup
  .object({
    name: yup.string().required(),
    email: yup.string().email().required(),
    password: passwordValidator,
  })
  .required();

export type SignUpInputData = yup.TypeOf<typeof signUpSchema>;
export type SignUpValidatedData = yup.Asserts<typeof signUpSchema>;
