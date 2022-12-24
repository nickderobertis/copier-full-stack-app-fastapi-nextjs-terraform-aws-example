import SignUp from "../auth/signup/SignUp";
import { SignUpValidatedData } from "../auth/signup/signup.data";

function onSignUp(data: SignUpValidatedData) {
  console.log("signed up from home page with", data);
}

export default function Home(): JSX.Element {
  return (
    <div>
      <section className="mb-40">
        <div className="px-6 py-12 md:px-12 bg-gray-100 text-gray-800 text-center lg:text-left">
          <div className="container mx-auto xl:px-32">
            <div className="grid lg:grid-cols-2 gap-12">
              <div className="mt-12 lg:mt-0">
                <h1 className="text-5xl md:text-6xl xl:text-7xl font-bold tracking-tight mb-12">
                  Tag-line <br />
                  <span className="text-blue-600">placeholder</span>
                </h1>
                <p className="text-gray-600">
                  Lorem ipsum dolor sit amet consectetur adipisicing elit...
                  Eveniet, itaque accusantium odio, soluta, corrupti aliquam
                  quibusdam tempora at cupiditate quis eum maiores libero
                  veritatis? Dicta facilis sint aliquid ipsum atque?
                </p>
              </div>
              <div className="mb-12 lg:mb-0">
                <SignUp afterSignUp={onSignUp} />
              </div>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}
