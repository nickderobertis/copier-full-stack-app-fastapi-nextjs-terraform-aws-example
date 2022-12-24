import logoutApi from "../../auth/logout/logout.api";
import ProfileDropdownItem from "./ProfileDropdownItem";

function logOut() {
  logoutApi().logOut();
}

export default function ProfileDropdownList(): JSX.Element {
  return (
    <div className="hidden group-hover:block absolute right-0 top-9 w-32 shadow-lg bg-white">
      <hr className="border-t-2"></hr>
      <ProfileDropdownItem
        text="Log out"
        href="/logout"
        beforeNavigate={logOut}
      />
      <hr className="border-t-2"></hr>
      <ProfileDropdownItem text="Account" href="/account" />
    </div>
  );
}
