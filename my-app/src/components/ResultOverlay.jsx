import './ResultOverlay.css';
import ResultPanel from './ResultPanel';
import { MdClose } from "react-icons/md"; // thêm dòng này

export default function ResultOverlay({ result, onClose }) {
  if (!result) return null;

  return (
    <div className="overlay-backdrop">
      <div className="overlay-box">
        <div className="overlay-header">
          <h2>{result.title}</h2>
          <button className="close-btn" onClick={onClose}>
            <MdClose />
          </button>
        </div>
        <div className="overlay-body">
          <ResultPanel data={result.data} />
        </div>
      </div>
    </div>
  );
}
