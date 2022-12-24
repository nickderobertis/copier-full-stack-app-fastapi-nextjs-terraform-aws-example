import * as yup from "yup";
import passwordValidator from "../../core/data/password-validator";

export const updateAccountSchema = yup
  .object({
    name: yup.string().optional(),
    email: yup.string().email().optional(),
    password: yup.string().required(),
  })
  .required();

export type UpdateAccountInputData = yup.TypeOf<typeof updateAccountSchema>;
export type UpdateAccountValidatedData = yup.Asserts<
  typeof updateAccountSchema
>;

export const updatePasswordSchema = yup
  .object({
    newPassword: passwordValidator,
    oldPassword: yup.string().required(),
  })
  .required();

export type UpdatePasswordInputData = yup.TypeOf<typeof updatePasswordSchema>;
export type UpdatePasswordValidatedData = yup.Asserts<
  typeof updatePasswordSchema
>;

export const deleteAccountWithPasswordSchema = yup
  .object({
    email: yup.string().email().required(),
    password: yup.string().required(),
  })
  .required();

export type DeleteAccountWithPasswordInputData = yup.TypeOf<
  typeof deleteAccountWithPasswordSchema
>;
export type DeleteAccountWithPasswordValidatedData = yup.Asserts<
  typeof deleteAccountWithPasswordSchema
>;

export const deleteAccountWithoutPasswordSchema = yup

  .object({
    email: yup.string().email().required(),
  })
  .required();

export type DeleteAccountWithoutPasswordInputData = yup.TypeOf<
  typeof deleteAccountWithoutPasswordSchema
>;
export type DeleteAccountWithoutPasswordValidatedData = yup.Asserts<
  typeof deleteAccountWithoutPasswordSchema
>;
