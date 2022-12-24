import Button from "../buttons/Button";

type Props = {
  onOk: () => void;
};

export default function ErrorCard({ onOk }: Props) {
  return (
    <div className="block rounded-lg shadow-lg bg-white px-6 py-12 md:px-12">
      <h1>Something went wrong.</h1>
      <div className="mt-6"></div>
      <Button text="Ok" onClick={onOk} />
    </div>
  );
}
