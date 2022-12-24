import log from "Logging/log";
import { NextPage } from "next";
import { useRouter } from "next/router";
import { useEffect } from "react";

const devPageEnabled = process.env.NEXT_PUBLIC_ENABLE_DEV_PAGES === "true";

const Dev: NextPage = () => {
  const { push } = useRouter();

  useEffect(() => {
    if (!devPageEnabled) {
      push("/");
    }
  }, [push]);

  return (
    <div>
      <h1>Dev Page</h1>
      <h2>Error Testing</h2>
      <button
        className="inline-block px-6 py-2.5 mr-2 bg-transparent text-blue-600 font-medium text-xs leading-tight uppercase rounded hover:text-blue-700 hover:bg-gray-100 focus:bg-gray-100 focus:outline-none focus:ring-0 active:bg-gray-200 transition duration-150 ease-in-out"
        onClick={() => {
          throw new Error("Test unexpected error");
        }}
      >
        Unexpected Exception
      </button>
      <button
        className="inline-block px-6 py-2.5 mr-2 bg-transparent text-blue-600 font-medium text-xs leading-tight uppercase rounded hover:text-blue-700 hover:bg-gray-100 focus:bg-gray-100 focus:outline-none focus:ring-0 active:bg-gray-200 transition duration-150 ease-in-out"
        onClick={() => {
          try {
            const errorFn = () => {
              throw new Error("Test caught error");
            };
            errorFn();
          } catch (err) {
            log.exception(err);
          }
        }}
      >
        Caught Exception
      </button>
      <button
        className="inline-block px-6 py-2.5 mr-2 bg-transparent text-blue-600 font-medium text-xs leading-tight uppercase rounded hover:text-blue-700 hover:bg-gray-100 focus:bg-gray-100 focus:outline-none focus:ring-0 active:bg-gray-200 transition duration-150 ease-in-out"
        onClick={() => {
          log.info("Test captured message info level");
        }}
      >
        Log info message to Sentry
      </button>
      <button
        className="inline-block px-6 py-2.5 mr-2 bg-transparent text-blue-600 font-medium text-xs leading-tight uppercase rounded hover:text-blue-700 hover:bg-gray-100 focus:bg-gray-100 focus:outline-none focus:ring-0 active:bg-gray-200 transition duration-150 ease-in-out"
        onClick={() => {
          log.warn("Test captured message warning level");
        }}
      >
        Log warning message to Sentry
      </button>
      <button
        className="inline-block px-6 py-2.5 mr-2 bg-transparent text-blue-600 font-medium text-xs leading-tight uppercase rounded hover:text-blue-700 hover:bg-gray-100 focus:bg-gray-100 focus:outline-none focus:ring-0 active:bg-gray-200 transition duration-150 ease-in-out"
        onClick={() => {
          log.error("Test captured message error level");
        }}
      >
        Log error message to Sentry
      </button>
    </div>
  );
};

export default Dev;
