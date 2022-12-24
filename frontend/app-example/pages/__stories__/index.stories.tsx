import { Meta } from "@storybook/react";
import Home from "../index.page";

const meta: Meta = {
  title: "Pages/Home",
  component: Home,
};

export default meta;

export const HomePage = () => (
  <div className="w-full">
    <Home />
  </div>
);
