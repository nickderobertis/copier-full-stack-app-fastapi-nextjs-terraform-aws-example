import Link from "next/link";
import { forwardRef, MouseEvent, MouseEventHandler } from "react";

type Props = {
  text: string;
  href: string;
  beforeNavigate?: MouseEventHandler<HTMLAnchorElement>;
};

type ItemInsideLinkProps = {
  // Manually provided props
  text: string;
  beforeNavigate?: MouseEventHandler<HTMLAnchorElement>;
  // Props that will be provided automatically by next/link
  onClick?: MouseEventHandler<HTMLAnchorElement>;
  href?: string;
};

const ItemInsideLink = forwardRef<HTMLAnchorElement, ItemInsideLinkProps>(
  ({ onClick, href, text, beforeNavigate }, ref) => {
    function fullOnClick(e: MouseEvent<HTMLAnchorElement>) {
      beforeNavigate && beforeNavigate(e);
      onClick && onClick(e);
    }
    return (
      <a href={href} onClick={fullOnClick} ref={ref}>
        {text}
      </a>
    );
  }
);
ItemInsideLink.displayName = "ItemInsideLink";

export default function ProfileDropdownItem({
  text,
  href,
  beforeNavigate,
}: Props): JSX.Element {
  return (
    <div className="h-10 w-full flex justify-center items-center">
      <span>
        <Link href={href} passHref>
          <ItemInsideLink text={text} beforeNavigate={beforeNavigate} />
        </Link>
      </span>
    </div>
  );
}
