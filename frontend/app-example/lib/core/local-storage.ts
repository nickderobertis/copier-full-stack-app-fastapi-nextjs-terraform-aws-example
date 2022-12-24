export async function storeLocalData(value: any, key: string): Promise<void> {
  try {
    const jsonValue = JSON.stringify(value);
    await localStorage.setItem(key, jsonValue);
  } catch (e) {
    throw new Error(`error saving ${value} to ${key}`);
  }
}

export async function getLocalData<T>(key: string): Promise<T | null> {
  try {
    const jsonValue = await localStorage.getItem(key);
    return jsonValue != null ? JSON.parse(jsonValue) : null;
  } catch (e) {
    throw new Error(`error reading ${key} from local data`);
  }
}

export async function deleteLocalData(key: string): Promise<void> {
  try {
    await localStorage.removeItem(key);
  } catch (e) {
    throw new Error(`error removing ${key} from local data`);
  }
}
