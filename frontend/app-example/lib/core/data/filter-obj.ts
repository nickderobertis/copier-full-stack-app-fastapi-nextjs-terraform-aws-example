import { isFalsy } from "./falsy";

export function filterObj<T extends Record<string, unknown>>(
  obj: T,
  fn: (key: keyof T, value: T[keyof T]) => boolean
): Partial<T> {
  const filteredObj: Partial<T> = {};
  for (const key in obj) {
    if (obj.hasOwnProperty(key)) {
      const value = obj[key];
      if (fn(key, value)) {
        filteredObj[key] = value;
      }
    }
  }
  return filteredObj;
}

export function filterObjForTruthyValues<T extends Record<string, unknown>>(
  obj: T
): Partial<T> {
  return filterObj(obj, (_, value) => !isFalsy(value));
}
