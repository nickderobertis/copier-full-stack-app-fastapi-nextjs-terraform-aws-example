import { PropsWithChildren } from "react";
import { FormProvider, UseFormReturn } from "react-hook-form";

type Props<T> = PropsWithChildren<{
  methods: UseFormReturn<T>;
  onSubmit: (data: T) => unknown;
}>;

export default function NestedForm<T>({
  methods,
  onSubmit,
  children,
}: Props<T>): JSX.Element {
  return (
    <FormProvider {...methods}>
      <form onSubmit={methods.handleSubmit(onSubmit)}>{children}</form>
    </FormProvider>
  );
}
