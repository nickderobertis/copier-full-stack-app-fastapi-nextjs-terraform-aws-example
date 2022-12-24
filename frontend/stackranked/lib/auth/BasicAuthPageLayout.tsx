import { PropsWithChildren } from "react";
import styles from "./BasicAuthPageLayout.module.css";

export default function BasicAuthPageLayout(
  props: PropsWithChildren
): JSX.Element {
  const wrapperStyles = `${styles.vh} flex justify-center content-center items-center flex-wrap overflow-y-auto p-7`;
  return <div className={wrapperStyles}>{props.children}</div>;
}
