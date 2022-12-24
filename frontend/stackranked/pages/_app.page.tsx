import "../styles/globals.css";
import type { AppProps } from "next/app";
import App from "../lib/App";

function AppPage(props: AppProps) {
  return <App {...props} />;
}

export default AppPage;
