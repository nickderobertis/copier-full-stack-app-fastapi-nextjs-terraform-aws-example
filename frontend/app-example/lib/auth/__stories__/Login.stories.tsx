import { Meta } from "@storybook/react";
import LogIn from "../login/LogIn";

const meta: Meta = {
  title: "Components/Auth/LogIn",
  component: LogIn,
};

export default meta;

export const LogInBlank = () => (
  <div className="w-full flex justify-center">
    <LogIn afterLogin={console.log} />
  </div>
);
