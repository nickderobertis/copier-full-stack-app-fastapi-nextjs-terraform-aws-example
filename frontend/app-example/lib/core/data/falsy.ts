export function isFalsy(value: unknown): boolean {
  return (
    value === undefined ||
    value === null ||
    value === false ||
    value === 0 ||
    value === ""
  );
}

export function objIsEmpty(obj: object): boolean {
  return Object.keys(obj).length === 0;
}
