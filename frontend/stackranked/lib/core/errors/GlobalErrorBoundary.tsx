import { Component, ErrorInfo, PropsWithChildren } from "react";
import log from "../logging/log";
import Button from "../buttons/Button";
import GlobalErrorDisplay from "./GlobalErrorDisplay";

type Props = PropsWithChildren<{}>;

type State = {
  error?: any;
};

export default class GlobalErrorBoundary extends Component<Props, State> {
  private promiseRejectionHandler = (event: PromiseRejectionEvent) => {
    const error = event.reason;
    log.error("Uncaught promise rejection:", error);
    this.setState({
      error,
    });
  };

  constructor(props: Props) {
    super(props);
    this.state = {};
  }

  public static getDerivedStateFromError(error: Error): State {
    // Update state so the next render will show the fallback UI.
    return { error };
  }

  public componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    // You can also log the error to an error reporting service
    log.error("Uncaught error:", error, errorInfo);
  }

  componentDidMount() {
    // Add an event listener to the window to catch unhandled promise rejections & stash the error in the state
    window.addEventListener("unhandledrejection", this.promiseRejectionHandler);
  }

  componentWillUnmount() {
    window.removeEventListener(
      "unhandledrejection",
      this.promiseRejectionHandler
    );
  }

  render() {
    if (this.hasError) {
      // You can render any custom fallback UI
      return <GlobalErrorDisplay onOk={() => this.clearError()} />;
    }

    return this.props.children;
  }

  private clearError() {
    this.setState({ error: undefined });
  }

  get hasError(): boolean {
    return !!this.state.error;
  }
}
