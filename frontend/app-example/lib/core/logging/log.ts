// Basic logger module with info, warn, error, and debug levels.
// Logs to console.log, error etc. currently
import * as Sentry from "@sentry/nextjs";

type LogFn = (message: string, ...args: any[]) => void;
type ErrorLogFn = (error: Error) => void;

class Logger {
  constructor(
    private name: string,
    private infoLogger: LogFn = console.log,
    private warnLogger: LogFn = console.warn,
    private errorLogger: LogFn = console.error,
    private exceptionLogger: ErrorLogFn = console.error,
    private debugLogger: LogFn = console.debug
  ) {}

  info(message: string, ...args: any[]) {
    this.infoLogger(`${this.name}: ${message}`, ...args);
  }

  warn(message: string, ...args: any[]) {
    this.warnLogger(`${this.name}: ${message}`, ...args);
  }

  error(message: string, ...args: any[]) {
    this.errorLogger(`${this.name}: ${message}`, ...args);
  }

  exception(error: unknown) {
    this.exceptionLogger(error as Error);
  }

  debug(message: string, ...args: any[]) {
    this.debugLogger(`${this.name}: ${message}`, ...args);
  }
}

function createLogger(name: string) {
  const sentryEnabled = !!process.env.NEXT_PUBLIC_SENTRY_DSN;
  if (!sentryEnabled) {
    return new Logger(name);
  }

  function logWarn(message: string, ...args: any[]) {
    Sentry.captureMessage(message, {
      level: "warning",
    });
  }

  function logError(message: string, ...args: any[]) {
    Sentry.captureMessage(message, {
      level: "error",
    });
  }

  return new Logger(
    name,
    Sentry.captureMessage,
    logWarn,
    logError,
    Sentry.captureException
  );
}

export default createLogger("app");
