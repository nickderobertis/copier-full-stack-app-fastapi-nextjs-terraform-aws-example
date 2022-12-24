import * as yup from "yup";
import passwordValidator from "../../core/data/password-validator";

export const forgotPasswordBeginSchema = yup
  .object({
    email: yup.string().email().required(),
  })
  .required();

export type ForgotPasswordBeginInputData = yup.TypeOf<
  typeof forgotPasswordBeginSchema
>;
export type ForgotPasswordBeginValidatedData = yup.Asserts<
  typeof forgotPasswordBeginSchema
>;

export const forgotPasswordResetSchema = yup
  .object({
    password: passwordValidator,
  })
  .required();

export type ForgotPasswordResetInputData = yup.TypeOf<
  typeof forgotPasswordResetSchema
>;
export type ForgotPasswordResetValidatedData = yup.Asserts<
  typeof forgotPasswordResetSchema
>;
