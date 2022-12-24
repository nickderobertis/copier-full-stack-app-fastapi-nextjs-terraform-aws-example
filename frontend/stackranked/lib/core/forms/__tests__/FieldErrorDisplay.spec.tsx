import { render, screen } from "@testing-library/react";
import "@testing-library/jest-dom";
import FieldErrorDisplay from "../FieldErrorDisplay";

it("renders a required message", () => {
  render(<FieldErrorDisplay error={{ type: "required" }} />);

  const message = screen.getByText("This field is required");

  expect(message).toBeInTheDocument();
});

it("renders a custom message", () => {
  const expectMessage = "custom message";
  render(
    <FieldErrorDisplay error={{ type: "maxLength", message: expectMessage }} />
  );

  const message = screen.getByText(expectMessage);

  expect(message).toBeInTheDocument();
});

it("renders nothing with no error", () => {
  const { container } = render(<FieldErrorDisplay />);
  expect(container.firstChild).toBeNull();
});
