import ErrorCard from "./ErrorCard";

type Props = {
  onOk: () => void;
};

export default function GlobalErrorDisplay({ onOk }: Props) {
  return (
    <div className="flex justify-center content-center items-center flex-wrap h-[85vh]">
      <ErrorCard onOk={onOk} />
    </div>
  );
}
