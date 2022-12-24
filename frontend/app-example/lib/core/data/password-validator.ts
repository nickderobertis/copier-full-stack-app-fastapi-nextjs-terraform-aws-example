import * as yup from "yup";
const passwordValidator = yup.string().required().min(8);
export default passwordValidator;
