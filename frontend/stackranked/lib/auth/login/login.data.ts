import * as yup from "yup";

export const loginSchema = yup
  .object({
    email: yup.string().email().required(),
    password: yup.string().required(),
  })
  .required();

export type LoginInputData = yup.TypeOf<typeof loginSchema>;
export type LoginValidatedData = yup.Asserts<typeof loginSchema>;
